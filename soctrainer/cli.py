import argparse
import os
import random
import sys
import time

from . import bank, export, grade, scenarios
from .srs import Progress

DEFAULT_PROGRESS = os.path.expanduser("~/.soctrainer.json")


def _questions(a):
    qs = bank.filter_questions(bank.load(), a.domain, a.level, getattr(a, "search", None))
    if not qs:
        sys.exit("no questions match those filters")
    return qs


def ask(q, input_fn, out, self_grade=False):
    """Ask one question. Returns (score, correct)."""
    out("\n[%s | level %d]  %s" % (q.domain, q.level, q.text))
    resp = input_fn("your answer (blank to skip): ").strip()
    score, hits, misses = grade.grade(q, resp) if resp else (0.0, [], list(q.keywords))
    out("\nModel answer: " + q.answer)
    if resp:
        out("Key terms covered: %d/%d (%s)" % (len(hits), len(q.keywords), grade.verdict(score)))
        if misses:
            out("Missed terms: " + ", ".join(misses))
    if self_grade:
        correct = input_fn("did you get it? [y/N]: ").strip().lower().startswith("y")
    else:
        correct = score >= 0.6
    return score, correct


def cmd_quiz(a, input_fn=input, out=print):
    qs = _questions(a)
    prog = Progress(a.progress)
    picked = prog.pick(qs, a.count)
    right = 0
    for q in picked:
        _, ok = ask(q, input_fn, out, a.self_grade)
        prog.record(q.id, ok)
        right += ok
    prog.save()
    out("\nScore: %d/%d" % (right, len(picked)))
    return 0


def cmd_mock(a, input_fn=input, out=print):
    qs = _questions(a)
    rng = random.Random(a.seed)
    picked = rng.sample(qs, min(a.count, len(qs)))
    out("Mock interview: %d questions, aim for %d seconds each. Answer in full sentences." % (len(picked), a.seconds))
    total, slow = 0.0, 0
    for q in picked:
        t0 = time.time()
        score, _ = ask(q, input_fn, out, False)
        took = time.time() - t0
        if took > a.seconds:
            slow += 1
            out("(took %ds, over the %ds target)" % (took, a.seconds))
        total += score
    pct = round(100 * total / len(picked))
    out("\nOverall keyword coverage: %d%%. Over time on %d questions." % (pct, slow))
    return 0


def cmd_drill(a, input_fn=input, out=print):
    sc = scenarios.load()
    if a.id:
        sc = [s for s in sc if s["id"] == a.id]
        if not sc:
            sys.exit("unknown scenario id")
    else:
        sc = [random.Random(a.seed).choice(sc)]
    s = sc[0]
    out("\n== %s (%s) ==" % (s["title"], s.get("difficulty", "")))
    for ln in s["logs"]:
        out("  " + ln)
    out("\n" + s["question"])
    v = ""
    while v not in scenarios.VERDICTS:
        v = input_fn("verdict (true_positive / false_positive / needs_more_data): ").strip()
    expl = input_fn("explain your reasoning and next steps: ")
    sc_score, hits, misses = scenarios.score(s, v, expl)
    out("\nCorrect verdict: %s. Your score: %d%%" % (s["verdict"], round(sc_score * 100)))
    out("Explanation: " + s["explanation"])
    if misses:
        out("Terms you did not mention: " + ", ".join(misses))
    return 0


def cmd_stats(a):
    qs = bank.load()
    prog = Progress(a.progress)
    st = prog.stats(qs)
    print("cards: %(cards)d  seen: %(seen)d  accuracy: %(accuracy)s  mastered (box 5): %(mastered)d" % st)
    print("boxes:", " ".join("%d:%d" % kv for kv in st["by_box"].items()))
    weak = prog.weak_domains(qs)
    if weak:
        print("weakest domains:", ", ".join("%s (%.0f%%)" % (d, 100 * x) for d, x in weak[:3]))
    return 0


def cmd_list(a):
    qs = _questions(a)
    for q in qs:
        print("%-12s L%d  %s" % (q.domain, q.level, q.text))
    print("\n%d questions" % len(qs))
    return 0


def cmd_export(a):
    qs = bank.load()
    if a.format == "anki":
        text = export.anki_csv(qs)
    else:
        text = export.flashcards_html(qs)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote %d cards to %s" % (len(qs), a.out))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="soctrainer", description="SOC analyst interview trainer")
    p.add_argument("--progress", default=DEFAULT_PROGRESS, help="progress file (default ~/.soctrainer.json)")
    sub = p.add_subparsers(dest="cmd", required=True)

    def filt(s):
        s.add_argument("--domain")
        s.add_argument("--level", type=int, choices=[1, 2, 3], help="maximum level")
        return s

    s = filt(sub.add_parser("quiz", help="spaced-repetition quiz"))
    s.add_argument("-n", "--count", type=int, default=5)
    s.add_argument("--self-grade", action="store_true")
    s.set_defaults(fn=cmd_quiz)
    s = filt(sub.add_parser("mock", help="timed mock interview"))
    s.add_argument("-n", "--count", type=int, default=8)
    s.add_argument("--seconds", type=int, default=90)
    s.add_argument("--seed", type=int)
    s.set_defaults(fn=cmd_mock)
    s = sub.add_parser("drill", help="log triage scenario")
    s.add_argument("--id")
    s.add_argument("--seed", type=int)
    s.set_defaults(fn=cmd_drill)
    sub.add_parser("stats").set_defaults(fn=cmd_stats)
    s = filt(sub.add_parser("list"))
    s.add_argument("--search")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("export")
    s.add_argument("format", choices=["anki", "html"])
    s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_export)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
