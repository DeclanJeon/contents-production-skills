import copy,json,math,unittest
from pathlib import Path
import os,subprocess,sys,tempfile
from spatial_spec import validate,analyze,project,sample,reconcile_project

def spec():return json.loads((Path(__file__).parent.parent/'assets/camera-spec-example.json').read_text())
class SpatialTests(unittest.TestCase):
    def test_example(self):
        p=spec();self.assertEqual(validate(p),[]);r=analyze(p);self.assertTrue(r['valid']);self.assertEqual(r['total_duration_s'],4)
        self.assertEqual(sum(len(s['samples']) for s in r['shots']),96)
        self.assertFalse(any(s['warnings'] for s in r['shots']))
        self.assertAlmostEqual(r['shots'][0]['samples'][0]['pair_distances_m']['CH01/CH02'],1.6)
    def test_projection_and_perspective(self):
        c={'position':[0,-5,1],'target':[0,0,1],'lens_mm':35}
        x,y,z=project([0,0,1],c,640,360,36);self.assertEqual((x,y,z),(.5,.5,5))
        self.assertAlmostEqual(project([1,0,1],c,640,360,36)[0],.5+35/180)
        self.assertLess(project([1,5,1],c,640,360,36)[0],project([1,0,1],c,640,360,36)[0])
        zoom=dict(c,lens_mm=70);self.assertAlmostEqual(project([1,0,1],zoom,640,360,36)[0]-.5,2*(x-.5+35/180))
    def test_roll_and_behind(self):
        c={'position':[0,-5,1],'target':[0,0,1],'lens_mm':35}
        self.assertAlmostEqual(project([1,0,1],c,640,360,36,90)[0],.5)
        self.assertLess(project([0,-6,1],c,640,360,36)[2],0)
    def test_path(self):
        keys=[{'frame':0,'position':[0,0,0]},{'frame':4,'position':[4,0,0]}]
        self.assertEqual(sample(keys,2,'linear')['position'],[2,0,0]);self.assertEqual(sample(keys,2,'smoothstep')['position'],[2,0,0])
        self.assertLess(sample(keys,1,'smoothstep')['position'][0],1)
    def test_invalid_contracts(self):
        cases=[lambda p:p.update(fps=True),lambda p:p.update(resolution=[0,720]),lambda p:p['subjects'][0].update(size_m=[0,1,1]),lambda p:p['shots'][0]['camera'].update(lens_mm=0),lambda p:p['shots'][0]['camera']['keyframes'][0].update(target=[0,-5,1.6]),lambda p:p['shots'][0].update(subject_ids=['missing']),lambda p:p['shots'][0].update(duration_frames=-1),lambda p:p['shots'][0]['camera']['keyframes'].pop(),lambda p:p['shots'][0]['axis'].update(b_subject_id='missing'),lambda p:p['shots'][0]['camera'].update(clearance_radius_m=-1)]
        for i,change in enumerate(cases):
            with self.subTest(i=i):p=spec();change(p);self.assertTrue(validate(p))
    def test_motion_collision_and_axis(self):
        p=spec();p['obstacles']=[{'id':'W01','position':[0,-5,0],'size_m':[1,1,2]}];r=analyze(p)
        self.assertTrue(any(w['type']=='camera_clearance_aabb_overlap' for w in r['shots'][0]['warnings']))
        p=spec();p['shots'][0]['axis']['allowed_side']='positive';r=analyze(p)
        self.assertTrue(any(w['type']=='axis_side_change' for w in r['shots'][0]['warnings']))
    def test_cli_reads_and_writes_utf8_independent_of_locale(self):
        with tempfile.TemporaryDirectory() as temp:
            p=spec();p['project_id']='한국어-é'
            source=Path(temp,'camera.json');output=Path(temp,'analysis.json')
            source.write_text(json.dumps(p,ensure_ascii=False),encoding='utf-8')
            env=dict(os.environ,PYTHONUTF8='0',PYTHONCOERCECLOCALE='0',LC_ALL='C')
            result=subprocess.run([sys.executable,str(Path(__file__).with_name('spatial_spec.py')),str(source),'--out',str(output)],
                                  env=env,capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            report=json.loads(output.read_text(encoding='utf-8'))
            self.assertTrue(report['valid'])
            self.assertEqual(report['project_id'],'한국어-é')

def ledger():
    """Minimal canonical project: SH01/SH02 cover the spec's two 2s shots at 24fps."""
    return {
        'schema_version':'1.1','project_id':'dialogue-distance-previs','version':'0.1','fps':24,
        'scenes':[{'id':'S01','purpose':'대화 장면'}],
        'characters':[{'id':'CH01','locked_traits':'t'},{'id':'CH02','locked_traits':'t'}],
        'shots':[
            {'id':'SH01','scene_id':'S01','character_ids':['CH01','CH02'],'asset_ids':[],'start_s':0,'end_s':2,
             'spatial':{'mode':'numeric','artifact_id':'CAM01'}},
            {'id':'SH02','scene_id':'S01','character_ids':['CH01','CH02'],'asset_ids':[],'start_s':2,'end_s':4,
             'spatial':{'mode':'numeric','artifact_id':'CAM01'}},
        ],
        'artifacts':[{'id':'CAM01','type':'camera_spec','version':'1.0','status':'reviewed'}],
    }
class ReconcileTests(unittest.TestCase):
    def test_registered_spec_attaches(self):
        self.assertEqual(reconcile_project(ledger(),spec(),'CAM01'),[])
    def test_subset_spec_is_legitimate(self):
        p=spec();p['shots']=[s for s in p['shots'] if s['id']=='SH01']
        j=ledger();j['shots'][1]['spatial']={'mode':'not_applicable','reason':'간단 그래픽'}
        self.assertEqual(reconcile_project(j,p,'CAM01'),[])
    def test_numeric_shot_missing_from_spec(self):
        p=spec();p['shots']=[s for s in p['shots'] if s['id']=='SH01']
        self.assertTrue(reconcile_project(ledger(),p,'CAM01'))
    def test_wrong_version_project_scene_fps_duration(self):
        def change(fn):
            j=ledger();fn(j);return reconcile_project(j,spec(),'CAM01')
        self.assertTrue(change(lambda j:j['shots'][1].update(scene_id='S02')))
        self.assertTrue(change(lambda j:j.update(fps=30)))
        self.assertTrue(change(lambda j:j['shots'][0].update(end_s=3)))
        self.assertTrue(change(lambda j:j['shots'][0].update(start_s=0.5)))
        j=ledger();p=spec();p['version']='9.9';self.assertTrue(reconcile_project(j,p,'CAM01'))
        p=spec();p['project_id']='other';self.assertTrue(reconcile_project(j,p,'CAM01'))
    def test_artifact_type_id_and_declared_mismatch(self):
        j=ledger();self.assertTrue(reconcile_project(j,spec(),'MISSING'))
        j['artifacts'][0]['type']='storyboard';self.assertTrue(reconcile_project(j,spec(),'CAM01'))
        j=ledger();p=spec();del p['version'];self.assertTrue(reconcile_project(j,p,'CAM01'))
        p=spec();p['artifact_id']='OTHER';self.assertTrue(reconcile_project(j,p,'CAM01'))
    def test_unknown_subject_reference(self):
        j=ledger();j['shots'][0]['character_ids']=['CH01']
        self.assertTrue(reconcile_project(j,spec(),'CAM01'))
    def test_standalone_spec_without_version_still_validates(self):
        p=spec();del p['version'];del p['artifact_id']
        self.assertEqual(validate(p),[])
        self.assertTrue(reconcile_project(ledger(),p,'CAM01'))
if __name__=='__main__':unittest.main()
