"""Small decision-contract scenarios; no independent LLM or actual media evaluation."""
import unittest
from reference_contract import camera_choice, rights_disposition, control_disposition, inspection_support


class ReferenceDecisions(unittest.TestCase):
    def test_camera_choice_preserves_mechanism_and_ambiguity(self):
        self.assertEqual(camera_choice('translate_toward_subject'), 'dolly')
        self.assertEqual(camera_choice('tighten_without_translation'), 'zoom_or_crop')
        self.assertEqual(camera_choice('move closer'), 'unresolved')
        self.assertEqual(camera_choice('change_focus_target'), 'rack_focus')

    def test_commercial_permission_does_not_grant_upload_or_training(self):
        row={'actions':{'commercial_use':{'decision':'allowed','evidence_locator':'terms#media','checked_at':'2026-11-01'},
                        'ai_training':{'decision':'restricted','evidence_locator':'terms#ai','checked_at':'2026-11-01'}}}
        self.assertEqual(rights_disposition(row,'commercial_use'),'evidence_recorded')
        self.assertEqual(rights_disposition(row,'generator_upload'),'unverified')
        self.assertEqual(rights_disposition(row,'ai_training'),'restricted')

    def test_allowed_word_without_evidence_is_not_clearance(self):
        self.assertEqual(rights_disposition({'actions':{'generator_upload':{'decision':'allowed'}}},'generator_upload'),'unverified')
        with self.assertRaises(ValueError):rights_disposition({},'publish_everywhere')

    def test_caption_and_metadata_are_not_motion_or_listening(self):
        row={'evidence':{'page_text':[{'locator':'post/body','scope':'text only'}],
                         'stream_metadata':[{'locator':'probe','scope':'audio stream exists'}]}}
        self.assertTrue(inspection_support(row,'body_text'))
        self.assertFalse(inspection_support(row,'motion'))
        self.assertFalse(inspection_support(row,'audio'))

    def test_frames_do_not_establish_dynamic_quality(self):
        row={'evidence':{'opened_frames':[{'locator':'frame@1.2','scope':'one image'}]}}
        self.assertTrue(inspection_support(row,'sampled_appearance'))
        self.assertFalse(inspection_support(row,'motion'))
        self.assertFalse(inspection_support(row,'audio'))

    def test_only_inspected_intervals_are_supported(self):
        row={'evidence':{'continuous_playback':[{'locator':'clip#0-2','scope':'0-2s only'}]}}
        self.assertTrue(inspection_support(row,'motion'))
        self.assertFalse(inspection_support(row,'audio'))
        row['evidence']['listening']=[{'locator':'audio','scope':''}]
        self.assertFalse(inspection_support(row,'audio'))

    def test_uninspected_schema_never_yields_hard_control(self):
        self.assertEqual(control_disposition('focal_length',{'fields':{'focal_length':{'supported':True,'locator':'old-doc'}}}),'UNVERIFIED')

    def test_endpoint_duration_is_not_exact_camera_control(self):
        row={'inspected':True,'locator':'current-schema','fields':{'duration':{'supported':True,'locator':'schema#duration'}},
             'text_intent_supported':True,'unsupported':['camera_path']}
        self.assertEqual(control_disposition('duration',row),'HARD_CONTROL')
        self.assertEqual(control_disposition('camera_path',row),'UNSUPPORTED')
        self.assertEqual(control_disposition('focal_length',row),'SOFT_PROMPT')
