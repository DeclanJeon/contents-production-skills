import copy,json,math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import path_map
from path_map import (parse_facing_map,facing_at,facing_summary,facing_rotation_z,figure_proxy_parts,
                      silhouette_points,silhouette_half_extent,cone_mesh,facing_marker_parts,
                      occlusion_summary,build_svg,shot_samples)
from build_previs import signed_volume

EXAMPLE=Path(__file__).resolve().parents[2]/'camera-spatial-design'/'assets'/'camera-spec-example.json'


def spec():
    return json.loads(EXAMPLE.read_text(encoding='utf-8'))


def shot(data,shot_id):
    return [s for s in data['shots'] if s['id']==shot_id][0]


class FacingMapTests(unittest.TestCase):
    def test_normalizes_and_accepts_object_form(self):
        m,errors=parse_facing_map('{"SH01": {"CH01": [0, 5], "CH02": {"vector": [2, 0]}}}')
        self.assertEqual(errors,[])
        self.assertAlmostEqual(m['SH01']['CH01']['vector'][1],1.0)
        self.assertAlmostEqual(m['SH01']['CH02']['vector'][0],1.0)

    def test_rejects_bad_shapes_zero_and_non_finite(self):
        for bad in ('{','"x"','{}','{"SH01":{"CH01":[0,0]}}','{"SH01":{"CH01":[1]}}',
                    '{"SH01":{"CH01":["a",1]}}','{"SH01":{"CH01":[1,2,3]}}'):
            with self.subTest(bad=bad):
                m,errors=parse_facing_map(bad)
                self.assertTrue(errors)


class FacingAtTests(unittest.TestCase):
    def test_override_wins_over_motion(self):
        data=spec()
        vector,source=facing_at(data,shot(data,'SH02'),'CH01',10,{'SH02':{'CH01':{'vector':[-1.0,0.0]}}})
        self.assertEqual(source,'facing-map')
        self.assertEqual(tuple(vector),(-1.0,0.0))

    def test_static_subject_reports_no_direction(self):
        data=spec()
        vector,source=facing_at(data,shot(data,'SH01'),'CH02',10)
        self.assertEqual((vector,source),(None,'none'))

    def test_moving_subject_derives_direction_from_travel(self):
        data=spec()
        vector,source=facing_at(data,shot(data,'SH02'),'CH01',10)
        self.assertEqual(source,'motion')
        self.assertAlmostEqual(math.hypot(*vector),1.0)

    def test_summary_records_source_per_subject(self):
        data=spec()
        summary=facing_summary(data,shot(data,'SH02'))
        self.assertEqual(summary['CH01']['source'],'motion')
        self.assertEqual(summary['CH02'],{'vector':None,'source':'none'})

    def test_look_card_subject_reports_no_rendered_heading(self):
        data=spec()
        summary=facing_summary(data,shot(data,'SH02'),{'SH02':{'CH01':{'vector':[1.0,0.0]}}},('CH01',))
        self.assertEqual(summary['CH01'],{'vector':None,'source':'look-card'})
        self.assertEqual(summary['CH02']['source'],'none')

    def test_marker_rotation_points_plus_y_cone_along_heading(self):
        angle=facing_rotation_z([1.0,0.0])
        # Rz(angle) applied to local +Y must equal the requested world heading.
        self.assertAlmostEqual(math.cos(angle+math.pi/2),1.0,places=9)
        self.assertAlmostEqual(math.sin(angle+math.pi/2),0.0,places=9)
        self.assertIsNone(facing_rotation_z(None))


class SilhouetteTests(unittest.TestCase):
    def test_box_grid_has_nine_points_inside_the_proxy(self):
        points=silhouette_points([0.5,0.35,1.7],'box')
        self.assertEqual(len(points),9)
        names=[p['name'] for p in points]
        self.assertEqual(names,[f'{row}_{column}' for row in ('high','mid','low') for column in ('left','center','right')])
        for point in points:
            self.assertGreater(point['z'],0.0)
            self.assertLess(point['z'],1.7)
            self.assertLessEqual(abs(point['lateral_frac']),0.9)

    def test_figure_grid_uses_body_heights(self):
        box=silhouette_points([0.5,0.35,1.7],'box')
        figure=silhouette_points([0.5,0.35,1.7],'figure')
        self.assertEqual(len(figure),9)
        self.assertNotEqual([p['z'] for p in box],[p['z'] for p in figure])
        head=figure_proxy_parts([0.5,0.35,1.7])[-1]
        self.assertAlmostEqual(figure[0]['z'],head['z'])

    def test_half_extent_matches_axis_projection(self):
        # Camera looking along +X: the right axis is world -Y, so the depth counts.
        self.assertAlmostEqual(silhouette_half_extent([0.5,0.35,1.7],'box',(0.0,1.0)),0.175)
        self.assertAlmostEqual(silhouette_half_extent([0.5,0.35,1.7],'box',(1.0,0.0)),0.25)
        torso=figure_proxy_parts([0.5,0.35,1.7])[0]
        self.assertAlmostEqual(silhouette_half_extent([0.5,0.35,1.7],'figure',(1.0,0.0)),torso['radius'])


class MarkerMeshTests(unittest.TestCase):
    def test_cone_is_closed_and_outward_facing(self):
        verts,faces=cone_mesh(12)
        self.assertEqual(len(verts),14)
        self.assertGreater(signed_volume(verts,faces),0.0)
        edges={}
        for f in faces:
            for i in range(len(f)):
                e=tuple(sorted((f[i],f[(i+1)%len(f)])))
                edges[e]=edges.get(e,0)+1
        self.assertTrue(all(count==2 for count in edges.values()))

    def test_marker_sits_above_the_base_and_inside_the_body(self):
        marker=facing_marker_parts([0.5,0.35,1.7])
        self.assertGreater(marker['z'],0.0)
        self.assertLess(marker['z'],1.7)
        self.assertGreater(marker['offset_y'],0.0)
        self.assertLess(marker['offset_y'],0.35)


class OcclusionSummaryTests(unittest.TestCase):
    def test_reports_fraction_and_first_hidden_point(self):
        data=spec();current=shot(data,'SH01')
        checks=[{'frame':0,'subject_id':'CH01','point':'mid_center','proxy_point_visible':True,'first_hit':None},
                {'frame':1,'subject_id':'CH01','point':'mid_left','proxy_point_visible':False,'first_hit':'SH01_CH02'},
                {'frame':1,'subject_id':'CH01','point':'mid_center','proxy_point_visible':True,'first_hit':None}]
        summary=occlusion_summary(checks,current,'box')
        self.assertEqual(summary['frames_checked'],2)
        entry=summary['subjects']['CH01']
        self.assertEqual(entry['points_checked'],3)
        self.assertAlmostEqual(entry['visible_fraction'],round(2/3,4))
        self.assertEqual(entry['first_occluded'],{'frame':1,'point':'mid_left','first_hit':'SH01_CH02'})
        self.assertEqual(entry['proxy'],'box')
        self.assertIn('point sampling only',summary['scope'])


class DiagramGeometryTests(unittest.TestCase):
    def test_pixels_follow_the_documented_world_to_page_mapping(self):
        data=spec();current=shot(data,'SH01')
        rows=shot_samples(data,current)
        svg=build_svg(data,current)
        xmin,xmax,ymin,ymax=path_map._bounds(data,current,rows)
        width=1180;scale=(width-80)/(xmax-xmin);origin_x,origin_y=40,60
        camera=rows[0]['camera']['position']
        expected=(origin_x+(camera[0]-xmin)*scale,origin_y+(ymax-camera[1])*scale)
        self.assertIn(f'cx="{path_map._f(expected[0])}" cy="{path_map._f(expected[1])}" r="4"',svg)

    def test_one_metre_scale_bar_spans_exactly_the_scale(self):
        data=spec();current=shot(data,'SH01')
        svg=build_svg(data,current)
        import re
        match=re.search(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="\2" stroke="#8b93a7"',svg)
        self.assertIsNotNone(match)
        rows=shot_samples(data,current)
        xmin,xmax,_,_=path_map._bounds(data,current,rows)
        self.assertAlmostEqual(float(match.group(3))-float(match.group(1)),(1180-80)/(xmax-xmin),places=2)


class DiagramTests(unittest.TestCase):
    def test_svg_is_deterministic_and_names_its_parts(self):
        data=spec();data['obstacles']=[{'id':'PILLAR','size_m':[0.4,0.4,3.0],'position':[0.0,0.9,0.0]}]
        current=shot(data,'SH02')
        first=build_svg(data,current);second=build_svg(data,current)
        self.assertEqual(first,second)
        self.assertTrue(first.startswith('<svg'))
        self.assertTrue(first.rstrip().endswith('</svg>'))
        for token in ('SH02','CH01','CH02','PILLAR','camera path','1 m','facing'):
            self.assertIn(token,first)

    def test_svg_marks_undetermined_facing_for_a_static_subject(self):
        data=spec()
        svg=build_svg(data,shot(data,'SH01'))
        self.assertIn('facing undetermined',svg)

    def test_svg_uses_facing_map_heading(self):
        data=spec()
        svg=build_svg(data,shot(data,'SH01'),facing_map={'SH01':{'CH02':{'vector':[0.0,1.0]}}})
        self.assertIn('facing·facing-map',svg)
        # CH01 is static in SH01 and has no map entry, so exactly one subject stays undetermined.
        self.assertEqual(svg.count('facing undetermined'),1)

    def test_samples_cover_the_shot_without_repeating_the_last_frame(self):
        rows=shot_samples(spec(),shot(spec(),'SH01'))
        frames=[row['frame'] for row in rows]
        self.assertEqual(frames,sorted(set(frames)))
        self.assertEqual(frames[0],0)
        self.assertEqual(frames[-1],47)


if __name__=='__main__':unittest.main()
