"""Contract regression tests; fixture bytes are NOT a rendered media sample."""
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from validate_project import validate


def project():
    return {'schema_version':'1.1','project_id':'test','version':'1','aspect_ratio':'16:9','target_duration_s':2,'fps':24,'audio_mode':'no_audio',
            'scenes':[{'id':'S01','purpose':'show sum'}],'characters':[],
            'shots':[{'id':'SH01','scene_id':'S01','character_ids':[],'start_s':0,'end_s':2,'source_duration_s':2,'source_duration_status':'estimated','purpose':'show','start_state':'2 + 3','end_state':'5'}],
            'claims':[], 'artifacts':[{'id':'A01','type':'plan','version':'1','status':'draft','dependencies':[],'dependency_versions':{}}],
            'asset_registry':[],'audio_cues':[],'captions':[],'issues':[],'delivery_spec':{},'delivery_checks':[]}


class ContractTests(unittest.TestCase):
    def test_minimal_characterless_plan(self): self.assertEqual(validate(project()),[])
    def test_known_rejections(self):
        cases=[
            ('ratio',lambda p:p.update(aspect_ratio='wrong')),
            ('fps',lambda p:p.update(fps=True)),
            ('scene purpose',lambda p:p['scenes'][0].pop('purpose')),
            ('traits',lambda p:p['characters'].append({'id':'CH01'})),
            ('artifacts',lambda p:p.update(artifacts=[])),
            ('approval',lambda p:p['artifacts'][0].update(status='approved')),
            ('approval type',lambda p:p['artifacts'][0].update(status='approved',approval=True)),
            ('gap',lambda p:p['shots'][0].update(start_s=1)),
            ('overlap',lambda p:p['shots'].append(dict(p['shots'][0],id='SH02'))),
            ('duplicate',lambda p:p['shots'].append(copy.deepcopy(p['shots'][0]))),
            ('frame boundary',lambda p:p['shots'][0].update(start_s=.01)),
            ('duration',lambda p:p.update(target_duration_s=3)),
            ('short trim',lambda p:p['shots'][0].update(source_in_s=1)),
            ('missing scene',lambda p:p['shots'][0].update(scene_id='S99')),
            ('malformed ref',lambda p:p['shots'][0].update(scene_id=[])),
            ('missing char array',lambda p:p['shots'][0].pop('character_ids')),
            ('missing asset',lambda p:p['shots'][0].update(asset_ids=['AS99'])),
            ('unknown duration state',lambda p:p['shots'][0].update(source_duration_status='verified')),
            ('sound in silence',lambda p:p['audio_cues'].append({'id':'AU01','start_s':0,'end_s':1,'layer':'music'})),
            ('caption interval',lambda p:p['captions'].append({'id':'CAP01','start_s':1,'end_s':3,'text':'5'})),
            ('claim source',lambda p:p['claims'].append({'id':'CL01','statement':'x','kind':'fact','status':'verified'})),
            ('claim label',lambda p:p['claims'].append({'id':'CL01','statement':'x','kind':'fact','status':'fiction'})),
            ('cycle',lambda p:p['artifacts'][0].update(dependencies=['A01'],dependency_versions={'A01':'1'})),
            ('version',lambda p:p['artifacts'].append({'id':'A02','type':'shots','version':'1','status':'draft','dependencies':['A01'],'dependency_versions':{'A01':'0'}})),
            ('unversioned dependency',lambda p:p['artifacts'].append({'id':'A02','type':'shots','version':'1','status':'draft','dependencies':['A01'],'dependency_versions':{}})),
        ]
        for name,change in cases:
            with self.subTest(name=name):
                p=project();change(p);self.assertTrue(validate(p),name)
    def test_slow_motion_source_duration(self):
        p=project();p['shots'][0].update(source_duration_s=1,playback_rate=.5)
        self.assertEqual(validate(p),[])
    def test_good_approval(self):
        p=project();p['artifacts'][0].update(status='approved',approval={'by':'test user','at':'2026-10-02','evidence':'test approval record'})
        self.assertEqual(validate(p),[])
    def test_no_dialogue_music_allowed(self):
        p=project();p['audio_mode']='no_dialogue';p['audio_cues']=[{'id':'AU01','start_s':0,'end_s':2,'layer':'music'}]
        self.assertEqual(validate(p),[])
        p['audio_cues'][0]['layer']='voiceover';self.assertTrue(validate(p))
    def test_silent_plan_is_not_delivery(self): self.assertTrue(validate(project(),'delivery'))
    def test_local_asset_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp,'fixture.bin');path.write_bytes(b'fixture, not media')
            p=project();p['asset_registry']=[{'id':'AS01','kind':'fixture','version':'1','status':'available','path':'fixture.bin','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}]
            self.assertEqual(validate(p,base_dir=temp),[])
            path.write_bytes(b'changed');self.assertTrue(validate(p,base_dir=temp))
            path.unlink();self.assertTrue(validate(p,base_dir=temp))
    def test_delivery_manifest_structure(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp,'fixture.bin');path.write_bytes(b'contract test only')
            p=project();p['shots'][0]['source_duration_status']='measured'
            p['asset_registry']=[{'id':'AS01','kind':'test-final','version':'1','status':'verified','path':'fixture.bin','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}]
            p['delivery_spec']={'destination':'test','width':1920,'height':1080,'container':'test','video_codec':'test','caption_mode':'none','final_asset_id':'AS01'}
            p['delivery_checks']=[{'id':c,'category':c,'status':'pass','evidence':'synthetic contract record; no actual media inspection'} for c in ['playback','timing','visual','audio','captions','continuity','claims']]
            self.assertEqual(validate(p,'delivery',temp),[])
            q=copy.deepcopy(p);q['issues']=[{'id':'Q01','severity':'blocker','status':'open'}];self.assertTrue(validate(q,'delivery',temp))
            q=copy.deepcopy(p);q['delivery_checks'][0].update(status='unverified');self.assertTrue(validate(q,'delivery',temp))
            q=copy.deepcopy(p);q['delivery_spec']['width']=100;self.assertTrue(validate(q,'delivery',temp))
            q=copy.deepcopy(p);q['delivery_spec']['caption_mode']='sidecar';self.assertTrue(validate(q,'delivery',temp))
    def test_generation_attempts_contract(self):
        p=project()
        p['shots'][0]['retry_budget']=3
        p['asset_registry']=[{'id':'AS01','kind':'clip','version':'1','status':'available','path':'actual-output.mp4'}]
        p['generation_attempts']=[
            {'id':'GA01','shot_id':'SH01','attempt':1,'route':'t2v','changes':['initial'],'observed_failures':['hand mutation'],'preserve':['framing'],'result':'reject','failure_class':'motion'},
            {'id':'GA02','shot_id':'SH01','attempt':2,'route':'t2v','changes':['simplified action'],'result':'accept','result_asset_id':'AS01'}]
        self.assertEqual(validate(p),[])
    def test_generation_attempts_rejections(self):
        cases=[
            ('bad budget',lambda p:p['shots'][0].update(retry_budget=-1)),
            ('dup attempt',lambda p:p['generation_attempts'].append(dict(p['generation_attempts'][0],id='GA02'))),
            ('bad result',lambda p:p['generation_attempts'][0].update(result='maybe')),
            ('bad class',lambda p:p['generation_attempts'][0].update(failure_class='vibes')),
            ('accept sans asset',lambda p:p['generation_attempts'][0].update(result='accept')),
            ('missing shot',lambda p:p['generation_attempts'][0].update(shot_id='SH99')),
            ('over budget',lambda p:(p['shots'][0].update(retry_budget=0),p['generation_attempts'][0].update(attempt=2))),
        ]
        for name,change in cases:
            with self.subTest(name=name):
                p=project()
                p['generation_attempts']=[{'id':'GA01','shot_id':'SH01','attempt':1,'route':'t2v','changes':[],'result':'reject'}]
                change(p);self.assertTrue(validate(p),name)
    def test_asset_provenance_fields(self):
        p=project()
        p['asset_registry']=[{'id':'AS01','kind':'reference','version':'1','status':'planned','entity_type':'character','entity_id':'CH01','authority':'authoritative','source_asset_ids':[],'provider':'verified-provider','model':'verified-model','workflow':'w'}]
        self.assertEqual(validate(p),[])
        p['asset_registry'][0]['entity_type']='soul';self.assertTrue(validate(p))
    def test_retry_budget_counts_retries_after_initial_attempt(self):
        p=project()
        p['shots'][0]['retry_budget']=0
        p['generation_attempts']=[{'id':'GA01','shot_id':'SH01','attempt':1,'route':'t2v','result':'reject'}]
        self.assertEqual(validate(p),[])
        p['generation_attempts'].append({'id':'GA02','shot_id':'SH01','attempt':2,'route':'t2v','result':'reject'})
        self.assertTrue(any('retry_budget' in e for e in validate(p)))
        p['shots'][0]['retry_budget']=1
        self.assertEqual(validate(p),[])
        p['generation_attempts'].append({'id':'GA03','shot_id':'SH01','attempt':3,'route':'t2v','result':'reject'})
        self.assertTrue(any('retry_budget' in e for e in validate(p)))
    def test_malformed_attempt_shot_reference_returns_validation_error(self):
        for sid in ([],{}):
            with self.subTest(shot_id=sid):
                p=project()
                p['generation_attempts']=[{'id':'GA01','shot_id':sid,'attempt':1,'route':'t2v','result':'reject'}]
                self.assertTrue(any('shots reference' in e for e in validate(p)))
    def test_accepted_attempt_requires_available_result(self):
        p=project()
        p['asset_registry']=[{'id':'AS01','kind':'clip','version':'1','status':'planned'}]
        p['generation_attempts']=[{'id':'GA01','shot_id':'SH01','attempt':1,'route':'t2v','result':'accept','result_asset_id':'AS01'}]
        self.assertTrue(any('accepted attempt' in e for e in validate(p)))
        p['asset_registry'][0].update(status='available',path='actual-output.mp4')
        self.assertEqual(validate(p),[])
    def test_cli_reads_utf8_project_independent_of_system_locale(self):
        with tempfile.TemporaryDirectory() as temp:
            p=project()
            p['project_id']='한국어 제작 프로젝트'
            path=Path(temp,'project.json')
            path.write_text(json.dumps(p,ensure_ascii=False),encoding='utf-8')
            env=dict(os.environ,PYTHONUTF8='0',PYTHONCOERCECLOCALE='0',LC_ALL='C')
            result=subprocess.run([sys.executable,str(Path(__file__).with_name('validate_project.py')),str(path)],
                                  env=env,capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertTrue(json.loads(result.stdout)['valid'])

if __name__=='__main__': unittest.main()
