#!/usr/bin/env python3
"""Blender-only adapter. Creates fresh proxy scenes; run in an isolated process."""
import argparse,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from spatial_spec import validate,analyze,sample,subject_positions


def arguments():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--spec',required=True);p.add_argument('--output',required=True)
    p.add_argument('--mode',choices=['smoke','stills','sequence'],default='stills')
    return p.parse_args(argv)


def main():
    args=arguments()
    try:import bpy
    except ImportError:raise SystemExit('Blender bpy unavailable. Run with Blender --background --factory-startup --python, or a working bpy module.')
    from mathutils import Vector,Quaternion
    from bpy_extras.object_utils import world_to_camera_view
    spec=json.loads(Path(args.spec).read_text());errors=validate(spec)
    if errors:raise SystemExit(json.dumps({'valid':False,'errors':errors},ensure_ascii=False))
    out=Path(args.output).resolve()
    if out.exists():raise SystemExit('Output already exists. Choose a new folder; nothing was overwritten.')
    out.mkdir(parents=True)
    manifest={'project_id':spec['project_id'],'blender_version':bpy.app.version_string,'engine':'CYCLES CPU','mode':args.mode,'status':'running','files':[],'scope':'box proxy previs; no final character/lighting/acting validation'}
    def write_manifest(): (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    write_manifest()
    try:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        numerical=analyze(spec);(out/'numerical-analysis.json').write_text(json.dumps(numerical,ensure_ascii=False,indent=2)+'\n')
        def material(name,color):
            m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True
            node=m.node_tree.nodes.get('Principled BSDF')
            if node:node.inputs['Base Color'].default_value=color
            return m
        def box(scene,name,pos,size,color):
            vertices=[(x*size[0]/2,y*size[1]/2,z*size[2]/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
            faces=[(0,2,6,4),(1,5,7,3),(0,4,5,1),(2,3,7,6),(0,1,3,2),(4,6,7,5)]
            mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
            ob=bpy.data.objects.new(name,mesh);scene.collection.objects.link(ob)
            ob.location=(pos[0],pos[1],pos[2]+size[2]/2);ob.data.materials.append(material(name,color));return ob
        def orient(ob,target,roll=0):
            q=(Vector(target)-ob.location).to_track_quat('-Z','Y')
            q=q@Quaternion((0,0,1),math.radians(roll))
            ob.rotation_mode='QUATERNION'
            if ob.rotation_quaternion.dot(q)<0:q.negate()
            ob.rotation_quaternion=q
        inspections=[];subjects={x['id']:x for x in spec['subjects']}
        scenes=[]
        for shot in spec['shots']:
            scene=bpy.data.scenes.new(shot['id']);scenes.append(scene)
            if bpy.context.window:bpy.context.window.scene=scene
            scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
            scene.render.resolution_x,scene.render.resolution_y=spec['resolution'];scene.render.resolution_percentage=100
            scene.render.pixel_aspect_x=scene.render.pixel_aspect_y=1;scene.render.fps=spec['fps'];scene.render.fps_base=1
            scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8
            if hasattr(scene.render,'use_motion_blur'):scene.render.use_motion_blur=False
            scene.render.image_settings.file_format='PNG';scene.frame_start=1;scene.frame_end=shot['duration_frames']
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
            for f in range(shot['duration_frames']):
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
            for f in range(shot['duration_frames']):
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
            inspections.append({'shot_id':shot['id'],'checks':checks})
            folder=out/shot['id'];folder.mkdir()
            frames=range(shot['duration_frames']) if args.mode=='sequence' else sorted({0,shot['duration_frames']//2,shot['duration_frames']-1})
            if args.mode=='smoke':frames=[0] if shot is spec['shots'][0] else []
            for f in frames:
                scene.frame_set(f+1);scene.render.filepath=str(folder/f'frame_{f+1:06d}.png')
                bpy.ops.render.render(write_still=True,scene=scene.name)
                path=Path(scene.render.filepath)
                if not path.is_file():raise RuntimeError('Render did not create '+str(path))
                manifest['files'].append(str(path.relative_to(out)))
        if bpy.context.window:bpy.context.window.scene=scenes[0]
        bpy.ops.wm.save_as_mainfile(filepath=str(out/'previs.blend'),check_existing=False)
        if not (out/'previs.blend').is_file():raise RuntimeError('Blend save missing')
        (out/'blender-inspection.json').write_text(json.dumps({'scope':'proxy point projection and first ray hit, all integer frames','shots':inspections},ensure_ascii=False,indent=2)+'\n')
        manifest['files']+=['previs.blend','numerical-analysis.json','blender-inspection.json'];manifest['status']='generated';write_manifest()
    except Exception as e:
        manifest['status']='failed';manifest['error']=str(e);write_manifest();raise
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
