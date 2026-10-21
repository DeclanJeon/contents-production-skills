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


def figure_proxy_parts(size_m):
    """Return stylized human-proxy part definitions derived from a subject box.

    ``size_m`` is [width, depth, height] in meters, the same subject box the
    numeric spec already defines. The returned parts are soft clay-style
    spheres: torso, neck, head. They exist so framing, headroom, eyeline
    height, silhouette overlap and occlusion read as a body in frame instead
    of an abstract box. They are proxies only: no face direction, pose,
    articulation, hair, costume or contact detail is implied, so a figure
    render never proves acting, likeness or hand/object contact.
    """
    w,d,h=[float(v) for v in size_m]
    head_r=max(0.05,h*0.075)
    head_z=h-head_r*1.25
    neck_r=max(0.03,h*0.022)
    neck_z=head_z-head_r*0.95
    torso_r=max(0.06,min(w,d)*0.38)
    torso_top=neck_z-neck_r*1.4
    torso_bottom=max(0.06*h,torso_r*0.9)
    torso_h=max(0.05,torso_top-torso_bottom)
    return [
        {'name':'torso','kind':'sphere','radius':torso_r,'scale':[1.0,1.0,torso_h/(2*torso_r)],'z':(torso_top+torso_bottom)/2},
        {'name':'neck','kind':'sphere','radius':neck_r,'scale':[1.0,1.0,1.4],'z':neck_z},
        {'name':'head','kind':'sphere','radius':head_r,'scale':[1.0,1.0,1.12],'z':head_z},
    ]


def sphere_mesh(segments=24,rings=12):
    """Return (vertices, faces) of a unit UV sphere with outward normals.

    Pure helper so the proxy geometry can be tested without Blender. The
    winding is fixed by the signed-volume check below rather than by hand.
    """
    verts=[(0.0,0.0,1.0)]
    for i in range(1,rings):
        phi=math.pi*i/rings
        z=math.cos(phi);rr=math.sin(phi)
        for j in range(segments):
            th=2.0*math.pi*j/segments
            verts.append((rr*math.cos(th),rr*math.sin(th),z))
    bottom=len(verts);verts.append((0.0,0.0,-1.0))
    faces=[]
    for j in range(segments):
        faces.append((0,1+(j+1)%segments,1+j))
    for i in range(rings-2):
        base0=1+i*segments;base1=1+(i+1)*segments
        for j in range(segments):
            j2=(j+1)%segments
            faces.append((base0+j,base0+j2,base1+j2,base1+j))
    base=1+(rings-2)*segments
    for j in range(segments):
        faces.append((base+j,base+(j+1)%segments,bottom))
    if signed_volume(verts,faces)<0:
        faces=[tuple(reversed(f)) for f in faces]
    return verts,faces


def signed_volume(verts,faces):
    """Signed volume of a closed mesh; negative means inward normals."""
    total=0.0
    for f in faces:
        for i in range(1,len(f)-1):
            a,b,c=(verts[j] for j in (f[0],f[i],f[i+1]))
            cx=b[1]*c[2]-b[2]*c[1];cy=b[2]*c[0]-b[0]*c[2];cz=b[0]*c[1]-b[1]*c[0]
            total+=a[0]*cx+a[1]*cy+a[2]*cz
    return total/6.0


def parse_focus_map(text):
    """Normalize a focus/rack-focus map to {shot_id:{'keyframes':[...],'f_number':...}}.

    Shape: {"SH01": {"f_number": 2.8, "keyframes": [{"frame": 0,
    "focus_distance_m": 2.0}, {"frame": 47, "focus_distance_m": 1.1}]}}
    Accepts a per-shot list of {frame, focus_distance_m} as well. Returns
    (map, errors). Focus is an adapter-local input: the camera-spatial-1.0
    spec carries no focus field, so this never widens the versioned schema.
    """
    errors=[];out={}
    try:data=json.loads(text)
    except ValueError as e:return None,['invalid JSON: '+str(e)]
    if not isinstance(data,dict):return None,['focus map must be an object of shot ids']
    for shot,row in data.items():
        if not isinstance(row,dict):errors.append(f'{shot}: focus entry must be an object');continue
        frames=row.get('keyframes')
        if frames is None:frames=row.get('keys')
        if not isinstance(frames,list) or not frames:errors.append(f'{shot}: focus keyframes required');continue
        parsed=[]
        for i,k in enumerate(frames):
            if not isinstance(k,dict):errors.append(f'{shot}.focus[{i}]: must be an object');continue
            f=k.get('frame');d=k.get('focus_distance_m')
            if not isinstance(f,int) or isinstance(f,bool):errors.append(f'{shot}.focus[{i}]: frame must be an integer');continue
            if not isinstance(d,(int,float)) or isinstance(d,bool) or d<=0:errors.append(f'{shot}.focus[{i}]: focus_distance_m must be positive');continue
            parsed.append({'frame':f,'focus_distance_m':float(d)})
        if len(parsed)!=len(frames):continue
        parsed.sort(key=lambda k:k['frame'])
        if len({k['frame'] for k in parsed})!=len(parsed):errors.append(f'{shot}: duplicate focus frames');continue
        fstop=row.get('f_number')
        if fstop is not None and (not isinstance(fstop,(int,float)) or isinstance(fstop,bool) or fstop<=0):errors.append(f'{shot}: f_number must be positive when present');continue
        out[shot]={'keyframes':parsed,'f_number':float(fstop) if fstop is not None else None}
    if not out and not errors:errors.append('focus map selects no shots')
    return out,errors


def focus_distance_at(keyframes,frame):
    """Linear focus distance at a local frame; constant before/after the keys."""
    if not keyframes:return None
    if frame<=keyframes[0]['frame']:return keyframes[0]['focus_distance_m']
    if frame>=keyframes[-1]['frame']:return keyframes[-1]['focus_distance_m']
    for a,b in zip(keyframes,keyframes[1:]):
        if a['frame']<=frame<=b['frame']:
            span=b['frame']-a['frame']
            if span<=0:return b['focus_distance_m']
            t=(frame-a['frame'])/span
            return a['focus_distance_m']+(b['focus_distance_m']-a['focus_distance_m'])*t
    return keyframes[-1]['focus_distance_m']


def parse_look_cards(text):
    """Normalize a look-card map to {subject_id:{'image':abs path}}.

    Shape: {"CH01": {"image": "/abs/path/character_sheet.png"}}. The card is
    a camera-facing flat image plane sized from the subject box: it shows the
    approved look inside the framing, and nothing else. Returns (map, errors).
    """
    errors=[];out={}
    try:data=json.loads(text)
    except ValueError as e:return None,['invalid JSON: '+str(e)]
    if not isinstance(data,dict):return None,['look-card map must be an object of subject ids']
    for subject,row in data.items():
        if isinstance(row,str):row={'image':row}
        if not isinstance(row,dict):errors.append(f'{subject}: look-card entry must be an object or path');continue
        image=row.get('image') or row.get('path')
        if not isinstance(image,str) or not image.strip():errors.append(f'{subject}: look-card image path required');continue
        path=Path(image).expanduser()
        if not path.is_file():errors.append(f'{subject}: look-card image not found: {image}');continue
        out[subject]={'image':str(path.resolve())}
    if not out and not errors:errors.append('look-card map selects no subjects')
    return out,errors


def engine_candidates(requested):
    """Ordered render-engine ids to try for a requested engine.

    The engine enum a build exposes depends on enabled add-ons, so the
    adapter tries the candidates instead of trusting one enum snapshot.
    """
    return ['CYCLES'] if requested=='cycles' else ['BLENDER_EEVEE_NEXT','BLENDER_EEVEE']


def arguments():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--spec',required=True);p.add_argument('--output',required=True)
    p.add_argument('--mode',choices=['smoke','stills','sequence'],default='stills')
    p.add_argument('--render-map',help='stills-mode JSON or @file: {shot:[frame|{frame,panel}]} or {shot:{panel:frame}} of local 0-based frames to render')
    p.add_argument('--proxy',choices=['box','figure'],default='box',
                   help='subject proxy: box (default, abstract) or figure (stylized clay body for readable framing/headroom/occlusion); neither is final character or acting validation')
    p.add_argument('--engine',choices=['cycles','eevee'],default='cycles',
                   help='render engine for the preview frames; cycles is the reference look, eevee is a faster preview and is not a quality claim')
    p.add_argument('--focus-map',help='JSON file: {shot_id: {"f_number": 2.8, "keyframes": [{"frame": 0, "focus_distance_m": 2.0}]}} for focus/rack-focus previews')
    p.add_argument('--look-cards',help='JSON file: {subject_id: {"image": "/abs/path.png"}} to show the approved look as a camera-facing card inside the framing')
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
    focus_map={}
    if args.focus_map:
        path=Path(args.focus_map).expanduser()
        if not path.is_file():raise SystemExit(json.dumps({'valid':False,'errors':['--focus-map file not found: '+str(path)]},ensure_ascii=False))
        focus_map,focus_errors=parse_focus_map(path.read_text(encoding='utf-8'))
        if focus_errors:raise SystemExit(json.dumps({'valid':False,'errors':['--focus-map: '+e for e in focus_errors]},ensure_ascii=False))
        shot_ids={s['id'] for s in spec['shots']}
        unknown=[k for k in focus_map if k not in shot_ids]
        if unknown:raise SystemExit(json.dumps({'valid':False,'errors':['--focus-map: not a spec shot: '+k for k in unknown]},ensure_ascii=False))
        for shot_id,row in focus_map.items():
            shot=[s for s in spec['shots'] if s['id']==shot_id][0];n=shot['duration_frames']
            for k in row['keyframes']:
                if not 0<=k['frame']<n:raise SystemExit(json.dumps({'valid':False,'errors':[f'--focus-map: {shot_id} frame {k["frame"]} outside local 0..{n-1}']},ensure_ascii=False))
    look_cards={}
    if args.look_cards:
        path=Path(args.look_cards).expanduser()
        if not path.is_file():raise SystemExit(json.dumps({'valid':False,'errors':['--look-cards file not found: '+str(path)]},ensure_ascii=False))
        look_cards,card_errors=parse_look_cards(path.read_text(encoding='utf-8'))
        if card_errors:raise SystemExit(json.dumps({'valid':False,'errors':['--look-cards: '+e for e in card_errors]},ensure_ascii=False))
        subject_ids={s['id'] for s in spec['subjects']}
        unknown=[k for k in look_cards if k not in subject_ids]
        if unknown:raise SystemExit(json.dumps({'valid':False,'errors':['--look-cards: not a spec subject: '+k for k in unknown]},ensure_ascii=False))
    try:import bpy
    except ImportError:raise SystemExit('Blender bpy unavailable. Run with Blender --background --factory-startup --python, or a working bpy module.')
    from mathutils import Vector,Quaternion
    from bpy_extras.object_utils import world_to_camera_view
    available=[i.identifier for i in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
    engine_id=None
    out=Path(args.output).resolve()
    if out.exists():raise SystemExit('Output already exists. Choose a new folder; nothing was overwritten.')
    out.mkdir(parents=True)
    smoke=args.mode=='smoke'
    scope_text=('stylized figure proxy previs: readable framing, headroom and silhouette overlap only; '
                'no face direction, pose, articulation, likeness or hand/object contact validation; no final lighting or acting validation'
                if args.proxy=='figure' else
                'box proxy previs; no final character/lighting/acting validation')
    if look_cards:
        scope_text+='; look cards show the approved look as camera-facing flat images and prove no depth, occlusion order, pose or contact'
    if focus_map:
        scope_text+='; focus preview comes from an adapter-local focus map, not from the camera-spatial-1.0 spec, and proves no real lens calibration'
    manifest={'project_id':spec['project_id'],'blender_version':bpy.app.version_string,'engine':args.engine,'mode':args.mode,'status':'running','files':[],'rendered':{},
              'proxy_mode':args.proxy,
              'look_cards':{k:v['image'] for k,v in look_cards.items()},
              'focus_map':{k:{'f_number':v['f_number'],'keyframes':v['keyframes']} for k,v in focus_map.items()},
              'camera_spec':{'version':spec.get('version'),'artifact_id':spec.get('artifact_id'),'sha256':hashlib.sha256(spec_bytes).hexdigest()},
              'shot_links':{s['id']:{'scene_id':s.get('scene_id'),'beat_ids':s.get('beat_ids',[])} for s in (spec['shots'][:1] if smoke else spec['shots'])},
              'scope':scope_text}
    if smoke:
        manifest['scope']=scope_text+'; smoke: first shot, one low-resolution frame; narrow pipeline check only, not whole-spec render verification'
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
        def look_card(scene,name,row,image_path):
            """Camera-facing flat card showing the approved look for a subject.

            The card is sized from the subject box and textured with the given
            image. It shows the approved look inside the framing; it is not a
            3D body, so it proves no depth, occlusion order, pose or contact.
            """
            w,d,h=row['size_m']
            vertices=[(-w/2,-h/2,0),(w/2,-h/2,0),(w/2,h/2,0),(-w/2,h/2,0)]
            faces=[(0,1,2,3)]
            me=bpy.data.meshes.new(name+'_card');me.from_pydata(vertices,[],faces);me.validate()
            uv=me.uv_layers.new(name='UVMap')
            corners=[(0.0,0.0),(1.0,0.0),(1.0,1.0),(0.0,1.0)]
            for loop in me.loops:uv.data[loop.index].uv=corners[loop.vertex_index]
            ob=bpy.data.objects.new(me.name,me);scene.collection.objects.link(ob)
            img=bpy.data.images.load(image_path,check_existing=True)
            mat=bpy.data.materials.new(me.name+'_mat');mat.use_nodes=True
            nodes=mat.node_tree.nodes;links=mat.node_tree.links
            bsdf=nodes.get('Principled BSDF')
            tex=nodes.new('ShaderNodeTexImage');tex.image=img;tex.interpolation='Linear'
            links.new(tex.outputs['Color'],bsdf.inputs['Base Color'])
            ob.data.materials.append(mat)
            return ob
        def orient(ob,target,roll=0):
            ob.rotation_mode='QUATERNION'
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
            if engine_id is None:
                for candidate in engine_candidates(args.engine):
                    try:
                        scene.render.engine=candidate;engine_id=candidate;break
                    except TypeError:continue
                if engine_id is None:raise SystemExit(json.dumps({'valid':False,'errors':['requested render engine is not available in this Blender build: '+args.engine]},ensure_ascii=False))
            else:
                scene.render.engine=engine_id
            manifest['engine']=engine_id+(' CPU' if engine_id=='CYCLES' else '')
            scene.cycles.device='CPU';scene.cycles.samples=8
            if engine_id!='CYCLES' and hasattr(scene,'eevee') and hasattr(scene.eevee,'taa_render_samples'):
                scene.eevee.taa_render_samples=16
            if hasattr(scene.render,'use_motion_blur'):scene.render.use_motion_blur=False
            scene.render.image_settings.file_format='PNG';scene.frame_start=1;scene.frame_end=1 if smoke else shot['duration_frames']
            scene.world=bpy.data.worlds.new(shot['id']+'_world');scene.world.use_nodes=True
            scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.12,.12,1)
            scene.world.node_tree.nodes['Background'].inputs[1].default_value=.4
            objects={};parts={}
            for rid,row in subjects.items():
                base=shot['id']+'_'+rid;color=tuple(row.get('color_rgba',[.25,.5,.75,1]))
                if look_cards.get(rid):
                    objects[rid]=look_card(scene,base,row,look_cards[rid]['image'])
                elif args.proxy=='figure':
                    parent=bpy.data.objects.new(base+'_root',None);parent.empty_display_size=.2;scene.collection.objects.link(parent)
                    parent.location=(row['position'][0],row['position'][1],row['position'][2])
                    made=[]
                    for part in figure_proxy_parts(row['size_m']):
                        verts,faces=sphere_mesh()
                        me=bpy.data.meshes.new(base+'_'+part['name']);me.from_pydata(verts,[],faces);me.validate()
                        ob=bpy.data.objects.new(me.name,me);scene.collection.objects.link(ob)
                        ob.scale=(part['radius']*part['scale'][0],part['radius']*part['scale'][1],part['radius']*part['scale'][2])
                        ob.location=(0.0,0.0,part['z']);ob.parent=parent
                        ob.data.materials.append(material(ob.name,color))
                        for poly in me.polygons:poly.use_smooth=True
                        made.append(ob)
                    objects[rid]=parent;parts[rid]=made
                else:
                    objects[rid]=box(scene,base,row['position'],row['size_m'],color)
            for ob in spec['obstacles']:box(scene,shot['id']+'_'+ob['id'],ob['position'],ob['size_m'],tuple(ob.get('color_rgba',[.35,.35,.35,1])))
            box(scene,shot['id']+'_floor',[0,0,-.1],[20,20,.1],(.55,.55,.55,1))
            light=bpy.data.lights.new(shot['id']+'_key','AREA');light.energy=500;light.size=5
            lamp=bpy.data.objects.new(light.name,light);scene.collection.objects.link(lamp);lamp.location=(2,-3,6);orient(lamp,(0,0,0))
            data=bpy.data.cameras.new(shot['id']+'_camera');cam=bpy.data.objects.new(data.name,data);scene.collection.objects.link(cam);scene.camera=cam
            c=shot['camera'];data.type='PERSP';data.sensor_fit='HORIZONTAL';data.sensor_width=c['sensor_width_mm'];data.sensor_height=c['sensor_width_mm']*spec['resolution'][1]/spec['resolution'][0]
            data.clip_start=c['clip_start_m'];data.clip_end=c['clip_end_m'];data.shift_x=data.shift_y=0;data.dof.use_dof=False
            focus=focus_map.get(shot['id'])
            if focus:
                data.dof.use_dof=True
                if focus.get('f_number'):data.dof.aperture_fstop=focus['f_number']
            frames=range(1) if smoke else range(shot['duration_frames'])
            for f in frames:
                k=sample(c['keyframes'],f,c['interpolation'],c['lens_mm']);positions=subject_positions(spec,shot,f)
                cam.location=k['position'];orient(cam,k['target'],c.get('roll_deg',0));data.lens=k['lens_mm']
                cam.keyframe_insert('location',frame=f+1);cam.keyframe_insert('rotation_quaternion',frame=f+1);data.keyframe_insert('lens',frame=f+1)
                if focus:
                    data.dof.focus_distance=focus_distance_at(focus['keyframes'],f)
                    data.dof.keyframe_insert('focus_distance',frame=f+1)
                    if focus.get('f_number'):data.dof.keyframe_insert('aperture_fstop',frame=f+1)
                for rid,ob in objects.items():
                    pos=positions[rid]
                    if args.proxy=='figure' and not look_cards.get(rid):ob.location=(pos[0],pos[1],pos[2])
                    else:ob.location=(pos[0],pos[1],pos[2]+subjects[rid]['size_m'][2]/2)
                    if look_cards.get(rid):
                        ob.rotation_mode='QUATERNION'
                        q=(Vector(cam.location)-Vector(ob.location)).to_track_quat('Z','Y')
                        if ob.rotation_quaternion.dot(q)<0:q.negate()
                        ob.rotation_quaternion=q
                        ob.keyframe_insert('rotation_quaternion',frame=f+1)
                    ob.keyframe_insert('location',frame=f+1)
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
                        owned=(not hit) or first==objects[rid] or first.name in {p.name for p in parts.get(rid,[])}
                        visible=ndc.z>data.clip_start and ndc.z<data.clip_end and 0<=ndc.x<=1 and 0<=ndc.y<=1 and owned
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
