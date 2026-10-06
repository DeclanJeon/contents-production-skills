import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_previs
from build_previs import parse_render_map,render_plan

def spec():return json.loads((Path(__file__).parent.parent.parent/'camera-spatial-design'/'assets'/'camera-spec-example.json').read_text())
def frames(plan):return {sid:[e['frame'] for e in rows] for sid,rows in plan.items()}
class RenderPlanTests(unittest.TestCase):
    def test_stills_boundaries(self):
        plan,errors=render_plan(spec(),'stills')
        self.assertEqual(errors,[]);self.assertEqual(frames(plan),{'SH01':[0,24,47],'SH02':[0,24,47]})
        self.assertEqual([e['label'] for e in plan['SH01']],['start','mid','end'])
    def test_tiny_shot_boundaries(self):
        p=spec();shot=copy.deepcopy(p['shots'][0]);shot['id']='SHX';shot['duration_frames']=2
        shot['camera']['keyframes']=[k for k in shot['camera']['keyframes'] if k['frame']==0]+[dict(k,frame=1) for k in shot['camera']['keyframes'] if k['frame']==47]
        p['shots']=[shot]
        plan,errors=render_plan(p,'stills');self.assertEqual(errors,[]);self.assertEqual(frames(plan),{'SHX':[0,1]})
        shot['duration_frames']=1;shot['camera']['keyframes']=[shot['camera']['keyframes'][0]]
        plan,errors=render_plan(p,'stills');self.assertEqual(errors,[]);self.assertEqual(frames(plan),{'SHX':[0]})
    def test_sequence_covers_every_local_frame(self):
        plan,errors=render_plan(spec(),'sequence');self.assertEqual(errors,[])
        for sid in ('SH01','SH02'):self.assertEqual(frames(plan)[sid],list(range(48)))
    def test_smoke_first_shot_one_frame_only(self):
        plan,errors=render_plan(spec(),'smoke');self.assertEqual(errors,[])
        self.assertEqual(plan,{'SH01':[{'frame':0,'label':'smoke_first_frame','panels':[]}]})
    def test_smoke_resolution_is_bounded_without_upscaling(self):
        for resolution,expected in [([1920,1080],[320,180]),([1080,1920],[180,320]),
                                    ([100000,1],[320,1]),([100,200],[100,200])]:
            with self.subTest(resolution=resolution):
                self.assertEqual(build_previs.smoke_resolution(resolution),expected)
    def test_render_map_exact_peak_and_panel(self):
        m,errors=parse_render_map('{"SH01":{"P04":17},"SH02":[0,47]}')
        self.assertEqual(errors,[])
        plan,errors=render_plan(spec(),'stills',m);self.assertEqual(errors,[])
        self.assertEqual(plan['SH01'],[{'frame':17,'label':'P04','panels':['P04']}])
        self.assertEqual(frames(plan)['SH02'],[0,47])
    def test_render_map_duplicate_frames_merge_panels(self):
        m,errors=parse_render_map('[{"shot_id":"SH01","frame":17,"panel":"P04"},{"shot_id":"SH01","frame":17,"panel":"P05"}]')
        self.assertEqual(errors,[])
        plan,errors=render_plan(spec(),'stills',m);self.assertEqual(errors,[])
        self.assertEqual(len(plan['SH01']),1);self.assertEqual(sorted(plan['SH01'][0]['panels']),['P04','P05'])
    def test_rejects_out_of_range_and_wrong_mode(self):
        m,_=parse_render_map('{"SH01":[47],"SH02":[48]}')
        plan,errors=render_plan(spec(),'stills',m)
        self.assertEqual(frames(plan)['SH01'],[47]);self.assertTrue(any('SH02' in e for e in errors))
        plan,errors=render_plan(spec(),'sequence',{'SH01':[0]});self.assertTrue(errors)
        plan,errors=render_plan(spec(),'stills',{'NOPE':[0]});self.assertTrue(errors)
    def test_parse_render_map_rejects_malformed(self):
        for bad in ('{','"x"','{}','{"SH01":[]}','{"SH01":[47.5]}'):
            m,errors=parse_render_map(bad);self.assertTrue(errors,bad)
if __name__=='__main__':unittest.main()
