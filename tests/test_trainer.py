import csv
import io
import json
import os
import tempfile
import unittest
from datetime import date, timedelta

from soctrainer import bank, cli, export, grade, scenarios
from soctrainer.srs import Progress

Q = bank.parse("""### Q: What is Kerberoasting?
- domain: windows
- level: 2
- keywords: 4769, RC4, service account
A: Requesting service tickets (4769) for service accounts
and cracking the RC4 encrypted part offline.
""")[0]


class ParseTests(unittest.TestCase):
    def test_multiline_answer_and_meta(self):
        self.assertEqual(Q.level, 2)
        self.assertEqual(Q.keywords, ("4769", "RC4", "service account"))
        self.assertIn("offline", Q.answer)
        self.assertNotIn("\n", Q.answer)

    def test_missing_answer_rejected(self):
        with self.assertRaises(ValueError):
            bank.parse("### Q: x?\n- domain: a\n")

    def test_filter(self):
        qs = bank.load()
        self.assertTrue(all(q.domain == "windows" for q in bank.filter_questions(qs, domain="windows")))
        self.assertTrue(all(q.level == 1 for q in bank.filter_questions(qs, level=1)))
        self.assertTrue(bank.filter_questions(qs, search="kerberos"))


class BankQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qs = bank.load()

    def test_enough_questions_across_domains(self):
        self.assertGreaterEqual(len(self.qs), 60)
        self.assertGreaterEqual(len({q.domain for q in self.qs}), 8)

    def test_ids_unique_and_levels_valid(self):
        self.assertEqual(len({q.id for q in self.qs}), len(self.qs))
        self.assertTrue(all(q.level in (1, 2, 3) for q in self.qs))

    def test_model_answers_cover_their_own_keywords(self):
        for q in self.qs:
            score, _, miss = grade.grade(q, q.answer)
            self.assertEqual(miss, [], q.id)
            self.assertGreaterEqual(len(q.keywords), 3, q.id)

    def test_keyword_stuffing_scores_the_same_as_prose(self):
        q = next(q for q in self.qs if "kerberoasting" in q.text.lower())
        self.assertEqual(grade.grade(q, " ".join(q.keywords))[0], 1.0)

    def test_scenarios_valid(self):
        sc = scenarios.load()
        self.assertGreaterEqual(len(sc), 6)
        self.assertEqual({s["verdict"] for s in sc}, set(scenarios.VERDICTS))
        for s in sc:
            score, _, miss = scenarios.score(s, s["verdict"], s["explanation"])
            self.assertEqual(miss, [], s["id"])
            self.assertEqual(score, 1.0)


class GradeTests(unittest.TestCase):
    def test_partial_and_plural_and_case(self):
        score, hits, miss = grade.grade(Q, "Event 4769 and service accounts")
        self.assertEqual(hits, ["4769", "service account"])
        self.assertEqual(miss, ["RC4"])
        self.assertAlmostEqual(score, 2 / 3)
        self.assertEqual(grade.verdict(score), "partial")

    def test_no_substring_false_hits(self):
        q = bank.parse("### Q: t\n- domain: d\n- keywords: IP\nA: ip addresses\n")[0]
        self.assertEqual(grade.grade(q, "script descriptions")[0], 0.0)

    def test_empty_response(self):
        self.assertEqual(grade.grade(Q, "")[0], 0.0)


class SrsTests(unittest.TestCase):
    def test_box_moves_and_resets(self):
        p = Progress()
        today = date(2026, 3, 1)
        p.record("a", True, today)
        p.record("a", True, today)
        self.assertEqual(p.card("a")["box"], 3)
        self.assertEqual(p.card("a")["due"], (today + timedelta(days=3)).isoformat())
        p.record("a", False, today)
        self.assertEqual(p.card("a")["box"], 1)

    def test_box_capped_at_five(self):
        p = Progress()
        for _ in range(10):
            p.record("a", True, date(2026, 3, 1))
        self.assertEqual(p.card("a")["box"], 5)

    def test_due_logic(self):
        p = Progress()
        p.record("a", True, date(2026, 3, 1))
        self.assertFalse(p.is_due("a", date(2026, 3, 1)))
        self.assertTrue(p.is_due("a", date(2026, 3, 2)))
        self.assertTrue(p.is_due("never-seen", date(2026, 3, 1)))

    def test_pick_prefers_due_low_box_and_no_duplicates(self):
        qs = bank.load()[:10]
        p = Progress()
        today = date(2026, 3, 1)
        for q in qs[:5]:
            p.record(q.id, True, today)
        picked = p.pick(qs, 6, today)
        self.assertEqual(len({q.id for q in picked}), 6)
        self.assertTrue(all(p.is_due(q.id, today) for q in picked[:5]))

    def test_save_and_load(self):
        path = os.path.join(tempfile.mkdtemp(), "p.json")
        p = Progress(path)
        p.record("a", True)
        p.save()
        self.assertEqual(Progress(path).card("a")["seen"], 1)

    def test_weak_domains_sorted(self):
        qs = bank.load()
        w = next(q for q in qs if q.domain == "windows")
        n = next(q for q in qs if q.domain == "network")
        p = Progress()
        p.record(w.id, False)
        p.record(n.id, True)
        self.assertEqual(p.weak_domains(qs)[0][0], "windows")


class ExportTests(unittest.TestCase):
    def test_anki_roundtrip(self):
        text = export.anki_csv([Q])
        row = next(csv.reader(io.StringIO(text), delimiter="\t"))
        self.assertEqual(row[0], Q.text)
        self.assertEqual(row[1], Q.answer)

    def test_html_embeds_safely(self):
        evil = bank.parse("### Q: </script><b>x\n- domain: a<b\n- keywords: x\nA: <img src=x onerror=1>\n")[0]
        out = export.flashcards_html([evil])
        self.assertNotIn("</script><b>", out)
        self.assertNotIn("<img src=x", out)
        self.assertNotIn("<option value=\"a<b\">", out)


class CliTests(unittest.TestCase):
    def run_cli(self, argv, inputs):
        it = iter(inputs)
        out = []
        import argparse
        ns = cli.main.__globals__["argparse"].Namespace
        return it, out

    def test_ask_auto_grading(self):
        out = []
        score, ok = cli.ask(Q, lambda prompt: "4769 RC4 service account", out.append)
        self.assertTrue(ok)
        self.assertEqual(score, 1.0)
        score, ok = cli.ask(Q, lambda prompt: "no idea", out.append)
        self.assertFalse(ok)

    def test_quiz_updates_progress(self):
        path = os.path.join(tempfile.mkdtemp(), "p.json")
        import argparse
        a = argparse.Namespace(domain="windows", level=None, search=None, progress=path, count=2, self_grade=False)
        out = []
        cli.cmd_quiz(a, input_fn=lambda prompt: "", out=out.append)
        data = json.load(open(path))
        self.assertEqual(len(data), 2)
        self.assertTrue(any("Score:" in line for line in out))

    def test_drill_scoring(self):
        import argparse
        a = argparse.Namespace(id="av-lsass", seed=None)
        answers = iter(["false_positive", "It is Defender MsMpEng, a legitimate signed path, add an allow rule"])
        out = []
        cli.cmd_drill(a, input_fn=lambda prompt: next(answers), out=out.append)
        self.assertTrue(any("Correct verdict: false_positive" in l for l in out))


if __name__ == "__main__":
    unittest.main()
