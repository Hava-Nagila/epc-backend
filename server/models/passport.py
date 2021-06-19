import json
from pathlib import Path


class Passport:
    def __init__(
        self,
        file_name,
        prog_name=None,
        hours_cnt=0,
        hours_prac=0,
        online=False,
        difficulty=None,
    ):
        self.file_name = file_name or ""
        self.prog_name = prog_name or ""
        self.hours_cnt = hours_cnt or 0
        self.hours_prac = hours_prac or 0
        self.online = online or False
        self.difficulty = difficulty or None
        self.min_listeners = 0
        self.max_listeners = 0
        self.taxonomies = set()
        self.taxonomy = 0
        self.expected_taxonomy_match = 0
        self.reviews = [0, 0, 0]

    def __repr__(self):
        if self.max_listeners < self.min_listeners:
            self.max_listeners = self.min_listeners
        return json.dumps(
            {
                "file_name": Path(self.file_name).name,
                "prog_name": self.prog_name,
                "hours_total": self.hours_cnt,
                "hours_prac": self.hours_prac,
                "online": self.online,
                "difficulty": self.difficulty,
                "min_listeners": self.min_listeners,
                "max_listeners": self.max_listeners,
                "taxonomies": list(self.taxonomies),
                "taxonomy": self.taxonomy,
                "expected_taxonomy_match": self.expected_taxonomy_match,
                "positive_reviews": self.reviews[0],
                "neutral_reviews": self.reviews[1],
                "negative_reviews": self.reviews[2],
            },
            ensure_ascii=False,
        )