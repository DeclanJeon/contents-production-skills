import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_previs
from build_previs import parse_render_map,render_plan,figure_proxy_parts,sphere_mesh,signed_volume,parse_focus_map,focus_distance_at,parse_look_cards,engine_candidates

class FigureProxyTests(unittest.TestCase):
    def test_parts_stack_head_above_torso_inside_subject_height(self):
        parts=figure_proxy_parts([0.5,0.35,1.7])
        names=[p['name'] for p in parts]
        self.assertEqual(names,['torso','neck','head'])
        head=[p for p in parts if p['name']=='head'][0]
        torso=[p for p in parts if p['name']=='torso'][0]
        self.assertGreater(head['z'],torso['z'])
        self.assertLess(head['z']+head['radius']*head['scale'][2],1.7)
        self.assertGreater(torso['z']-torso['radius']*torso['scale'][2],0.0)
    def test_parts_handle_small_and_large_subjects(self):
        for size in ([0.2,0.2,0.4],[1.0,0.8,2.2]):
            with self.subTest(size=size):
                parts=figure_proxy_parts(size)
                self.assertTrue(all(p['radius']>0 for p in parts))
                head=[p for p in parts if p['name']=='head'][0]
                self.assertLess(head['z']+head['radius']*head['scale'][2],size[2]+1e-6)
    def test_sphere_mesh_is_closed_with_outward_normals(self):
        verts,faces=sphere_mesh(segments=16,rings=8)
        self.assertGreater(signed_volume(verts,faces),0.0)
        self.assertEqual(len(verts),2+16*(8-1))
        counts={}
        for f in faces:
            self.assertIn(len(f),(3,4))
            for i in range(len(f)):
                e=tuple(sorted((f[i],f[(i+1)%len(f)])))
                counts[e]=counts.get(e,0)+1
        self.assertTrue(all(c==2 for c in counts.values()))
    def test_proxy_cli_defaults_to_box_and_accepts_figure(self):
        argv=sys.argv
        try:
            sys.argv=['build_previs.py','--','--spec','s.json','--output','o']
            self.assertEqual(build_previs.arguments().proxy,'box')
            sys.argv=['build_previs.py','--','--spec','s.json','--output','o','--proxy','figure']
            self.assertEqual(build_previs.arguments().proxy,'figure')
        finally:
            sys.argv=argv

def spec():return json.loads((Path(__file__).parent.parent.parent/'camera-spatial-design'/'assets'/'camera-spec-example.json').read_text())
def frames(plan):return {sid:[e['frame'] for e in rows] for sid,rows in plan.items()}
class FocusLookEngineTests(unittest.TestCase):
    def test_focus_map_normalizes_and_rejects_bad_values(self):
        m,errors=parse_focus_map('{"SH01": {"f_number": 2.8, "keyframes": [{"frame": 0, "focus_distance_m": 4.0}, {"frame": 47, "focus_distance_m": 1.0}]}}')
        self.assertEqual(errors,[])
        self.assertEqual(m['SH01']['f_number'],2.8)
        self.assertEqual([k['frame'] for k in m['SH01']['keyframes']],[0,47])
        for bad in ('{','{"SH01": {}}','{"SH01": {"keyframes": [{"frame": 0, "focus_distance_m": 0}]}}',
                    '{"SH01": {"keyframes": [{"frame": "x", "focus_distance_m": 1}]}}',
                    '{"SH01": {"f_number": 0, "keyframes": [{"frame": 0, "focus_distance_m": 1}]}}'):
            with self.subTest(bad=bad):
                m,errors=parse_focus_map(bad);self.assertTrue(errors,bad)
    def test_focus_distance_interpolates_and_clamps(self):
        keys=[{'frame':0,'focus_distance_m':4.0},{'frame':47,'focus_distance_m':1.0}]
        self.assertAlmostEqual(focus_distance_at(keys,0),4.0)
        self.assertAlmostEqual(focus_distance_at(keys,24),4.0+(1.0-4.0)*(24/47))
        self.assertAlmostEqual(focus_distance_at(keys,47),1.0)
        self.assertAlmostEqual(focus_distance_at(keys,90),1.0)
        self.assertIsNone(focus_distance_at([],3))
    def test_look_cards_require_existing_files_and_subjects(self):
        import tempfile,os
        with tempfile.TemporaryDirectory() as tmp:
            img=os.path.join(tmp,'look.png');open(img,'wb').write(b'x')
            m,errors=parse_look_cards('{"CH01": {"image": "%s"}}'%img)
            self.assertEqual(errors,[]);self.assertTrue(m['CH01']['image'].endswith('look.png'))
            m,errors=parse_look_cards('{"CH01": {"image": "%s/missing.png"}}'%tmp)
            self.assertTrue(errors)
    def test_engine_candidates(self):
        self.assertEqual(engine_candidates('cycles'),['CYCLES'])
        self.assertEqual(engine_candidates('eevee'),['BLENDER_EEVEE_NEXT','BLENDER_EEVEE'])


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
