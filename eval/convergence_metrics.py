#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convergence metrics for long LLM conversations.

Three metrics:
  1. concept_reuse_rate       -- how often concepts repeat
  2. frame_entropy            -- normalized Shannon entropy of concept usage
  3. belief_revision_latency  -- turns between a new fact and its revision

No third-party dependencies.

Usage:
    python eval/convergence_metrics.py --demo
    python eval/convergence_metrics.py --input data.json
    python eval/convergence_metrics.py --input data.json --json

Input format (list of turns):
[
  {"turn": 1, "concepts": ["利差"], "facts_introduced": [], "facts_revised": []},
  {"turn": 2, "concepts": ["利差", "水池"], "facts_introduced": ["F-017"], "facts_revised": ["F-012"]}
]
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from typing import Any, Dict, Iterable, List, Optional


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
    """Average turns between a fact's introduction and its revision.

    A revision on the same turn counts as 0. Returns None if no revision.
    """
    introduced: Dict[str, int] = {}
    latencies: List[float] = []
    for turn in turns:
        turn_no = int(turn.get("turn", 0))
        for fact_id in turn.get("facts_introduced", []):
            introduced.setdefault(fact_id, turn_no)
        for fact_id in turn.get("facts_revised", []):
            if fact_id in introduced:
                latencies.append(turn_no - introduced[fact_id])
    if not latencies:
        return None
    return sum(latencies) / len(latencies)


def summarize(turns: List[Dict[str, Any]]) -> Dict[str, Any]:
    reuse = concept_reuse_rate(turns)
    entropy = frame_entropy(turns)
    latency = belief_revision_latency(turns)

    if latency is None:
        score_latency = 0.5
    else:
        score_latency = max(0.0, 1.0 - latency / 3.0)

    score = 0.4 * (1 - reuse) + 0.3 * entropy + 0.3 * score_latency

    return {
        "turns": len(turns),
        "concept_reuse_rate": round(reuse, 4),
        "frame_entropy": round(entropy, 4),
        "belief_revision_latency": None if latency is None else round(latency, 2),
        "cvc_score": round(score, 4),
        "warnings": _warnings(reuse, entropy, latency),
    }


def _warnings(reuse: float, entropy: float, latency: Optional[float]) -> List[str]:
    out: List[str] = []
    if reuse > 0.6:
        out.append("概念复用率 > 0.6：严重固化，建议强制更换框架。")
    elif reuse > 0.4:
        out.append("概念复用率 > 0.4：开始固着，建议提示换框架。")
    if entropy < 0.5:
        out.append("框架熵 < 0.5：框架过于集中。")
    if latency is not None and latency >= 3:
        out.append("信念修订延迟 >= 3 轮：存在信念粘性，建议执行重置协议。")
    return out


DEMO = [
    {"turn": 1, "concepts": ["利差"], "facts_introduced": ["F-012"], "facts_revised": []},
    {"turn": 2, "concepts": ["利差", "水池"], "facts_introduced": [], "facts_revised": []},
    {"turn": 3, "concepts": ["利差", "水池", "拔河"], "facts_introduced": [], "facts_revised": []},
    {"turn": 4, "concepts": ["利差", "拔河"], "facts_introduced": [], "facts_revised": []},
    {"turn": 5, "concepts": ["利差", "水位差"], "facts_introduced": ["F-017"], "facts_revised": ["F-012"]},
]


def main() -> None:
    parser = argparse.ArgumentParser(description="CVC convergence metrics")
    parser.add_argument("--input", help="JSON file with a list of turns")
    parser.add_argument("--demo", action="store_true", help="run built-in demo data")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    if args.demo:
        turns = DEMO
    elif args.input:
        with open(args.input, encoding="utf-8") as fh:
            turns = json.load(fh)
    else:
        parser.error("use --demo or --input")

    result = summarize(turns)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("CVC metrics")
    print("-----------")
    for key, value in result.items():
        if key == "warnings":
            continue
        print(f"{key}: {value}")
    if result["warnings"]:
        print("\nWarnings:")
        for warning in result["warnings"]:
            print(f"- {warning}")


if __name__ == "__main__":
    main()
