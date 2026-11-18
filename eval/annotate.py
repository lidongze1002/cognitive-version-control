#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Annotation helper for CVC experiments.

Three modes:

  # 1. Build a blank annotation file from raw turns
  python eval/annotate.py --template raw.jsonl --out annotation.json

  # 2. Validate an annotation file and print metrics
  python eval/annotate.py --check annotation.json

  # 3. Per-turn summary (find turns with no concepts)
  python eval/annotate.py --summary annotation.json

Raw JSONL format (one object per line):

  {"turn": 1, "user": "...", "assistant": "..."}

Annotation format is the same as eval/sample_data.json, plus an optional
"note" field per turn.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.convergence_metrics import (  # noqa: E402
    InputError,
    load_turns,
    summarize,
    validate_turns,
)

__version__ = "0.2.1"


def load_raw(path: str | Path) -> List[Dict[str, Any]]:
    """Read and validate a JSONL file of raw conversation turns."""
    turns: List[Dict[str, Any]] = []
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise InputError(f"line {lineno}: invalid JSON ({exc})") from exc
            if not isinstance(item, dict):
                raise InputError(f"line {lineno}: must be an object")
            turn = item.get("turn")
            if isinstance(turn, bool) or not isinstance(turn, int) or turn < 0:
                raise InputError(f"line {lineno}: turn must be a non-negative integer")
            for field in ("user", "assistant"):
                if field in item and not isinstance(item[field], str):
                    raise InputError(f"line {lineno}: {field} must be a string")
            turns.append(
                {
                    "turn": turn,
                    "user": item.get("user", ""),
                    "assistant": item.get("assistant", ""),
                }
            )

    if not turns:
        raise InputError("no turns found in raw file")
    if len({t["turn"] for t in turns}) != len(turns):
        raise InputError("duplicate turn numbers in raw file")
    return sorted(turns, key=lambda t: t["turn"])


def build_template(raw_turns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Create a blank annotation record for every raw turn."""
    return [
        {
            "turn": t["turn"],
            "concepts": [],
            "facts_introduced": [],
            "facts_revised": [],
            "note": "",
        }
        for t in raw_turns
    ]


def write_json(path: str | Path, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def summarize_annotation(path: str | Path) -> Dict[str, Any]:
    turns = load_turns(path)
    result = summarize(turns)
    result["empty_concept_turns"] = [
        t["turn"] for t in turns if not t["concepts"]
    ]
    return result


def print_summary(path: str | Path) -> None:
    result = summarize_annotation(path)
    print(f"turns: {result['turns']}")
    print(f"concept_reuse_rate: {result['concept_reuse_rate']}")
    print(f"frame_entropy: {result['frame_entropy']}")
    print(f"belief_revision_latency: {result['belief_revision_latency']}")
    print(f"empty_concept_turns: {result['empty_concept_turns']}")
    for warning in result["warnings"]:
        print(f"- {warning}")


def main() -> None:
    parser = argparse.ArgumentParser(description="CVC annotation helper")
    parser.add_argument("--template", metavar="RAW.jsonl", help="build a blank annotation file")
    parser.add_argument("--out", metavar="ANNOTATION.json", help="output path for --template")
    parser.add_argument("--check", metavar="ANNOTATION.json", help="validate and print metrics")
    parser.add_argument("--summary", metavar="ANNOTATION.json", help="per-turn summary")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    try:
        if args.template:
            if not args.out:
                parser.error("--template requires --out")
            raw = load_raw(args.template)
            write_json(args.out, build_template(raw))
            print(f"wrote {len(raw)} turns to {args.out}")
        elif args.check:
            result = summarize_annotation(args.check)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.summary:
            print_summary(args.summary)
        else:
            parser.error("use --template/--out, --check, or --summary")
    except (InputError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
