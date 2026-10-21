"""Synthetic local CLI exercise; no model invocation, media, or approval claims."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
p = dict(schema_version='1.1', project_id='F5-synthetic-chef', version='1', aspect_ratio='16:9', target_duration_s=4, fps=24, audio_mode='no_audio', scenes=[dict(id='S01', purpose='plate attention then service gaze')], characters=[dict(id='CH01', locked_traits={'apron':'charcoal','hair':'short dark','plate':'left hand throughout'})], claims=[], artifacts=[dict(id='SYN01',type='synopsis',version='1',status='draft',dependencies=[],dependency_versions={}),dict(id='CAM01',type='camera_spec',version='1',status='draft',dependencies=[],dependency_versions={}),dict(id='BOARD01',type='storyboard',version='1',status='draft',dependencies=['SYN01','CAM01'],dependency_versions={'SYN01':'1','CAM01':'1'})], asset_registry=[dict(id=x,kind='image',version='1',status='planned') for x in ['IM01','IM02']],audio_cues=[],captions=[],issues=[],delivery_spec={},delivery_checks=[])
p['shots']=[dict(id='SH01',scene_id='S01',character_ids=['CH01'],asset_ids=[],start_s=0,end_s=4,source_duration_s=4,source_duration_status='estimated',purpose='attention shifts from dish to opening',start_state='plate level left hand; eyes down',end_state='same plate left hand; gaze at opening',beat_ids=['B01','B02'],camera=dict(shot_size='medium',angle='eye-level impression',framing='face torso and plate; plate then eyes; no crop',movement='static',start='(0,-2.5,1.5) target (0,.35,1.25), 50mm FF',end='unchanged; speed 0'),spatial=dict(mode='numeric',artifact_id='CAM01'),vfx=dict(enabled=False,description='gaze-only scene; no compositing effect'),speech=[],audio_cue_ids=[])]
p['storyboard']=dict(synopsis_artifact_id='SYN01',beats=[dict(id='B01',synopsis_locator='SYN01 v1 P1/S1',event='Mira holds plated dish and looks down',emotion='attentive'),dict(id='B02',synopsis_locator='SYN01 v1 P2/S1',event='Mira raises gaze without moving plate',emotion='ready attention')],panels=[])
for i, beat, frame, role, action in [(1,'B01',0,'start','Mira looks down at completed dish; level plate left hand'),(2,'B02',95/24,'end','Mira looks toward service opening; plate unchanged in left hand')]:
    p['storyboard']['panels'].append(dict(id=f'P{i:02}',shot_id='SH01',frame_time_s=frame,role=role,beat_ids=[beat],visible_character_ids=['CH01'],audio_cue_ids=[],speech_ids=[],visual_action=action,reveals='dish and gaze direction',withholds='no later delivery depicted',continuity='charcoal apron; short dark hair; right hand empty; plate same position and owner',image_asset_id=f'IM{i:02}'))
path=OUT/'chef-board.json'
path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cmd=[sys.executable,str(ROOT/'video-production-assets/scripts/validate_storyboard.py'),str(path)]
r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
record=dict(command=cmd,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr,input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),scope='real CLI on synthetic structured plan; not full prose, pixels, rights, approvals, voice or camera-fit validation')
(OUT/'validator-result.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Boundary: a missing numeric spatial artifact is a structural error, not a pass.
p['shots'][0]['spatial'].pop('artifact_id')
bad=OUT/'chef-board-missing-spatial.json'
bad.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r2=subprocess.run([*cmd[:-1],str(bad)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
(OUT/'validator-boundary-result.json').write_text(json.dumps(dict(command=[*cmd[:-1],str(bad)],exit_code=r2.returncode,stdout=r2.stdout,stderr=r2.stderr),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
identities=[]
for name, file in [('Hooks','E:/Book/06_Book/originals/콘텐츠_제작/md/Acting for Animators (Ed Hooks) (z-library.sk, 1lib.sk, z-lib.sk).md'),('Hu','E:/Book/06_Book/콘티_스토리보드/md/스토리보드 마스터하기 - 캐롤라인 후.md')]:
    b=Path(file).read_bytes()
    identities.append(dict(name=name,path=file,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(OUT/'source-identities.json').write_text(json.dumps(identities,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
print(json.dumps(dict(boundary_exit=r2.returncode,boundary_stdout=r2.stdout),ensure_ascii=False))
if r.returncode or r2.returncode == 0:
    raise SystemExit('unexpected validator outcome')
