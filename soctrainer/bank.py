"""Question bank loader. Files in bank/*.md use this format:

### Q: Question text?
- domain: windows
- level: 2
- keywords: 4769, RC4, service account
A: Model answer, which may run over several lines.
"""
import glob
import os
import re
from dataclasses import dataclass
from typing import List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass(frozen=True)
class Question:
    id: str
    text: str
    answer: str
    domain: str
    level: int
    keywords: tuple


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def parse(text, source=""):
    out = []
    blocks = re.split(r"^### Q:\s*", text, flags=re.M)[1:]
    for block in blocks:
        lines = block.strip().splitlines()
        question = lines[0].strip()
        meta, answer, in_answer = {}, [], False
        for ln in lines[1:]:
            if in_answer:
                answer.append(ln)
            elif ln.startswith("A:"):
                in_answer = True
                answer.append(ln[2:].strip())
            else:
                m = re.match(r"-\s*(\w+):\s*(.*)$", ln)
                if m:
                    meta[m.group(1)] = m.group(2).strip()
        if not answer or "domain" not in meta:
            raise ValueError("%s: question %r is missing an answer or domain" % (source, question))
        kws = tuple(k.strip() for k in meta.get("keywords", "").split(",") if k.strip())
        out.append(Question(_slug(question), question, " ".join(" ".join(answer).split()), meta["domain"], int(meta.get("level", 1)), kws))
    return out


def load(path=None) -> List[Question]:
    path = path or os.path.join(ROOT, "bank")
    qs = []
    for f in sorted(glob.glob(os.path.join(path, "*.md"))):
        with open(f, encoding="utf-8") as fh:
            qs.extend(parse(fh.read(), f))
    ids = [q.id for q in qs]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError("duplicate question ids: %s" % ", ".join(sorted(dupes)))
    return qs


def filter_questions(qs, domain=None, level=None, search=None):
    out = qs
    if domain:
        out = [q for q in out if q.domain == domain]
    if level:
        out = [q for q in out if q.level <= level]
    if search:
        s = search.lower()
        out = [q for q in out if s in q.text.lower() or s in q.answer.lower()]
    return out
