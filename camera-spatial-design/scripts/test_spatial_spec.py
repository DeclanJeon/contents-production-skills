import copy,json,math,unittest
from pathlib import Path
from spatial_spec import validate,analyze,project,sample

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
if __name__=='__main__':unittest.main()
