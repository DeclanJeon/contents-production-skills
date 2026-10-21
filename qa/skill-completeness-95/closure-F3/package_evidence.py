import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
root = Path(__file__).resolve().parent
truth = json.loads((root/'ground-truth.json').read_text(encoding='utf-8'))
observations = {}
for clip in ['A','B']:
    folder = root/'media'/clip
    command = ['ffmpeg','-hide_banner','-loglevel','error','-n','-framerate','12','-i',str(folder/'frame_%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p',str(root/'media'/f'{clip}.mp4')]
    subprocess.run(command,check=True)
    probe = subprocess.run(['ffprobe','-v','error','-count_frames','-show_entries','stream=width,height,r_frame_rate,nb_read_frames,duration','-of','json',str(root/'media'/f'{clip}.mp4')],check=True,capture_output=True,text=True)
    (root/f'{clip}-probe.json').write_text(probe.stdout,encoding='utf-8')
    sheet = Image.new('RGB',(960,420),'white')
    draw = ImageDraw.Draw(sheet)
    for index,frame in enumerate([0,4,9,14,19,23]):
        image = Image.open(folder/f'frame_{frame:03d}.png').convert('RGB')
        x,y = (index%3)*320,(index//3)*210
        sheet.paste(image,(x,y))
        draw.text((x+4,y+184),f'{clip} | frame {frame} | {frame/12:.4f} s',fill='black')
    sheet.save(root/'media'/f'{clip}-contact.png')
    samples = [r for r in truth['samples'] if r['clip']==clip]
    observations[clip] = {name:{'first_height_uv':samples[0]['points'][name]['height_uv'],'last_height_uv':samples[-1]['points'][name]['height_uv'],'growth':samples[-1]['points'][name]['height_uv']/samples[0]['points'][name]['height_uv']} for name in ['near','middle','far']}
base = Path('E:/Book/06_Book/originals/콘텐츠_제작/md')
source_names = ['Film Directing Shot by Shot Visualizing from Concept to Screen (Steven D. Katz) (z-library.sk, 1lib.sk, z-lib.sk).md','The Visual Story Creating the Visual Structure of Film, TV, and Digital Media Third Edition (Bruce Block) (z-library.sk, 1lib.sk, z-lib.sk).md']
identities=[]
for name in source_names:
    path=base/name
    data=path.read_bytes()
    identities.append({'path':path.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(root/'source-identities.json').write_text(json.dumps(identities,indent=2),encoding='utf-8')
(root/'depth-measurements.json').write_text(json.dumps(observations,indent=2),encoding='utf-8')
(root/'media'/'timing.json').write_text(json.dumps({'fps':12,'timebase':'CFR; zero-based frame index / 12','clips':{'A':{'frames':24,'duration_seconds':2},'B':{'frames':24,'duration_seconds':2}},'sampled_frames':[0,4,9,14,19,23],'last_frame_pts_seconds':23/12},indent=2),encoding='utf-8')
print(json.dumps({'sources':identities,'depth':observations},indent=2))
