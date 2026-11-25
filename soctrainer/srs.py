"""Leitner spaced repetition. Five boxes; a correct answer moves a card up, a miss sends it to box 1.
State is a JSON file mapping question id -> {box, due, seen, correct}."""
import json
import os
import random
from datetime import date, timedelta

INTERVALS = {1: 0, 2: 1, 3: 3, 4: 7, 5: 21}


class Progress:
    def __init__(self, path=None):
        self.path = path
        self.cards = {}
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                self.cards = json.load(fh)

    def save(self):
        if self.path:
            with open(self.path, "w", encoding="utf-8") as fh:
                json.dump(self.cards, fh, indent=1, sort_keys=True)

    def card(self, qid):
        return self.cards.get(qid, {"box": 1, "due": None, "seen": 0, "correct": 0})

    def record(self, qid, correct, today=None):
        today = today or date.today()
        c = self.card(qid)
        c["seen"] += 1
        if correct:
            c["correct"] += 1
            c["box"] = min(5, c["box"] + 1)
        else:
            c["box"] = 1
        c["due"] = (today + timedelta(days=INTERVALS[c["box"]])).isoformat()
        self.cards[qid] = c
        return c

    def is_due(self, qid, today=None):
        today = today or date.today()
        c = self.cards.get(qid)
        return c is None or c["due"] is None or date.fromisoformat(c["due"]) <= today

    def pick(self, questions, n, today=None, rng=None):
        """Due cards first (lowest box first), then fill with the rest. Never returns duplicates."""
        rng = rng or random.Random()
        due = [q for q in questions if self.is_due(q.id, today)]
        rng.shuffle(due)
        due.sort(key=lambda q: self.card(q.id)["box"])
        rest = [q for q in questions if q not in due]
        rng.shuffle(rest)
        return (due + rest)[:n]

    def stats(self, questions):
        by_box = {b: 0 for b in range(1, 6)}
        seen = correct = 0
        for q in questions:
            c = self.card(q.id)
            by_box[c["box"]] += 1
            seen += c["seen"]
            correct += c["correct"]
        return {"cards": len(questions), "by_box": by_box, "seen": seen, "accuracy": round(correct / seen, 2) if seen else None,
                "mastered": by_box[5]}

    def weak_domains(self, questions):
        agg = {}
        for q in questions:
            c = self.card(q.id)
            if c["seen"]:
                d = agg.setdefault(q.domain, [0, 0])
                d[0] += c["correct"]
                d[1] += c["seen"]
        return sorted(((dom, round(a / b, 2)) for dom, (a, b) in agg.items()), key=lambda x: x[1])
