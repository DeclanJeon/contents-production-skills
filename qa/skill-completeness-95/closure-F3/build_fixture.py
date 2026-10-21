"""Owned synthetic fixture; ground truth is kept outside analysis media."""
import bpy
import json
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

root = Path(__file__).resolve().parent
out = root / 'media'
out.mkdir(exist_ok=False)
bpy.ops.wm.read_factory_settings(use_empty=True)
s = bpy.context.scene
s.render.engine = 'BLENDER_WORKBENCH'
s.display.shading.light = 'STUDIO'
s.display.shading.color_type = 'MATERIAL'
s.display.shading.show_shadows = False
s.render.resolution_x = 320
s.render.resolution_y = 180
s.render.resolution_percentage = 100
s.render.fps = 12
s.frame_start = 1
s.frame_end = 24
objects = []
for name, loc, size, color in [('near',(-1,0,1),(.7,.7,2),(.9,.25,.1,1)),('middle',(0,4,1),(1,1,2),(.2,.8,.3,1)),('far',(1,9,1),(1,1,2),(.15,.35,.95,1))]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = size
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    o.data.materials.append(mat)
    objects.append(o)
for x in range(-6,7,2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x,12,1.5))
    bpy.context.object.dimensions = (.08,.1,5)
bpy.ops.mesh.primitive_plane_add(size=60)
bpy.ops.object.camera_add(location=(0,-8,2.5))
cam = bpy.context.object
cam.rotation_euler = (Vector((0,4,1))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.lens = 32
cam.data.sensor_width = 36
cam.data.sensor_fit = 'HORIZONTAL'
s.camera = cam
records = []
for clip in ['A','B']:
    folder = out / clip
    folder.mkdir()
    for f in range(24):
        t = f/23
        cam.location = (0,-8+3*t,2.5) if clip == 'A' else (0,-8,2.5)
        cam.data.lens = 32 if clip == 'A' else 32*(1+.6*t)
        s.frame_set(f+1)
        s.render.filepath = str(folder / f'frame_{f:03d}.png')
        bpy.ops.render.render(write_still=True)
        points = {}
        for o in objects:
            p = world_to_camera_view(s,cam,o.location)
            top = world_to_camera_view(s,cam,o.location+Vector((0,0,1)))
            bottom = world_to_camera_view(s,cam,o.location-Vector((0,0,1)))
            points[o.name] = {'center_uv':list(p)[:2], 'height_uv':abs(top.y-bottom.y)}
        records.append({'clip':clip,'frame_zero':f,'pts_seconds':f/12,'camera_position':list(cam.location),'lens_mm':cam.data.lens,'points':points})
bpy.ops.wm.save_as_mainfile(filepath=str(root/'fixture.blend'))
(root/'ground-truth.json').write_text(json.dumps({'blender':bpy.app.version_string,'fps':12,'frames_per_clip':24,'duration_seconds':2,'A':'camera translation along world +Y, constant orientation and 32 mm lens','B':'fixed camera position/orientation, lens 32 to 51.2 mm','subjects':'all objects static throughout both clips','focus':'DOF disabled; no focus quality claim','samples':records},indent=2),encoding='utf-8')
print('F3_FIXTURE_COMPLETE', bpy.app.version_string, len(records))
