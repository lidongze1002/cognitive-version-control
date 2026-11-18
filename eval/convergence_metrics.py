#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convergence metrics for long LLM conversations.

Three metrics:
  1. concept_reuse_rate       -- how often concepts repeat
  2. frame_entropy            -- normalized Shannon entropy of concept usage
  3. belief_revision_latency  -- turns between a new fact and its first revision

No third-party dependencies.

Usage:
    python eval/convergence_metrics.py --demo
    python eval/convergence_metrics.py --demo-good
    python eval/convergence_metrics.py --input eval/sample_data.json
    python eval/convergence_metrics.py --input data.json --json
    python eval/convergence_metrics.py --input data.json --markdown

Input format (list of turns):
[
  {"turn": 1, "concepts": ["利差"], "facts_introduced": ["F-012"], "facts_revised": []},
  {"turn": 2, "concepts": ["利差", "水池"], "facts_introduced": ["F-017"], "facts_revised": ["F-012"]}
]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

__version__ = "0.2.4"


class InputError(ValueError):
    """Raised when the input JSON does not match the expected schema."""


def _require_str_list(value: Any, field: str, index: int) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise InputError(f"turn[{index}].{field} must be a list of strings")
    return value


def validate_turns(data: Any) -> List[Dict[str, Any]]:
    """Validate and normalize a list of turns.

    Raises InputError with a precise message on the first problem found.
    """
    if not isinstance(data, list):
        raise InputError("top-level JSON must be a list of turns")
    if not data:
        raise InputError("turn list is empty")

    normalized: List[Dict[str, Any]] = []
    seen_turns = set()

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise InputError(f"turn[{index}] must be an object")

        turn = item.get("turn")
        if isinstance(turn, bool) or not isinstance(turn, int) or turn < 0:
            raise InputError(f"turn[{index}].turn must be a non-negative integer")
        if turn in seen_turns:
            raise InputError(f"duplicate turn number: {turn}")
        seen_turns.add(turn)

        concepts = _require_str_list(item.get("concepts", []), "concepts", index)
        introduced = _require_str_list(
            item.get("facts_introduced", []), "facts_introduced", index
        )
        revised = _require_str_list(
            item.get("facts_revised", []), "facts_revised", index
        )

        normalized.append(
            {
                "turn": turn,
                "concepts": concepts,
                "facts_introduced": introduced,
                "facts_revised": revised,
            }
        )

    return sorted(normalized, key=lambda x: x["turn"])


def load_turns(path: str | Path) -> List[Dict[str, Any]]:
    with open(path, encoding="utf-8") as fh:
        return validate_turns(json.load(fh))


def concept_reuse_rate(turns: Iterable[Dict[str, Any]]) -> float:
    """Repeated concept occurrences / total concept occurrences."""
    seen = set()
    reused = 0
    total = 0
    for turn in turns:
        for concept in turn.get("concepts", []):
            total += 1
            if concept in seen:
                reused += 1
            else:
                seen.add(concept)
    return reused / total if total else 0.0


def frame_entropy(turns: Iterable[Dict[str, Any]], normalized: bool = True) -> float:
    """Shannon entropy of concept frequencies.

    Returns a value in [0, 1] when normalized=True.
    """
    counts: Counter[str] = Counter()
    for turn in turns:
        counts.update(turn.get("concepts", []))
    total = sum(counts.values())
    if total == 0:
        return 0.0
    entropy = -sum((c / total) * math.log2(c / total) for c in counts.values())
    if not normalized:
        return entropy
    k = len(counts)
    if k <= 1:
        return 0.0
    return entropy / math.log2(k)


def belief_revision_latency(turns: Iterable[Dict[str, Any]]) -> Optional[float]:
    """Average delay between the latest new fact and a revision.

    For every fact that was revised, the clock starts at the most recent turn
    (at or before the revision) on which *any* fact was introduced. This
    measures "did the model revise when the contradicting evidence arrived?",
    not "how old is the belief?".

    A revision on the same turn as the new fact counts as 0. Returns None if
    no revision happened.
    """
    fact_turns: List[int] = []
    first_revision: Dict[str, int] = {}

    for turn in turns:
        turn_no = int(turn.get("turn", 0))
        for _fact_id in turn.get("facts_introduced", []):
            fact_turns.append(turn_no)
        for fact_id in turn.get("facts_revised", []):
            first_revision.setdefault(fact_id, turn_no)

    if not first_revision:
        return None

    latencies: List[float] = []
    for revision_turn in first_revision.values():
        candidates = [t for t in fact_turns if t <= revision_turn]
        if not candidates:
            continue
        latencies.append(revision_turn - max(candidates))

    return sum(latencies) / len(latencies) if latencies else None


def revision_diagnostics(turns: Iterable[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Return facts that were never revised and revisions of unknown facts."""
    introduced: Dict[str, int] = {}
    revised = set()
    orphan = set()

    for turn in turns:
        for fact_id in turn.get("facts_introduced", []):
            introduced.setdefault(fact_id, int(turn.get("turn", 0)))
        for fact_id in turn.get("facts_revised", []):
            if fact_id in introduced:
                revised.add(fact_id)
            else:
                orphan.add(fact_id)

    return {
        "unrevised_facts": sorted(f for f in introduced if f not in revised),
        "orphan_revisions": sorted(orphan),
    }


def summarize(turns: List[Dict[str, Any]]) -> Dict[str, Any]:
    reuse = concept_reuse_rate(turns)
    entropy = frame_entropy(turns)
    latency = belief_revision_latency(turns)
    diagnostics = revision_diagnostics(turns)
    has_introduced = any(t.get("facts_introduced") for t in turns)

    if latency is None:
        # Never revising is worse than revising late.
        score_latency = 0.0 if has_introduced else 0.5
    else:
        score_latency = max(0.0, 1.0 - latency / 3.0)

    score = 0.4 * (1 - reuse) + 0.3 * entropy + 0.3 * score_latency

    return {
        "turns": len(turns),
        "concept_reuse_rate": round(reuse, 4),
        "frame_entropy": round(entropy, 4),
        "belief_revision_latency": None if latency is None else round(latency, 2),
        "cvc_score": round(score, 4),
        "warnings": _warnings(reuse, entropy, latency, diagnostics, has_introduced),
        "diagnostics": diagnostics,
    }


def _warnings(
    reuse: float,
    entropy: float,
    latency: Optional[float],
    diagnostics: Dict[str, List[str]],
    has_introduced: bool,
) -> List[str]:
    out: List[str] = []
    if reuse > 0.6:
        out.append("concept_reuse_rate > 0.6: severe fixation, force new frames.")
    elif reuse > 0.4:
        out.append("concept_reuse_rate > 0.4: fixation starting, suggest new frames.")
    if entropy < 0.5:
        out.append("frame_entropy < 0.5: frames are too concentrated.")
    if latency is not None and latency >= 3:
        out.append("belief_revision_latency >= 3: belief stickiness, run reset protocol.")
    if latency is None and has_introduced:
        out.append("no revisions recorded despite introduced facts.")
    if diagnostics["orphan_revisions"]:
        out.append(
            "orphan revisions (revised but never introduced): "
            + ", ".join(diagnostics["orphan_revisions"])
        )
    return out


BAD_DEMO = [
    {"turn": 1, "concepts": ["利差"], "facts_introduced": ["F-012"], "facts_revised": []},
    {"turn": 2, "concepts": ["利差", "水池"], "facts_introduced": [], "facts_revised": []},
    {"turn": 3, "concepts": ["利差", "水池", "拔河"], "facts_introduced": [], "facts_revised": []},
    {"turn": 4, "concepts": ["利差", "拔河"], "facts_introduced": [], "facts_revised": []},
    {"turn": 5, "concepts": ["利差", "水位差"], "facts_introduced": ["F-017"], "facts_revised": []},
]

GOOD_DEMO = [
    {"turn": 1, "concepts": ["利差"], "facts_introduced": ["F-012"], "facts_revised": []},
    {"turn": 2, "concepts": ["利差", "水池"], "facts_introduced": ["F-017"], "facts_revised": ["F-012"]},
    {"turn": 3, "concepts": ["水池", "拔河", "水位差"], "facts_introduced": [], "facts_revised": []},
]


def _print_text(result: Dict[str, Any]) -> None:
    print(f"CVC metrics (v{__version__})")
    print("-----------")
    for key in (
        "turns",
        "concept_reuse_rate",
        "frame_entropy",
        "belief_revision_latency",
        "cvc_score",
    ):
        print(f"{key}: {result[key]}")
    print(f"unrevised_facts: {result['diagnostics']['unrevised_facts']}")
    if result["warnings"]:
        print("\nWarnings:")
        for warning in result["warnings"]:
            print(f"- {warning}")


def _print_markdown(result: Dict[str, Any]) -> None:
    print("| metric | value |")
    print("|---|---|")
    for key in (
        "turns",
        "concept_reuse_rate",
        "frame_entropy",
        "belief_revision_latency",
        "cvc_score",
    ):
        print(f"| `{key}` | {result[key]} |")
    if result["warnings"]:
        print("\n**Warnings**")
        for warning in result["warnings"]:
            print(f"- {warning}")


def main() -> None:
    parser = argparse.ArgumentParser(description="CVC convergence metrics")
    parser.add_argument("--input", help="JSON file with a list of turns")
    parser.add_argument("--demo", action="store_true", help="run the bad-case demo")
    parser.add_argument("--demo-good", action="store_true", help="run the good-case demo")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    parser.add_argument("--markdown", action="store_true", help="print a Markdown table")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    try:
        if args.demo:
            turns = validate_turns(BAD_DEMO)
        elif args.demo_good:
            turns = validate_turns(GOOD_DEMO)
        elif args.input:
            turns = load_turns(args.input)
        else:
            parser.error("use --demo, --demo-good, or --input")
            return
    except (InputError, json.JSONDecodeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)

    result = summarize(turns)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.markdown:
        _print_markdown(result)
    else:
        _print_text(result)


if __name__ == "__main__":
    main()
