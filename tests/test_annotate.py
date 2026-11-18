# -*- coding: utf-8 -*-
"""Tests for the annotation helper."""

import json
import tempfile
import unittest
from pathlib import Path

from eval.annotate import build_template, load_raw, summarize_annotation, write_json
from eval.convergence_metrics import InputError


class LoadRawTest(unittest.TestCase):
    def test_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "raw.jsonl"
            path.write_text(
                "\n".join(
                    [
                        json.dumps({"turn": 2, "user": "b", "assistant": "B"}),
                        json.dumps({"turn": 1, "user": "a", "assistant": "A"}),
                    ]
                ),
                encoding="utf-8",
            )
            turns = load_raw(path)
            self.assertEqual([t["turn"] for t in turns], [1, 2])

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "raw.jsonl"
            path.write_text("{not json}\n", encoding="utf-8")
            with self.assertRaises(InputError):
                load_raw(path)

    def test_duplicate_turn(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "raw.jsonl"
            path.write_text(
                "\n".join(
                    [
                        json.dumps({"turn": 1}),
                        json.dumps({"turn": 1}),
                    ]
                ),
                encoding="utf-8",
            )
            with self.assertRaises(InputError):
                load_raw(path)

    def test_non_string_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "raw.jsonl"
            path.write_text(
                json.dumps({"turn": 1, "user": 123}) + "\n", encoding="utf-8"
            )
            with self.assertRaises(InputError):
                load_raw(path)


class TemplateTest(unittest.TestCase):
    def test_shape(self):
        raw = [
            {"turn": 1, "user": "a", "assistant": "A"},
            {"turn": 2, "user": "b", "assistant": "B"},
        ]
        template = build_template(raw)
        self.assertEqual(len(template), 2)
        self.assertEqual(template[0]["concepts"], [])
        self.assertEqual(template[1]["turn"], 2)
        self.assertIn("note", template[0])

    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw_path = Path(tmp) / "raw.jsonl"
            out_path = Path(tmp) / "ann.json"
            raw_path.write_text(
                json.dumps({"turn": 1, "user": "a", "assistant": "A"}) + "\n",
                encoding="utf-8",
            )
            write_json(out_path, build_template(load_raw(raw_path)))
            data = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(data[0]["turn"], 1)


class SummaryTest(unittest.TestCase):
    def test_summary_on_sample(self):
        root = Path(__file__).resolve().parents[1]
        result = summarize_annotation(root / "eval" / "sample_data.json")
        self.assertEqual(result["turns"], 5)
        self.assertAlmostEqual(result["concept_reuse_rate"], 0.6, places=4)
        self.assertEqual(result["empty_concept_turns"], [])


if __name__ == "__main__":
    unittest.main()
