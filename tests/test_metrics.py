# -*- coding: utf-8 -*-
"""Tests for the CVC metrics reference implementation."""

import unittest

from eval.convergence_metrics import (
    BAD_DEMO,
    GOOD_DEMO,
    InputError,
    belief_revision_latency,
    concept_reuse_rate,
    frame_entropy,
    revision_diagnostics,
    summarize,
    validate_turns,
)


class ReuseRateTest(unittest.TestCase):
    def test_bad_demo(self):
        self.assertAlmostEqual(concept_reuse_rate(BAD_DEMO), 0.6, places=4)

    def test_good_demo(self):
        self.assertAlmostEqual(concept_reuse_rate(GOOD_DEMO), 1 / 3, places=4)

    def test_empty(self):
        self.assertEqual(concept_reuse_rate([]), 0.0)


class EntropyTest(unittest.TestCase):
    def test_bad_demo(self):
        self.assertAlmostEqual(frame_entropy(BAD_DEMO), 0.8805, places=3)

    def test_good_demo(self):
        self.assertAlmostEqual(frame_entropy(GOOD_DEMO), 0.9592, places=3)

    def test_uniform(self):
        turns = [{"turn": 1, "concepts": ["a", "b", "c", "d"]}]
        self.assertAlmostEqual(frame_entropy(turns), 1.0, places=6)

    def test_single_concept(self):
        turns = [{"turn": 1, "concepts": ["a", "a", "a"]}]
        self.assertEqual(frame_entropy(turns), 0.0)

    def test_empty(self):
        self.assertEqual(frame_entropy([]), 0.0)


class LatencyTest(unittest.TestCase):
    def test_bad_demo(self):
        self.assertIsNone(belief_revision_latency(BAD_DEMO))

    def test_good_demo(self):
        self.assertEqual(belief_revision_latency(GOOD_DEMO), 0.0)

    def test_same_turn(self):
        turns = [
            {"turn": 1, "facts_introduced": ["F-1"], "facts_revised": ["F-1"]},
        ]
        self.assertEqual(belief_revision_latency(turns), 0.0)

    def test_duplicate_revision_counts_once(self):
        turns = [
            {"turn": 1, "facts_introduced": ["F-1"], "facts_revised": []},
            {"turn": 2, "facts_introduced": [], "facts_revised": ["F-1"]},
            {"turn": 3, "facts_introduced": [], "facts_revised": ["F-1"]},
        ]
        self.assertEqual(belief_revision_latency(turns), 1.0)

    def test_late_revision_without_new_fact(self):
        turns = [
            {"turn": 1, "facts_introduced": ["F-1"], "facts_revised": []},
            {"turn": 2, "facts_introduced": [], "facts_revised": []},
            {"turn": 3, "facts_introduced": [], "facts_revised": []},
            {"turn": 4, "facts_introduced": [], "facts_revised": ["F-1"]},
        ]
        self.assertEqual(belief_revision_latency(turns), 3.0)

    def test_no_revision(self):
        turns = [{"turn": 1, "facts_introduced": ["F-1"], "facts_revised": []}]
        self.assertIsNone(belief_revision_latency(turns))


class DiagnosticsTest(unittest.TestCase):
    def test_unrevised(self):
        diag = revision_diagnostics(BAD_DEMO)
        self.assertEqual(diag["unrevised_facts"], ["F-012", "F-017"])
        self.assertEqual(diag["orphan_revisions"], [])

    def test_orphan_revision(self):
        turns = [
            {"turn": 1, "facts_introduced": [], "facts_revised": ["F-9"]},
        ]
        diag = revision_diagnostics(turns)
        self.assertEqual(diag["orphan_revisions"], ["F-9"])


class ValidationTest(unittest.TestCase):
    def test_top_level_must_be_list(self):
        with self.assertRaises(InputError):
            validate_turns({"turn": 1})

    def test_empty_list_rejected(self):
        with self.assertRaises(InputError):
            validate_turns([])

    def test_duplicate_turn_rejected(self):
        with self.assertRaises(InputError):
            validate_turns(
                [
                    {"turn": 1, "concepts": []},
                    {"turn": 1, "concepts": []},
                ]
            )

    def test_bool_turn_rejected(self):
        with self.assertRaises(InputError):
            validate_turns([{"turn": True, "concepts": []}])

    def test_missing_fields_default_to_empty(self):
        turns = validate_turns([{"turn": 0}])
        self.assertEqual(turns[0]["concepts"], [])
        self.assertEqual(turns[0]["facts_introduced"], [])

    def test_sorted_by_turn(self):
        turns = validate_turns(
            [
                {"turn": 2, "concepts": ["b"]},
                {"turn": 1, "concepts": ["a"]},
            ]
        )
        self.assertEqual([t["turn"] for t in turns], [1, 2])


class SummaryTest(unittest.TestCase):
    def test_bad_demo_warns(self):
        result = summarize(validate_turns(BAD_DEMO))
        self.assertEqual(result["turns"], 5)
        self.assertAlmostEqual(result["cvc_score"], 0.4241, places=3)
        self.assertTrue(any("fixation" in w for w in result["warnings"]))
        self.assertTrue(any("no revisions" in w for w in result["warnings"]))

    def test_good_demo_has_no_latency_warning(self):
        result = summarize(validate_turns(GOOD_DEMO))
        self.assertFalse(any("stickiness" in w for w in result["warnings"]))
        self.assertEqual(result["belief_revision_latency"], 0.0)


if __name__ == "__main__":
    unittest.main()
