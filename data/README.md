# Data

Real API runs of the experiment scripts.

## Layout

```text
data/
├── raw/
│   ├── 01-rmb-A.jsonl        # baseline transcript
│   ├── 01-rmb-C.jsonl        # CVC transcript
│   ├── 01-rmb-A.meta.json    # model, temperature, usage
│   └── 01-rmb-C.meta.json
└── annotations/
    ├── 01-rmb-A.json
    └── 01-rmb-C.json
```

## Run 01 — RMB

| Field | Value |
|---|---|
| Model | `deepseek-v4-pro` |
| Temperature | 0 |
| Reasoning effort | low |
| Max tokens | 4000 |
| Date | 2026-11-18 |
| Turns | 10 per condition |
| A system prompt | neutral, with current date pinned |
| C system prompt | CVC reset rules, with current date pinned |
| Tokens (A) | 49,175 |
| Tokens (C) | 49,484 |

## Annotation

- One annotator (the author), **not blind** to condition.
- Concepts restricted to a controlled vocabulary per topic; a concept is recorded once per turn.
- `F-001` = the initial directional conclusion; `F-002` = the turn-5 contradicting data; `F-003` = the policy-tool interpretation.
- Revision is recorded only when the response **explicitly** marks the old conclusion as overturned (`推翻` / `作废` / `过期`).

This is a **preliminary** annotation. A second, blind annotator is required before treating the numbers as evidence.

## Reproduce

```bash
set DEEPSEEK_API_KEY=...
python experiments/run_deepseek.py --script experiments/scripts/01-rmb.json --condition A
python experiments/run_deepseek.py --script experiments/scripts/01-rmb.json --condition C
python eval/convergence_metrics.py --input data/annotations/01-rmb-A.json --json
python eval/convergence_metrics.py --input data/annotations/01-rmb-C.json --json
```

The API key is read from the environment and never written to disk.
