"""Keyword-based grading of a typed answer. Not an AI judge: it checks coverage of the key terms."""
import re


def _norm(s):
    return re.sub(r"[^a-z0-9.:\- ]+", " ", s.lower())


def grade(question, response):
    """Return (score 0..1, hit keywords, missed keywords). Accepts simple plurals and hyphen/space variants."""
    text = " " + _norm(response).replace("-", " ") + " "
    hits, misses = [], []
    for kw in question.keywords:
        k = _norm(kw).replace("-", " ").strip()
        pat = r"(?<![a-z0-9])" + re.escape(k) + r"(s|es|ing|ed)?(?![a-z0-9])"
        (hits if re.search(pat, text) else misses).append(kw)
    score = len(hits) / len(question.keywords) if question.keywords else 0.0
    return score, hits, misses


def verdict(score):
    return "strong" if score >= 0.75 else "partial" if score >= 0.4 else "weak"
