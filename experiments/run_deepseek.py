# -*- coding: utf-8 -*-
"""Run one CVC experiment script against the DeepSeek API.

Usage:
    set DEEPSEEK_API_KEY=...          (PowerShell: $env:DEEPSEEK_API_KEY='...')
    python experiments/run_deepseek.py --script experiments/scripts/01-rmb.json --condition A
    python experiments/run_deepseek.py --script experiments/scripts/01-rmb.json --condition C

The API key is read from the environment and never written to disk.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-v4-pro"
TEMPERATURE = 0.0
MAX_TOKENS = 4000
REASONING_EFFORT = "low"

ROOT = Path(__file__).resolve().parents[1]

NEUTRAL_SYSTEM = (
    "当前日期：2026-11-18。你是一名乐于助人的助手。"
    "回答要清晰、直接，必要时给出推理过程。"
)

CVC_SYSTEM = """【CVC 对话规则 v0.1】

当前日期：2026-11-18。

1. 事实与时间
- 每条结论标注“截至 2026-11-18”。
- 不确定的事实标“未核实”，不要编造。
- 不要假设当前日期是其他时间。

2. 修订
- 出现新事实时，先回答一句：“这条信息是否推翻此前的结论？是 / 否 / 部分。”
- 如果是或部分，必须在同一轮修订：说明旧结论作废、新结论是什么、你错在哪一步。

3. 假设
- 给出结论前，先列出它依赖的关键假设，并标注“已确认 / 待验证 / 已推翻”。

4. 概念
- 不要为了连贯而重复前面的类比或框架。
- 需要举例时，优先换一个领域。

5. 纠错
- 如果用户的问题基于错误前提，先指出，再回答。
"""


def call(messages: list[dict], api_key: str) -> dict:
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "reasoning_effort": REASONING_EFFORT,
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(2 + attempt * 3)
                continue
            raise SystemExit(f"HTTP {exc.code}: {body}")
        except Exception as exc:
            if attempt < 3:
                time.sleep(2 + attempt * 3)
                continue
            raise SystemExit(f"request failed: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", required=True)
    parser.add_argument("--condition", choices=["A", "C"], required=True)
    args = parser.parse_args()

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise SystemExit("DEEPSEEK_API_KEY is not set")

    script = json.loads(Path(args.script).read_text(encoding="utf-8"))
    system = NEUTRAL_SYSTEM if args.condition == "A" else CVC_SYSTEM
    messages = [{"role": "system", "content": system}]

    out_dir = ROOT / "data" / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{script['id']}-{args.condition}"

    turns = []
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    started = datetime.now(timezone.utc).isoformat()

    for turn in script["turns"]:
        messages.append({"role": "user", "content": turn["prompt"]})
        response = call(messages, api_key)
        content = response["choices"][0]["message"].get("content") or ""
        if not content.strip():
            raise SystemExit(
                f"empty content at turn {turn['turn']}; increase max_tokens or reasoning_effort"
            )
        messages.append({"role": "assistant", "content": content})

        usage = response.get("usage", {})
        for key in usage_total:
            usage_total[key] += int(usage.get(key, 0))

        turns.append(
            {"turn": turn["turn"], "user": turn["prompt"], "assistant": content}
        )
        print(f"[{stem}] turn {turn['turn']} ok ({len(content)} chars)")

    with open(out_dir / f"{stem}.jsonl", "w", encoding="utf-8") as fh:
        for item in turns:
            fh.write(json.dumps(item, ensure_ascii=False) + "\n")

    meta = {
        "script_id": script["id"],
        "condition": args.condition,
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "reasoning_effort": REASONING_EFFORT,
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "usage": usage_total,
        "turns": len(turns),
    }
    (out_dir / f"{stem}.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {stem}: {len(turns)} turns, usage={usage_total}")


if __name__ == "__main__":
    main()
