#!/usr/bin/env python3
"""Blender-only adapter. Creates fresh proxy scenes; run in an isolated process."""
import argparse,hashlib,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'camera-spatial-design'/'scripts'))
from spatial_spec import validate,analyze,sample,subject_positions

SMOKE_MAX_DIMENSION=320

def smoke_resolution(resolution):
    scale=min(1,SMOKE_MAX_DIMENSION/max(resolution))
    return [max(1,min(SMOKE_MAX_DIMENSION,round(v*scale))) for v in resolution]


def arguments():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--spec',required=True);p.add_argument('--output',required=True)
    p.add_argument('--mode',choices=['smoke','stills','sequence'],default='stills')
    p.add_argument('--render-map',help='stills-mode JSON or @file: {shot:[frame|{frame,panel}]} or {shot:{panel:frame}} of local 0-based frames to render')
    return p.parse_args(argv)


def parse_render_map(text):
    """Normalize an explicit render map to {shot_id:[{frame,label,panels}]}.

    Accepted shapes: {shot:[frame, ...]} or {shot:[{frame,label?,panel?|panels?}]},
    {shot:{panel_or_label:frame}}, or [{shot_id,frame,label?,panel?|panels?}].
    Returns (map, errors); frame bounds are checked later in render_plan.
    """
    errors=[];out={}
    try:data=json.loads(text)
    except ValueError as e:return None,['invalid JSON: '+str(e)]
    def frame_of(v,label):
        if isinstance(v,int) and not isinstance(v,bool):return v
        errors.append(f'{label}: frame must be an integer');return None
    def entry(frame,label,panels):return {'frame':frame,'label':label,'panels':panels if isinstance(panels,list) else ([panels] if panels else [])}
    if isinstance(data,dict):
        for shot,frames in data.items():
            out.setdefault(shot,[])
            if isinstance(frames,dict):
                for label,v in frames.items():
                    f=frame_of(v,f'{shot}.{label}')
                    if f is not None:out[shot].append(entry(f,label,[label]))
            elif isinstance(frames,list):
                for i,v in enumerate(frames):
                    if isinstance(v,dict):
                        f=frame_of(v.get('frame'),f'{shot}[{i}]')
                        if f is not None:out[shot].append(entry(f,str(v.get('label',v.get('panel',f))),v.get('panels',v.get('panel'))))
                    else:
                        f=frame_of(v,f'{shot}[{i}]')
                        if f is not None:out[shot].append(entry(f,'selected',[]))
            else:errors.append(f'{shot}: frames must be an array or object')
    elif isinstance(data,list):
        for i,v in enumerate(data):
            if not isinstance(v,dict) or not isinstance(v.get('shot_id'),str):
                errors.append(f'[{i}]: entry needs shot_id');continue
            f=frame_of(v.get('frame'),v['shot_id'])
            if f is None:continue
            label=str(v.get('label',v.get('panel',f)))
            out.setdefault(v['shot_id'],[]).append(entry(f,label,v.get('panels',v.get('panel'))))
    else:errors.append('render map must be an object or array')
    if errors:return None,errors
    if not any(out.values()):errors.append('render map selects no frames')
    return out,errors


def render_plan(spec,mode,render_map=None):
    """Decide the exact local frames to render per shot: (plan, errors).

    Frames stay in the spec's local 0..duration_frames-1 space; Blender +1
    conversion happens at render time. Every entry is {frame,label,panels}.
    """
    errors=[];plan={}
    shots={s['id']:s for s in spec.get('shots',[]) if isinstance(s,dict)}
    def add(shot_id,frame,label,panels):
        entries=plan.setdefault(shot_id,[])
        for e in entries:
            if e['frame']==frame:
                for pn in panels:
                    if pn not in e['panels']:e['panels'].append(pn)
                if label not in e['label'].split(','):e['label']=e['label']+','+label
                return
        entries.append({'frame':frame,'label':label,'panels':list(panels)})
    if render_map is not None:
        if mode!='stills':errors.append('--render-map is only valid with --mode stills')
        for shot_id,entries in sorted(render_map.items()):
            if isinstance(entries,dict):entries=[{'frame':f,'label':k,'panels':[k]} for k,f in entries.items()]
            if not isinstance(entries,list):errors.append(f'{shot_id}: render map value must be a list or object');continue
            shot=shots.get(shot_id)
            if shot is None:errors.append(f'{shot_id}: not a spec shot');continue
            n=shot.get('duration_frames')
            for e in entries:
                if isinstance(e,int) and not isinstance(e,bool):e={'frame':e,'label':'selected','panels':[]}
                f=e['frame'] if isinstance(e,dict) else None
                if not isinstance(f,int) or not isinstance(n,int) or not 0<=f<n:
                    errors.append(f'{shot_id}: frame {f} outside local 0..{n-1 if isinstance(n,int) else "?"}')
                else:add(shot_id,f,e['label'],e['panels'])
    elif mode=='sequence':
        for shot_id,shot in shots.items():
            for f in range(shot['duration_frames']):add(shot_id,f,'sequence',[])
    elif mode=='stills':
        for shot_id,shot in shots.items():
            n=shot['duration_frames']
            for f,label in [(0,'start'),(n//2,'mid'),(n-1,'end')]:add(shot_id,f,label,[])
    elif mode=='smoke':
        if spec.get('shots'):add(spec['shots'][0]['id'],0,'smoke_first_frame',[])
    else:errors.append(f'unknown mode {mode}')
    for entries in plan.values():entries.sort(key=lambda e:e['frame'])
    return plan,errors


def main():
    args=arguments()
    spec_bytes=Path(args.spec).read_bytes()
    spec=json.loads(spec_bytes.decode('utf-8'));errors=validate(spec)
    if errors:raise SystemExit(json.dumps({'valid':False,'errors':errors},ensure_ascii=False))
    render_map=None
    if args.render_map is not None:
        text=args.render_map.strip()
        if text.startswith('@'):
            try:text=Path(text[1:]).read_text(encoding='utf-8')
            except OSError as e:raise SystemExit('--render-map file error: '+str(e))
        render_map,map_errors=parse_render_map(text)
        if map_errors:raise SystemExit(json.dumps({'valid':False,'errors':['--render-map: '+e for e in map_errors]},ensure_ascii=False))
    plan,plan_errors=render_plan(spec,args.mode,render_map)
    if plan_errors:raise SystemExit(json.dumps({'valid':False,'errors':plan_errors},ensure_ascii=False))
    try:import bpy
    except ImportError:raise SystemExit('Blender bpy unavailable. Run with Blender --background --factory-startup --python, or a working bpy module.')
    from mathutils import Vector,Quaternion
    from bpy_extras.object_utils import world_to_camera_view
    out=Path(args.output).resolve()
    if out.exists():raise SystemExit('Output already exists. Choose a new folder; nothing was overwritten.')
    out.mkdir(parents=True)
    smoke=args.mode=='smoke'
    manifest={'project_id':spec['project_id'],'blender_version':bpy.app.version_string,'engine':'CYCLES CPU','mode':args.mode,'status':'running','files':[],'rendered':{},
              'camera_spec':{'version':spec.get('version'),'artifact_id':spec.get('artifact_id'),'sha256':hashlib.sha256(spec_bytes).hexdigest()},
              'shot_links':{s['id']:{'scene_id':s.get('scene_id'),'beat_ids':s.get('beat_ids',[])} for s in (spec['shots'][:1] if smoke else spec['shots'])},
              'scope':'box proxy previs; no final character/lighting/acting validation'}
    if smoke:
        manifest['scope']='smoke: first shot, one low-resolution frame; narrow pipeline check only, not whole-spec render verification; box proxy previs'
        manifest['smoke_max_dimension']=SMOKE_MAX_DIMENSION
    def write_manifest(): (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write_manifest()
    try:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        numerical={'status':'unverified','schema_status':'pass','scope':'smoke skips full-frame numerical analysis; only first-frame proxy checks run'} if smoke else analyze(spec)
        (out/'numerical-analysis.json').write_text(json.dumps(numerical,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        def material(name,color):
            m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True
            nodes=m.node_tree.nodes
            if 'Principled BSDF' in nodes:nodes['Principled BSDF'].inputs['Base Color'].default_value=color
            return m
        def box(scene,name,pos,size,color):
            vertices=[(x*size[0]/2,y*size[1]/2,z*size[2]/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
            faces=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(1,5,7,3),(0,2,6,4)]
            me=bpy.data.meshes.new(name);me.from_pydata(vertices,[],faces);ob=bpy.data.objects.new(name,me);scene.collection.objects.link(ob)
            ob.location=(pos[0],pos[1],pos[2]+size[2]/2);ob.data.materials.append(material(name,color));return ob
        def orient(ob,target,roll=0):
            q=(Vector(target)-ob.location).to_track_quat('-Z','Y')
            q.rotate(Quaternion(Vector((0,0,1)),math.radians(roll)))
            if ob.rotation_quaternion.dot(q)<0:q.negate()
            ob.rotation_quaternion=q
        inspections=[];subjects={x['id']:x for x in spec['subjects']}
        scenes=[]
        for shot in (spec['shots'][:1] if smoke else spec['shots']):
            scene=bpy.data.scenes.new(shot['id']);scenes.append(scene)
            if bpy.context.window:bpy.context.window.scene=scene
            scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
            scene.render.resolution_x,scene.render.resolution_y=spec['resolution'];scene.render.resolution_percentage=100
            if smoke:
                scene.render.resolution_x,scene.render.resolution_y=smoke_resolution(spec['resolution'])
                manifest['smoke_resolution']=[scene.render.resolution_x,scene.render.resolution_y]
            scene.render.pixel_aspect_x=scene.render.pixel_aspect_y=1;scene.render.fps=spec['fps'];scene.render.fps_base=1
            scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8
            if hasattr(scene.render,'use_motion_blur'):scene.render.use_motion_blur=False
            scene.render.image_settings.file_format='PNG';scene.frame_start=1;scene.frame_end=1 if smoke else shot['duration_frames']
            scene.world=bpy.data.worlds.new(shot['id']+'_world');scene.world.use_nodes=True
            scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.12,.12,1)
            scene.world.node_tree.nodes['Background'].inputs[1].default_value=.4
            objects={}
            for rid,row in subjects.items():objects[rid]=box(scene,shot['id']+'_'+rid,row['position'],row['size_m'],tuple(row.get('color_rgba',[.25,.5,.75,1])))
            for ob in spec['obstacles']:box(scene,shot['id']+'_'+ob['id'],ob['position'],ob['size_m'],tuple(ob.get('color_rgba',[.35,.35,.35,1])))
            box(scene,shot['id']+'_floor',[0,0,-.1],[20,20,.1],(.55,.55,.55,1))
            light=bpy.data.lights.new(shot['id']+'_key','AREA');light.energy=500;light.size=5
            lamp=bpy.data.objects.new(light.name,light);scene.collection.objects.link(lamp);lamp.location=(2,-3,6);orient(lamp,(0,0,0))
            data=bpy.data.cameras.new(shot['id']+'_camera');cam=bpy.data.objects.new(data.name,data);scene.collection.objects.link(cam);scene.camera=cam
            c=shot['camera'];data.type='PERSP';data.sensor_fit='HORIZONTAL';data.sensor_width=c['sensor_width_mm'];data.sensor_height=c['sensor_width_mm']*spec['resolution'][1]/spec['resolution'][0]
            data.clip_start=c['clip_start_m'];data.clip_end=c['clip_end_m'];data.shift_x=data.shift_y=0;data.dof.use_dof=False
            frames=range(1) if smoke else range(shot['duration_frames'])
            for f in frames:
                k=sample(c['keyframes'],f,c['interpolation'],c['lens_mm']);positions=subject_positions(spec,shot,f)
                cam.location=k['position'];orient(cam,k['target'],c.get('roll_deg',0));data.lens=k['lens_mm']
                cam.keyframe_insert('location',frame=f+1);cam.keyframe_insert('rotation_quaternion',frame=f+1);data.keyframe_insert('lens',frame=f+1)
                for rid,ob in objects.items():
                    pos=positions[rid];ob.location=(pos[0],pos[1],pos[2]+subjects[rid]['size_m'][2]/2);ob.keyframe_insert('location',frame=f+1)
            for ob in [cam,*objects.values()]:
                action=ob.animation_data.action if ob.animation_data else None
                if action and hasattr(action,'fcurves'):
                    for curve in action.fcurves:
                        for key in curve.keyframe_points:key.interpolation='LINEAR'
            checks=[]
            for f in frames:
                scene.frame_set(f+1)
                with bpy.context.temp_override(scene=scene,view_layer=scene.view_layers[0]):
                    bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
                positions=subject_positions(spec,shot,f)
                for rid in shot['subject_ids']:
                    pos=positions[rid];height=subjects[rid]['size_m'][2]
                    for point_name,z in [('center',height/2),('head',height*.95)]:
                        point=Vector((pos[0],pos[1],pos[2]+z));ndc=world_to_camera_view(scene,cam,point)
                        delta=point-cam.location;dist=delta.length
                        hit,loc,normal,index,obj,matrix=scene.ray_cast(deps,cam.location,delta.normalized(),distance=dist+1e-4)
                        first=obj.original if hit and hasattr(obj,'original') else obj
                        visible=ndc.z>data.clip_start and ndc.z<data.clip_end and 0<=ndc.x<=1 and 0<=ndc.y<=1 and (not hit or first==objects[rid])
                        checks.append({'frame':f,'subject_id':rid,'point':point_name,'ndc':[ndc.x,ndc.y,ndc.z],'proxy_point_visible':visible,'first_hit':obj.name if hit else None})
            folder=out/shot['id'];folder.mkdir()
            rendered=[]
            for e in plan.get(shot['id'],[]):
                f=e['frame'];scene.frame_set(f+1);scene.render.filepath=str(folder/f'frame_{f+1:06d}.png')
                bpy.ops.render.render(write_still=True,scene=scene.name)
                path=Path(scene.render.filepath)
                if not path.is_file():raise RuntimeError('Render did not create '+str(path))
                rel=str(path.relative_to(out));manifest['files'].append(rel)
                rendered.append({'frame':f,'png':rel,'label':e['label'],'panels':e['panels']})
            manifest['rendered'][shot['id']]=rendered
            inspections.append({'shot_id':shot['id'],'scene_id':shot.get('scene_id'),'beat_ids':shot.get('beat_ids',[]),'checks':checks,'rendered':rendered})
        if bpy.context.window:bpy.context.window.scene=scenes[0]
        bpy.ops.wm.save_as_mainfile(filepath=str(out/'previs.blend'),check_existing=False)
        if not (out/'previs.blend').is_file():raise RuntimeError('Blend save missing')
        (out/'blender-inspection.json').write_text(json.dumps({'scope':'first-shot frame-zero proxy checks only' if smoke else 'proxy point projection and first ray hit, all integer frames','spec_version':spec.get('version'),'spec_sha256':manifest['camera_spec']['sha256'],'shots':inspections},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest['files']+=['previs.blend','numerical-analysis.json','blender-inspection.json'];manifest['status']='generated';write_manifest()
    except Exception as e:
        manifest['status']='failed';manifest['error']=str(e);write_manifest();raise
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
