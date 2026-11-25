"""Log-triage drills. Each scenarios/*.json has: id, title, difficulty, logs (list of lines), question,
verdict (true_positive | false_positive | needs_more_data), keywords, explanation."""
import glob
import json
import os

from .bank import ROOT

VERDICTS = ("true_positive", "false_positive", "needs_more_data")


def load(path=None):
    path = path or os.path.join(ROOT, "scenarios")
    out = []
    for f in sorted(glob.glob(os.path.join(path, "*.json"))):
        with open(f, encoding="utf-8") as fh:
            s = json.load(fh)
        for k in ("id", "title", "logs", "question", "verdict", "keywords", "explanation"):
            if k not in s:
                raise ValueError("%s missing %s" % (f, k))
        if s["verdict"] not in VERDICTS:
            raise ValueError("%s: bad verdict" % f)
        out.append(s)
    return out


def score(scenario, verdict, explanation):
    """Verdict is worth 50%, explanation keyword coverage 50%."""
    from .grade import grade
    from .bank import Question
    q = Question(scenario["id"], scenario["question"], scenario["explanation"], "scenario", 1, tuple(scenario["keywords"]))
    kw_score, hits, misses = grade(q, explanation)
    return (0.5 if verdict == scenario["verdict"] else 0.0) + 0.5 * kw_score, hits, misses
