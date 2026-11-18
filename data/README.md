# Data

Real API runs of the experiment scripts (2026-11-18).

## Runs

| Topic | Condition | File | Tokens |
|---|---|---|---|
| 01 RMB | A | `raw/01-rmb-A.jsonl` | 55,203 |
| 01 RMB | C | `raw/01-rmb-C.jsonl` | 59,954 |
| 02 Gold | A | `raw/02-gold-A.jsonl` | 44,035 |
| 02 Gold | C | `raw/02-gold-C.jsonl` | 44,696 |
| 03 Nvidia | A | `raw/03-nvidia-A.jsonl` | 53,491 |
| 03 Nvidia | C | `raw/03-nvidia-C.jsonl` | 52,661 |

Model: `deepseek-v4-pro`, temperature 0, reasoning effort low, max tokens 4000.
Each transcript is 10 turns; each `.meta.json` records usage and settings.

## Prompts

Both conditions pin the current date (2026-11-18) and state that user-provided
facts are to be treated as true even if they conflict with the model's training
data. C adds the CVC reset rules.

## Annotations

- `annotations/01-rmb-A.json`, `annotations/01-rmb-C.json`
  **Manual, frame-level annotation.** 2–5 concepts per turn.
- `annotations/auto/*.json`
  **Assisted keyword annotation**, produced by `experiments/auto_annotate.py`.
  It over-counts domain terms (reuse ≈ 0.82 for every conversation) and is kept
  only for reproducibility, **not** as a result.
- `revision-log.json`
  Manual judgment of whether each conversation explicitly revised its prior
  conclusion, with evidence.

## Reproduce

```bash
set DEEPSEEK_API_KEY=...
python experiments/run_deepseek.py --script experiments/scripts/01-rmb.json --condition A
python experiments/run_deepseek.py --script experiments/scripts/01-rmb.json --condition C
python eval/convergence_metrics.py --input data/annotations/01-rmb-A.json --json
```

The API key is read from the environment and never written to disk.
