# Eval

Reference implementation of the three CVC metrics.

## Requirements

- Python 3.9+
- No third-party dependencies

## Usage

```bash
# bad case (fixation + slow revision)
python eval/convergence_metrics.py --demo

# good case (fast revision)
python eval/convergence_metrics.py --demo-good

# your own data
python eval/convergence_metrics.py --input eval/sample_data.json

# machine-readable
python eval/convergence_metrics.py --input eval/sample_data.json --json

# Markdown table
python eval/convergence_metrics.py --input eval/sample_data.json --markdown
```

## Input schema

A JSON array of turns:

```json
[
  {
    "turn": 1,
    "concepts": ["利差"],
    "facts_introduced": ["F-012"],
    "facts_revised": []
  },
  {
    "turn": 2,
    "concepts": ["利差", "水池"],
    "facts_introduced": ["F-017"],
    "facts_revised": ["F-012"]
  }
]
```

Rules:

- `turn` must be a unique non-negative integer
- `concepts`, `facts_introduced`, `facts_revised` are lists of strings
- a fact may be revised on the same turn it was introduced (latency = 0)

Invalid input exits with code `2` and a precise message.

## Output

```json
{
  "turns": 5,
  "concept_reuse_rate": 0.6,
  "frame_entropy": 0.8805,
  "belief_revision_latency": 4.0,
  "cvc_score": 0.4241,
  "warnings": ["..."],
  "diagnostics": {
    "unrevised_facts": ["F-017"],
    "orphan_revisions": []
  }
}
```

## Tests

```bash
python -m unittest discover -s tests -v
```
