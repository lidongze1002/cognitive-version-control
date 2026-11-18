# -*- coding: utf-8 -*-
"""Validate the experiment scripts."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = sorted((ROOT / "experiments" / "scripts").glob("*.json"))
FORBIDDEN = ["改口", "修正", "推翻", "账本", "CVC", "重置", "请更新"]


class ScriptsTest(unittest.TestCase):
    def test_three_scripts(self):
        self.assertEqual(len(SCRIPTS), 3)

    def test_each_script(self):
        ids = set()
        for path in SCRIPTS:
            data = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(script=path.name):
                self.assertIn("id", data)
                self.assertNotIn(data["id"], ids)
                ids.add(data["id"])

                turns = data.get("turns", [])
                self.assertEqual(len(turns), 10)
                self.assertEqual([t["turn"] for t in turns], list(range(1, 11)))
                self.assertEqual(data.get("fact_turn"), 5)
                self.assertTrue(data.get("fact"))

                for turn in turns:
                    prompt = turn["prompt"]
                    self.assertTrue(prompt.strip())
                    for word in FORBIDDEN:
                        self.assertNotIn(
                            word,
                            prompt,
                            f"{path.name} turn {turn['turn']} leaks '{word}'",
                        )

    def test_conflict_fact_is_at_turn_five(self):
        for path in SCRIPTS:
            data = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(script=path.name):
                fact_words = ["6.66", "3850", "1158"]
                turn5 = data["turns"][4]["prompt"]
                self.assertTrue(
                    any(word in turn5 for word in fact_words),
                    f"{path.name} turn 5 does not contain the conflict fact",
                )


if __name__ == "__main__":
    unittest.main()
