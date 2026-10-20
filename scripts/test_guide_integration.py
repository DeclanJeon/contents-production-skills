"""Static guide-integration contracts; not an agent/media quality benchmark.

Run: python3 -m unittest discover -s scripts -p test_guide_integration.py -v
No source PDF, OCR runtime, generation service or third-party package required.
"""
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "video-production-assets/references"
ASSETS = ROOT / "video-production-assets/assets"
GUIDE = REFS / "29-reference-driven-production.md"
ANCHORS = {
    "reference-roles", "sheet-inputs", "space-performance", "bilingual-prompts",
    "generation-modes", "dialogue-repair", "usable-ranges", "episode-delivery",
}


def read(path):
    return path.read_text(encoding="utf-8")


class GuideIntegrationTests(unittest.TestCase):
    def test_scan_identity_and_page_coverage(self):
        scan = json.loads(read(REFS / "guide-01-scan.json"))
        self.assertEqual(scan["source_sha256"],
                         "9dbc047ccbb9ef9e40f27cce0954e800838e35ccae32ce95b31ae6d2f5fb4a7d")
        self.assertEqual(scan["source_bytes"], 43462504)
        self.assertEqual(scan["page_count"], 101)
        self.assertEqual(scan["embedded_file_count"], 0)
        self.assertEqual(scan["direct_text_nonwhitespace_chars"], 0)
        self.assertEqual([p["page"] for p in scan["pages"]], list(range(1, 102)))
        for p in scan["pages"]:
            with self.subTest(page=p["page"]):
                self.assertTrue(p["ocr_read"])
                self.assertTrue(p["contact_sheet_overview"])
                self.assertGreater(p["ocr_nonwhitespace_chars"], 0)
                for key in ("render_sha256", "ocr_sha256"):
                    self.assertRegex(p[key], r"^[0-9a-f]{64}$")
        self.assertEqual(scan["individual_render_review_pages"],
                         [p["page"] for p in scan["pages"] if p["individual_render_review"]])
        self.assertEqual(len(scan["individual_render_review_pages"]), 28)
        self.assertFalse(scan["ocr_method"]["external_upload"])

    def test_all_chapters_and_knowledge_dispositions(self):
        scan = json.loads(read(REFS / "guide-01-scan.json"))
        audit = read(REFS / "guide-01-extraction.md")
        self.assertEqual([c["chapter"] for c in scan["chapters"]], list(range(1, 24)))
        covered = set()
        for c in scan["chapters"]:
            self.assertIn(f"| {c['chapter']:02d} ", audit)
            covered.update(range(c["start_page"], c["end_page"] + 1))
        self.assertEqual(covered, set(range(3, 102)))
        self.assertEqual(re.findall(r"\| (K\d{2}) \|", audit),
                         [f"K{i:02d}" for i in range(1, 45)])

    def test_runtime_links_and_explicit_anchors(self):
        guide = read(GUIDE)
        self.assertEqual(set(re.findall(r'<a id="([^"]+)"></a>', guide)), ANCHORS)
        for file in (GUIDE, REFS / "guide-01-extraction.md"):
            for link in re.findall(r"\]\(([^)]+)\)", read(file)):
                if "://" in link:
                    continue
                target, _, fragment = link.partition("#")
                path = (file.parent / target).resolve() if target else file
                with self.subTest(file=file.name, link=link):
                    self.assertTrue(path.is_file(), str(path))
                    if path == GUIDE and fragment:
                        self.assertIn(fragment, ANCHORS)
        # Provenance lives inside the installed skill, not absent sibling docs/.
        for name in ("sources.md", GUIDE.name):
            self.assertIn("guide-01-extraction.md", read(REFS / name))
            self.assertIn("guide-01-scan.json", read(REFS / name))

    def test_existing_owners_reach_relevant_procedures(self):
        owners = {
            "11-ai-handoff.md": ["reference-roles", "bilingual-prompts", "generation-modes"],
            "20-visual-mode-ssot.md": ["sheet-inputs"],
            "05-visual.md": ["space-performance"],
            "22-dialogue-lipsync.md": ["dialogue-repair"],
            "21-generated-video-qa-retry.md": ["usable-ranges", "generation-modes"],
            "14-production-ops.md": ["usable-ranges"],
            "18-episodic-series.md": ["episode-delivery"],
            "15-delivery.md": ["episode-delivery"],
        }
        for name, anchors in owners.items():
            for anchor in anchors:
                with self.subTest(owner=name, anchor=anchor):
                    self.assertIn(f"{GUIDE.name}#{anchor}", read(REFS / name))
        for relative in ("creative-production/SKILL.md", "video-production-assets/SKILL.md",
                         "designing-video-character-sheets/references/character-craft.md",
                         "blender-previsualization/assets/previs-handoff-template.md"):
            self.assertIn(GUIDE.name, read(ROOT / relative))

    def test_templates_expose_actionable_slots(self):
        required = {
            "11-ai-handoff-template.md": ["가져올 속성", "제외할 속성", "우선 기준", "NOT_EXPOSED", "번역 대조", "실제 확장"],
            "performance-cue-template.md": ["교체 in/out", "받침", "크로스페이드", "권리/동의", "전체 장면 믹스"],
            "generated-qa-report-template.md": ["원본 FPS/PTS", "선택 구간 판정", "빠진 필수 사건", "원본 포함 여부"],
            "14-production-ops-template.md": ["생성 총초수", "채택 초수", "0초=N/A", "미산정", "재개할 다음 작업"],
            "series-bible-template.md": ["이번 편 사건", "인물다운 선택", "estimated"],
        }
        for name, phrases in required.items():
            for phrase in phrases:
                with self.subTest(template=name, phrase=phrase):
                    self.assertIn(phrase, read(ASSETS / name))

    def test_no_drama_or_fixed_provider_recipe_in_runtime_guide(self):
        guide = read(GUIDE)
        for word in ("야장시단", "유메", "하린", "흑야풍", "Seedance 2.5", "Fish Audio", "GPT Image 2.5"):
            self.assertNotIn(word, guide)
        for phrase in ("90초", "세 번", "중국어·영어를 기본값으로 강제하지 않는다",
                       "현재 서비스의 실제 길이/형식", "T값 하나로 심도를 계산하지 않는다"):
            self.assertIn(phrase, guide)

    def test_existing_scope_and_authority_guards_remain(self):
        guide = read(GUIDE)
        for phrase in ("Sheet A 7뷰 요구는 유지", "별도 실행 승인이 필요",
                       "복제는 기본값이 아니며", "단일 기록자", "판정 enum",
                       "원본 영상·음성·Blender 파일은 이번 검토에 제공되지 않았다"):
            self.assertIn(phrase, guide)
        manifest = json.loads(read(ROOT / "manifest.json"))
        # Unrelated optional specialists may be present in a dirty checkout.
        # The guide integration adds no new skill and must not depend on them.
        self.assertTrue({"creative-production", "video-production-assets",
                         "designing-video-character-sheets"} <= set(manifest["skills"]))
        self.assertEqual(len(manifest["skills"]), len(set(manifest["skills"])))
        self.assertFalse(any("guide" in s for s in manifest["skills"]))

    def test_crosswalk_binds_every_item_to_owner_template_and_acceptance(self):
        coverage = json.loads(read(REFS / "guide-01-coverage.json"))
        self.assertEqual([i["id"] for i in coverage["items"]],
                         [f"K{i:02d}" for i in range(1, 45)])
        guide = read(GUIDE)
        audit_rows = {m[0]: (m[1].strip(), m[2].strip()) for m in re.findall(
            r"^\| (K\d{2}) \| ([^|]+) \| ([^|]+) \| [^|]+ \|$",
            read(REFS / "guide-01-extraction.md"), re.MULTILINE)}
        for item in coverage["items"]:
            with self.subTest(item=item["id"]):
                self.assertEqual((item["knowledge"], item["source_pdf_pages"]),
                                 audit_rows[item["id"]])
                self.assertEqual(item["evidence_level"], "source_document_contract_only")
                self.assertEqual(item["media_or_agent_effectiveness"], "unverified")
                for slot in ("owner", "template", "acceptance"):
                    binding = item[slot]
                    path = (ROOT / binding["path"]).resolve()
                    self.assertTrue(path.is_relative_to(ROOT))
                    self.assertIn(binding["marker"], read(path))
                anchor = item["reference"]["anchor"]
                if anchor:
                    self.assertIn(anchor, ANCHORS)
                    section = guide.split(f'<a id="{anchor}"></a>', 1)[1].split('<a id="', 1)[0]
                else:
                    section = guide.split('<a id="', 1)[0]
                self.assertIn(item["acceptance"]["marker"], section)
                for page in re.findall(r"\d+", item["source_pdf_pages"]):
                    self.assertTrue(1 <= int(page) <= 101)

    def test_narrow_owners_and_writable_followup_slots(self):
        owners = ["04-performance.md", "06-shots.md", "07-lighting.md", "09-edit.md"]
        for name in owners:
            self.assertIn(GUIDE.name, read(REFS / name))
        for path in ("camera-spatial-design/references/motion-timing-lens.md",
                     "ai-camera-control/references/control-contract.md"):
            self.assertIn(GUIDE.name, read(ROOT / path))
        templates = {
            "04-performance-template.md": ["자극→최소 반응", "시도/완료"],
            "05-visual-template.md": ["참조 기반 장소·소품 설계", "개폐/효과 상태", "입출구"],
            "07-lighting-template.md": ["공간 고정 광원", "실제 f-number/T-stop"],
            "character-ssot-template.md": ["답할 수 없는 질문", "필수 조건을 검사", "개별 원본과 통합 시트"],
            "crowd-map-template.md": ["정확한 인원수", "배경 밀도", "주인공 통로"],
            "motion-beat-template.md": ["관절", "탑승/하중", "소멸"],
            "vfx-layer-stack-template.md": ["발동 전→시작→지속→소멸", "잔류/복귀"],
            "09-edit-template.md": ["선택 구간/편집 후 판정", "원본 포함 확장"],
            "15-delivery-template.md": ["원문·실제 발화·자막", "화면비별 파일/크롭 검사"],
            "11-ai-handoff-template.md": ["과밀 입력 정리", "관측 가능한 대응", "클립/테이크 대응"],
        }
        for name, phrases in templates.items():
            for phrase in phrases:
                with self.subTest(template=name, phrase=phrase):
                    self.assertIn(phrase, read(ASSETS / name))

    def test_actual_request_snapshot_is_separate_from_hidden_rewrite(self):
        guide = read(GUIDE)
        template = read(ASSETS / "11-ai-handoff-template.md")
        for phrase in ("클라이언트가 실제 보낸 전체 요청문", "그 항목만 `NOT_EXPOSED`",
                       "실제 요청문 스냅샷을 생략", "SSOT 소비 증거 요건"):
            self.assertIn(phrase, guide)
        self.assertIn("실제 요청문 스냅샷", template)
        self.assertIn("공급자 보정/변환 후 본문", template)

    def test_followup_scan_preserves_original_coverage(self):
        scan = json.loads(read(REFS / "guide-01-scan.json"))
        original = set(scan["individual_render_review_pages"])
        followup = scan["followup_reviews"][0]
        extra = set(followup["individual_render_review_pages"])
        self.assertEqual(extra, {6, 32, 43, 67, 77})
        self.assertEqual(len(original), 28)
        self.assertEqual(len(original | extra), 33)
        self.assertEqual(followup["cumulative_individual_render_review_page_count"], 33)

    def test_followup_behavior_inputs_do_not_claim_results(self):
        suite = json.loads(read(ROOT / "qa/guide-followup-scenarios.json"))
        self.assertEqual(suite["status"], "evaluation_inputs_only")
        self.assertTrue((ROOT / suite["execution_review"]).is_file())
        self.assertEqual(len(suite["cases"]), 6)
        self.assertEqual(len({c["id"] for c in suite["cases"]}), 6)
        for case in suite["cases"]:
            self.assertTrue(case["required"])
            self.assertTrue(case["forbidden"])
            self.assertNotIn("passed", case)

    def test_behavior_inputs_do_not_claim_results(self):
        suite = json.loads(read(ROOT / "qa/guide-integration-scenarios.json"))
        self.assertEqual(suite["status"], "evaluation_inputs_only")
        self.assertTrue((ROOT / suite["execution_review"]).is_file())
        self.assertEqual(len(suite["cases"]), 12)
        self.assertEqual(len({c["id"] for c in suite["cases"]}), 12)
        for case in suite["cases"]:
            self.assertTrue(case["prompt"])
            self.assertTrue(case["required"])
            self.assertTrue(case["forbidden"])
            self.assertNotIn("passed", case)

    def test_review_evidence_bindings_not_semantic_verdicts(self):
        report = json.loads(read(ROOT / "qa/guide-behavior-review.json"))
        cases = {}
        for name in ("guide-integration-scenarios.json", "guide-followup-scenarios.json"):
            cases.update({c["id"]: c for c in json.loads(read(ROOT / "qa" / name))["cases"]})
        self.assertEqual({c["id"] for c in report["cases"]}, set(cases))
        for review in report["cases"]:
            with self.subTest(case=review["id"]):
                attempt_path = ROOT / review["attempt_path"]
                attempt = json.loads(read(attempt_path))
                response = read(ROOT / review["response_path"])
                wire = attempt_path.with_name(attempt_path.name.replace(".attempt.json", ".stdout.jsonl")).read_bytes()
                self.assertEqual(hashlib.sha256(wire).hexdigest(), review["wire_stdout_sha256"])
                self.assertEqual(attempt["prompt"], cases[review["id"]]["prompt"])
                self.assertEqual(response, attempt["trace"]["final_text"])
                self.assertEqual(attempt["verdict"], "UNREVIEWED")
                self.assertEqual(attempt["source_before"], attempt["source_after"])
                self.assertIn(review["verdict"], {"PASS", "PARTIAL", "FAIL"})
                self.assertEqual([c["criterion"] for c in review["required_criteria"]], cases[review["id"]]["required"])
                for criterion in review["required_criteria"]:
                    self.assertTrue(criterion["response_quotes"])
                    for quote in criterion["response_quotes"]:
                        self.assertIn(quote, response)
                # These checks bind evidence; they intentionally do not decide if
                # the recorded semantic judgments are correct.


if __name__ == "__main__":
    unittest.main()
