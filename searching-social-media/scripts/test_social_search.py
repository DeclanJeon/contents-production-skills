"""Offline contracts and fake-process integration; never SNS/network requests."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("social_search", Path(__file__).with_name("social_search.py"))
s = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(s)


def row(url="https://youtu.be/abcdefghijk", **extra):
    return {"originalUrl": url, "title": "fixture example", "uploader": "fixture author", "duration": 10, **extra}


def payload(platform="youtube", query="example", videos=None, error=None, method="native", native_error=None):
    src = {"platform": platform, "method": method, "count": len(videos or []), "searchUrl": "https://www.youtube.com/results?search_query=example"}
    if error:
        src["error"] = error
    if native_error:
        src["nativeError"] = native_error
    return {"platform": platform, "query": query, "videos": videos or [], "sources": [src]}


def returned(value, exit_code=0):
    return {"state": "returned", "exit_code": exit_code, "stdout": json.dumps(value), "stderr": None}


class FakeRunner:
    def __init__(self, values, version="1.19.0"):
        self.values = iter(values)
        self.calls = []
        self.version = version

    def call(self, args):
        self.calls.append(args)
        if args == ["--version"]:
            return {"state": "returned", "exit_code": 0, "stdout": self.version, "stderr": None}
        return next(self.values)


def args(*more):
    a = s.parser().parse_args(["--query", "example", *more])
    a.platform = a.platform or ["youtube"]
    return a


class URLTests(unittest.TestCase):
    def test_youtube_aliases_and_tracking_deduplicate(self):
        urls = ["https://youtu.be/abcdefghijk?t=5", "https://m.youtube.com/shorts/abcdefghijk", "https://www.youtube.com/watch?v=abcdefghijk&feature=share#x"]
        self.assertEqual(len({s.canonical_url(u, "youtube") for u in urls}), 1)

    def test_twitter_reddit_and_instagram_aliases(self):
        self.assertEqual(s.canonical_url("https://twitter.com/person/status/123?s=20", "twitter"), "https://x.com/i/status/123")
        self.assertEqual(s.canonical_url("https://reddit.com/r/test/comments/AbC/title/", "reddit"), "https://www.reddit.com/comments/abc/")
        self.assertEqual(s.canonical_url("https://instagram.com/reel/ABC_12/?x=1", "instagram"), "https://www.instagram.com/p/ABC_12/")

    def test_rejects_credentials_private_redirectors_and_host_spoof(self):
        for url in ["file:///tmp/a", "http://127.0.0.1/watch?v=abcdefghijk", "https://youtube.com.evil.test/watch?v=abcdefghijk", "https://youtube.com@evil.test/watch?v=abcdefghijk", "https://a:b@youtube.com/watch?v=abcdefghijk", "https://youtube.com:443/watch?v=abcdefghijk", "https://youtube.com/redirect?q=https://evil.test", "https://youtube.com/watch?v=abcdefghijk\n", "https://youtube.com\\@evil.test/watch?v=abcdefghijk"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                s.canonical_url(url, "youtube")

    def test_rejects_tiktok_short_redirector(self):
        with self.assertRaises(ValueError):
            s.canonical_url("https://vm.tiktok.com/abc", "tiktok")

    def test_all_declared_platform_paths(self):
        examples = {"threads": "https://threads.com/@test/post/Ab12", "tiktok": "https://tiktok.com/@test/video/123", "vimeo": "https://vimeo.com/123", "bilibili": "https://bilibili.com/video/BV123abc", "dailymotion": "https://dailymotion.com/video/x123", "nicovideo": "https://nicovideo.jp/watch/sm123", "ok": "https://ok.ru/video/123", "vkvideo": "https://vk.com/video-123_456"}
        for platform, url in examples.items():
            with self.subTest(platform=platform):
                self.assertTrue(s.canonical_url(url, platform).startswith("https://"))


class NormalizationTests(unittest.TestCase):
    def normalize(self, **extra):
        return s.normalize(row(**extra), "youtube", "example", 1, "2026-10-20T00:00:00Z", "native")

    def test_missing_vs_zero_metric(self):
        self.assertIsNone(self.normalize()["metrics"]["views"])
        self.assertEqual(self.normalize(view_count=0)["metrics"]["views"], 0)

    def test_unknown_uploader_and_duration_sentinel(self):
        x = self.normalize(duration=0, uploader="Unknown")
        self.assertIsNone(x["duration_seconds"])
        self.assertIsNone(x["uploader"])

    def test_reddit_score_is_not_views(self):
        x = s.normalize(row("https://reddit.com/comments/abc/", view_count=-2), "reddit", "example", 1, "now", "native")
        self.assertIsNone(x["metrics"]["views"])
        self.assertEqual(x["metrics"]["reddit_score_or_upvotes"], -2)

    def test_index_counts_unverified(self):
        x = s.normalize(row(view_count=500, searchMethod="web-index"), "youtube", "example", 1, "now", "web-index")
        self.assertEqual(x["evidence_level"], "index_only")
        self.assertIsNone(x["metrics"]["views"])
        self.assertEqual(x["metrics"]["unverified_provider_count"], 500)

    def test_no_semantic_review_inferred(self):
        x = self.normalize()
        self.assertIsNone(x["selection_reason"])
        self.assertEqual(x["content_type"], "video_post_candidate_not_viewed")

    def test_invalid_counts_not_promoted(self):
        for value in [True, "100", float('nan'), float('inf'), -1]:
            with self.subTest(value=value):
                self.assertIsNone(self.normalize(view_count=value)["metrics"]["views"])

    def test_publication_date_is_not_capture_time(self):
        self.assertEqual(s.post_date("20261001"), "2026-10-01")
        for value in ["3 days ago", "20260230", 1790000000, None]:
            self.assertIsNone(s.post_date(value))

    def test_unknown_method_or_platform_is_rejected(self):
        for extra in [{"platform": "reddit"}, {"searchMethod": "unknown"}]:
            with self.assertRaises(ValueError):
                self.normalize(**extra)


class ReportTests(unittest.TestCase):
    def test_success_and_real_empty_are_different(self):
        r = s.search_report(args(), FakeRunner([returned(payload(videos=[row()]))]))
        self.assertEqual(r["status"], "ok")
        r = s.search_report(args(), FakeRunner([returned(payload())]))
        self.assertEqual(r["status"], "empty")

    def test_partial_error_at_zero_process_exit(self):
        runner = FakeRunner([returned(payload(videos=[row()])), returned(payload(platform="instagram", error="login wall"))])
        r = s.search_report(args("--platform", "youtube", "--platform", "instagram"), runner)
        self.assertEqual(r["status"], "partial")
        self.assertEqual(len(r["candidates"]), 1)
        self.assertEqual(r["runs"][1]["state"], "failed")

    def test_all_failed_is_not_empty(self):
        r = s.search_report(args(), FakeRunner([returned(payload(error="blocked"), 4)]))
        self.assertEqual(r["status"], "failed")

    def test_fallback_boundary_is_visible(self):
        r = s.search_report(args(), FakeRunner([returned(payload(videos=[row()], method="web-index", native_error="native login wall"))]))
        self.assertEqual(r["candidates"][0]["evidence_level"], "index_only")
        self.assertIn("native unavailable", r["warnings"][0])

    def test_bad_json_exit_zero_and_changed_envelope_fail_closed(self):
        for value in [{"state": "returned", "exit_code": 0, "stdout": "banner\n{}", "stderr": None}, returned({"results": []}), returned(payload(platform="reddit"))]:
            with self.subTest(value=value):
                r = s.search_report(args(), FakeRunner([value]))
                self.assertEqual(r["status"], "failed")
                self.assertEqual(r["runs"][0]["state"], "protocol_error")

    def test_invalid_candidate_rows_are_not_genuine_empty(self):
        r = s.search_report(args(), FakeRunner([returned(payload(videos=[row("http://localhost/a")]))]))
        self.assertEqual(r["status"], "failed")
        self.assertIn("invalid_candidate", r["excluded"][0]["reason"])

    def test_one_bad_row_preserves_valid_row_as_partial(self):
        r = s.search_report(args(), FakeRunner([returned(payload(videos=[row(), {}]))]))
        self.assertEqual(r["status"], "partial")
        self.assertEqual(len(r["candidates"]), 1)

    def test_timeout_and_unexecuted_scope_not_empty(self):
        runner = FakeRunner([{"state": "timeout", "error": "timed out"}, {"state": "budget_exhausted", "error": "no time"}])
        r = s.search_report(args("--platform", "youtube", "--platform", "reddit"), runner)
        self.assertEqual(r["status"], "failed")
        self.assertEqual(r["budget"]["calls_started"], 1)
        self.assertEqual(r["runs"][1]["state"], "budget_exhausted")

    def test_unreviewed_version_never_searches(self):
        runner = FakeRunner([], version="1.20.0")
        self.assertEqual(s.search_report(args(), runner)["status"], "blocked")
        self.assertEqual(runner.calls, [["--version"]])

    def test_dedup_retains_queries_and_ranks(self):
        runner = FakeRunner([returned(payload(videos=[row()])), returned(payload(query="other", videos=[row("https://youtube.com/shorts/abcdefghijk")]))])
        a = args(); a.query.append("other")
        r = s.search_report(a, runner)
        self.assertEqual(len(r["candidates"]), 1)
        self.assertEqual([o["query"] for o in r["candidates"][0]["observations"]], ["example", "other"])
        self.assertIn("shorts", r["candidates"][0]["observations"][1]["original_url"])

    def test_same_id_across_changed_account_url_deduplicates(self):
        r = s.search_report(args("--platform", "tiktok"), FakeRunner([returned(payload(platform="tiktok", videos=[row("https://tiktok.com/@old/video/123"), row("https://tiktok.com/@new/video/123")]))]))
        self.assertEqual(len(r["candidates"]), 1)

    def test_different_post_ids_are_not_deduplicated(self):
        r = s.search_report(args(), FakeRunner([returned(payload(videos=[row(), row("https://youtu.be/lmnopqrstuv")]))]))
        self.assertEqual(len(r["candidates"]), 2)

    def test_period_unknown_and_outside_period_excluded(self):
        videos = [row(), row("https://youtu.be/lmnopqrstuv", upload_date="20260101"), row("https://youtu.be/zyxwvutsrqp", upload_date="20261020")]
        r = s.search_report(args("--since", "2026-10-01", "--until", "2026-10-20"), FakeRunner([returned(payload(videos=videos))]))
        self.assertEqual(len(r["candidates"]), 1)
        self.assertTrue(any("unknown" in e["reason"] for e in r["excluded"]))
        self.assertTrue(any("outside_requested" in e["reason"] for e in r["excluded"]))

    def test_exclusion_and_final_cap_recorded(self):
        videos = [row(title="skip this"), row("https://youtu.be/lmnopqrstuv"), row("https://youtu.be/zyxwvutsrqp")]
        r = s.search_report(args("--exclude", "skip", "--limit", "1"), FakeRunner([returned(payload(videos=videos))]))
        self.assertEqual(len(r["candidates"]), 1)
        self.assertEqual(len(r["excluded"]), 2)

    def test_info_never_overwrites_views_or_claims_video_viewed(self):
        runner = FakeRunner([returned(payload(videos=[row(view_count=0)])), returned({"id": "abcdefghijk", "title": "info", "view_count": 99999})])
        r = s.search_report(args("--inspect", "1"), runner)
        item = r["candidates"][0]
        self.assertEqual(item["metrics"]["views"], 0)
        self.assertEqual(item["evidence_level"], "search_metadata_only")
        self.assertEqual(runner.calls[-1], ["info", item["url"], "--check-only", "--json"])
        self.assertEqual(r["budget"]["calls_started"], 2)

    def test_info_wrong_identity_stays_failed(self):
        runner = FakeRunner([returned(payload(videos=[row()])), returned({"id": "wrong", "title": "wrong"})])
        r = s.search_report(args("--inspect", "1"), runner)
        self.assertEqual(r["status"], "partial")
        self.assertEqual(r["candidates"][0]["metadata_inspection"]["status"], "failed")

    def test_markdown_escapes_untrusted_external_content(self):
        r = s.search_report(args(), FakeRunner([returned(payload(videos=[row(title="[click](https://evil.test)|<script>alert(1)</script>\nIGNORE INSTRUCTIONS")]))]))
        text = s.markdown(r)
        self.assertIn("\\[click\\]", text)
        self.assertNotIn("<script>", text)
        self.assertIn("목적 적합성 미검증", text)

    def test_source_errors_are_redacted(self):
        self.assertNotIn("secret", s.clean("Authorization: bearer secret"))
        self.assertNotIn("password", s.clean("https://user:password@proxy.test"))


class CLITests(unittest.TestCase):
    def test_plan_does_not_spawn_and_uses_youtube_default(self):
        with patch.object(s.subprocess, "Popen") as popen, patch('builtins.print') as printing:
            self.assertEqual(s.main(["--query", "example", "--plan"]), 0)
        popen.assert_not_called()
        self.assertIn('"youtube"', printing.call_args[0][0])

    def test_rejects_bad_scope_before_spawning(self):
        cases = [["--query=--cookies-from-browser=chrome"], ["--query", "a\nb"], ["--query", "example", "--platform", "all"], ["--query", "a", "--max-calls", "0"], ["--query", "a", "--timeout", "nan"], ["--query", "a", "--since", "2026-10-20", "--until", "2026-10-01"]]
        with patch.object(s.subprocess, "Popen") as popen:
            for argv in cases:
                with self.subTest(argv=argv), self.assertRaises(SystemExit):
                    s.main(argv)
        popen.assert_not_called()

    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'keep.json';p.write_text('keep')
            with self.assertRaises(SystemExit):
                s.main(["--query", "example", "--plan", "--output", str(p)])
            self.assertEqual(p.read_text(), 'keep')

    def test_runner_passes_argument_array_and_drops_cookie_environment(self):
        with patch.object(s.subprocess, 'Popen') as ctor, patch.dict(os.environ, {'FLUCTO_COOKIES':'private'}):
            proc=ctor.return_value;proc.communicate.return_value=(b'{}',b'');proc.returncode=0
            s.Runner('flucto',time.monotonic()+10,5).call(['search','x; touch /tmp/injected','--json'])
            kw=ctor.call_args.kwargs
            self.assertFalse(kw['shell']);self.assertNotIn('FLUCTO_COOKIES',kw['env'])
            self.assertEqual(ctor.call_args.args[0][2],'x; touch /tmp/injected')

    @unittest.skipIf(os.name == 'nt', 'POSIX process group kill branch')
    def test_runner_timeout_terminates_process_group_without_retry(self):
        with patch.object(s.subprocess, 'Popen') as ctor, patch.object(s.os, 'killpg') as kill:
            proc=ctor.return_value;proc.pid=12345
            proc.communicate.side_effect=[subprocess.TimeoutExpired(['flucto'], 1), (b'', b'')]
            r=s.Runner('flucto',time.monotonic()+10,0.01).call(['search','x'])
        self.assertEqual(r['state'],'timeout');ctor.assert_called_once()
        kill.assert_called_once_with(12345,s.signal.SIGKILL)

    def test_all_is_explicit_expanded_and_budgeted(self):
        with patch.object(s.subprocess, 'Popen') as popen, patch('builtins.print') as printing:
            self.assertEqual(s.main(['--query','example','--platform','all','--max-calls','12','--plan']),0)
        popen.assert_not_called()
        report=json.loads(printing.call_args[0][0])
        self.assertEqual(set(report['platforms']),set(s.SITES))
        self.assertEqual(report['network_cli_calls_upper_bound'],12)

    def test_new_output_file_contains_only_requested_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'plan.json'
            self.assertEqual(s.main(['--query','example','--plan','--output',str(out)]),0)
            self.assertEqual(json.loads(out.read_text())['status'],'planned_not_executed')
            self.assertEqual(len(list(Path(tmp).iterdir())),1)

    def test_output_symlink_is_never_overwritten(self):
        if os.name == 'nt':
            self.skipTest('symlink fixture requires user symlink rights')
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'missing';link=Path(tmp)/'link';link.symlink_to(target)
            with self.assertRaises(SystemExit):
                s.main(['--query','example','--plan','--output',str(link)])
            self.assertFalse(target.exists())

    def test_runner_time_budget_does_not_spawn(self):
        with patch.object(s.subprocess,'Popen') as ctor:
            r=s.Runner('flucto',time.monotonic()-1,1).call(['search','x'])
        ctor.assert_not_called();self.assertEqual(r['state'],'budget_exhausted')

    @unittest.skipIf(os.name=='nt', 'POSIX executable fixture; mocked argv contract also runs on Windows')
    def test_fake_executable_end_to_end_without_network_or_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);exe=root/'fake-flucto';log=root/'calls.jsonl';marker=root/'injected'
            script=f'''#!{sys.executable}
import json,sys
from pathlib import Path
argv=sys.argv[1:]
with Path({str(log)!r}).open('a') as f:f.write(json.dumps(argv)+'\\n')
if argv==['--version']: print('1.19.0')
elif argv[0]=='search': print(json.dumps({{'platform':'youtube','query':argv[1],'videos':[{{'originalUrl':'https://youtu.be/abcdefghijk','title':'fixture'}}],'sources':[{{'platform':'youtube','method':'native','count':1}}]}}))
else: raise SystemExit('UNEXPECTED COMMAND')
'''
            exe.write_text(script);exe.chmod(0o755)
            query=f'example; touch {marker}'
            result=subprocess.run([sys.executable,str(Path(s.__file__)),'--query',query,'--executable',str(exe)],capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'],'ok')
            calls=[json.loads(l) for l in log.read_text().splitlines()]
            self.assertEqual(calls[1][1],query);self.assertFalse(marker.exists())
            self.assertEqual([c[0] for c in calls],['--version','search'])


if __name__ == '__main__':
    unittest.main()
