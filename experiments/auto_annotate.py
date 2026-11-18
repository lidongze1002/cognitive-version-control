# -*- coding: utf-8 -*-
"""Assisted annotation: controlled vocabulary + explicit revision markers.

This is not a replacement for blind human annotation. It makes the first pass
reproducible; a second annotator should still verify it.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEXICONS = {
    "01-rmb": [
        "利差", "贸易顺差", "美元指数", "结汇", "中间价", "资本流动",
        "套息", "政策工具", "情景", "套期保值", "自然对冲", "拔河", "水池",
    ],
    "02-gold": [
        "实际利率", "美元指数", "地缘", "央行购金", "财政赤字", "通胀",
        "机会成本", "避险", "获利了结", "情景", "配置", "定投", "仓位",
    ],
    "03-nvidia": [
        "出口管制", "中国收入", "数据中心", "需求", "治理", "CEO",
        "国会", "供应链", "估值", "客户", "竞争", "财报", "指引",
        "招聘", "替代",
    ],
}

REVISION_MARKERS = ["推翻", "作废", "过期", "错在", "不再成立"]
SNIPPET = 220


def annotate(path: Path) -> dict:
    topic = path.name.split("-")[0] + "-" + path.name.split("-")[1]
    lexicon = LEXICONS[topic]
    turns = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    rows = []
    turn5_text = ""
    for item in turns:
        text = item["assistant"]
        concepts = [term for term in lexicon if term in text]
        facts = []
        revised = []
        if item["turn"] == 2:
            facts = ["F-001"]
        elif item["turn"] == 5:
            facts = ["F-002"]
            turn5_text = text
            if any(marker in text for marker in REVISION_MARKERS):
                revised = ["F-001"]
        elif item["turn"] == 7:
            facts = ["F-003"]
        rows.append(
            {
                "turn": item["turn"],
                "concepts": concepts,
                "facts_introduced": facts,
                "facts_revised": revised,
                "note": "",
            }
        )

    return {
        "annotation": rows,
        "turn5_has_revision_marker": any(
            marker in turn5_text for marker in REVISION_MARKERS
        ),
        "turn5_snippet": turn5_text.replace("\n", " ")[:SNIPPET],
    }


def main() -> None:
    out_dir = ROOT / "data" / "annotations" / "auto"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {}

    for path in sorted((ROOT / "data" / "raw").glob("*.jsonl")):
        result = annotate(path)
        stem = path.stem
        (out_dir / f"{stem}.json").write_text(
            json.dumps(result["annotation"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        summary[stem] = {
            "revision_marker": result["turn5_has_revision_marker"],
            "turn5": result["turn5_snippet"],
        }
        print(f"wrote {stem}.json")

    (ROOT / "data" / "annotation-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote data/annotation-summary.json")


if __name__ == "__main__":
    main()
