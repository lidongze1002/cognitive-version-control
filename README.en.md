# Cognitive Version Control (CVC)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24338017.svg)](https://doi.org/10.5281/zenodo.24338017)
[![CI](https://github.com/lidongze1002/cognitive-version-control/actions/workflows/ci.yml/badge.svg)](https://github.com/lidongze1002/cognitive-version-control/actions/workflows/ci.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> The real problem with long conversations is not that the model forgets.
> It is that the model **will not change its mind**.

CVC is a lightweight specification for long LLM conversations:
**facts get IDs, concepts get a ledger, assumptions can be revoked, and conclusions expire.**

- Status: `v0.2.3-draft`
- Docs license: **CC BY 4.0**
- Code license: **MIT**
- DOI: **10.5281/zenodo.24338017** (concept DOI; each version also has a version DOI)

---

## 1. What it fixes

| Failure mode | Symptom | CVC mechanism |
|---|---|---|
| **Stale facts** | New data arrives, conclusion stays | Fact ledger + conflict check |
| **Concept fixation** | One metaphor from turn 1 to turn 50 | Concept ledger + reuse rate |
| **Hidden assumptions** | Premises are never stated | Assumption ledger |
| **Single-track drift** | Conversation only goes deeper, never sideways | Forking |
| **No measurement** | You cannot tell whether it improved | Three metrics |

A real case: [`examples/fx-case-study.md`](examples/fx-case-study.md) — the model kept saying "RMB depreciation pressure" after USD/CNY had already fallen to 6.66.

---

## 2. The three ledgers

### Fact ledger

```json
{
  "id": "F-017",
  "claim": "USD/CNY ~ 6.66",
  "as_of": "2026-11-18",
  "source": "TradingEconomics",
  "confidence": 0.9,
  "status": "active"
}
```

When a new fact contradicts an old one, the old record becomes `superseded`; it is never deleted.

### Concept ledger

Tracks metaphors, models, and keywords already used in the conversation. When reuse crosses a threshold, the next answer is forced to bring in new frames.

### Assumption ledger

Every conclusion must list the premises it depends on, each marked `pending`, `confirmed`, or `refuted`, with an `if_false` consequence.

---

## 3. Two moves

- **Fork**: branch from any turn with a lens (`skeptic`, `historian`, `contrarian`, `layman`, `quant`).
- **Reset**: re-anchor on a new topic or new facts instead of sliding further down the old context.

---

## 4. Three metrics

| Metric | Meaning | Healthy |
|---|---|---|
| `concept_reuse_rate` | repeated concepts / all concepts | < 0.4 |
| `frame_entropy` | normalized Shannon entropy | > 0.7 |
| `belief_revision_latency` | turns from new fact to revision | <= 1 |

```bash
python eval/convergence_metrics.py --demo
```

---

## 5. Quick start

Paste [`prompts/00-reset-protocol.md`](prompts/00-reset-protocol.md) at the start of a new conversation.

More templates:

- [`prompts/01-fact-ledger.md`](prompts/01-fact-ledger.md)
- [`prompts/02-concept-ledger.md`](prompts/02-concept-ledger.md)
- [`prompts/03-assumption-ledger.md`](prompts/03-assumption-ledger.md)
- [`prompts/04-fork-lenses.md`](prompts/04-fork-lenses.md)

FAQ (originality, RAG, commercial use): [`docs/faq.md`](docs/faq.md).

### Run an experiment

- Annotation guide: [`docs/annotation-guide.md`](docs/annotation-guide.md)
- Experiment protocol: [`docs/experiment.md`](docs/experiment.md)
- Annotation tool: `python eval/annotate.py --template raw.jsonl --out annotation.json`
- **Ready-made scripts**: [`experiments/scripts/`](experiments/scripts/) (RMB, gold, Nvidia; 10 turns each)
- Run sheet: [`experiments/run_sheet.md`](experiments/run_sheet.md)
- Pilot review (simulated, not evidence): [`docs/pilot-results.md`](docs/pilot-results.md)
- **First real A/C result**: [`docs/results.md`](docs/results.md)

---

## 6. Non-goals

- Not a new model; no training or fine-tuning
- Not "always be novel"; for companion products, convergence is a feature
- Not a fact-checker; ledgers make claims traceable, not true
- Not an academic first; see [`docs/prior-art.md`](docs/prior-art.md)

---

## 7. Prior art and contribution

The components are not new: belief revision, assumption-based planning, MemGPT-style memory, Revisitable Memory, Verbalized Sampling, prompt versioning tools.

**The contribution is integration and operationalization:**

1. Treating concept reuse rate and belief revision latency as first-class metrics
2. Packaging fact / concept / assumption ledgers plus forking into one workflow
3. Shipping copy-paste prompts and a runnable evaluation script

---

## 8. Roadmap

- [x] v0.1.0: spec, prompts, metrics script
- [x] v0.1.1: tests, English docs, FAQ, issue templates
- [x] v0.2.0: annotation tool, annotation guide, experiment protocol
- [x] v0.2.1: three experiment scripts + run sheet
- [x] v0.2.2: pilot run + metric fixes (revision clock, no-revision penalty)
- [x] v0.2.3: first real A/C run (DeepSeek, RMB)
- [ ] v0.2.4: gold and Nvidia replication + second annotator
- [ ] v0.3.0: multi-model adapters (Claude / GPT / Gemini / open models)
- [ ] v0.4.0: reference CLI for conversation forking

---

## 9. Citation

```text
Li, Dongze. (2026). Cognitive Version Control: Fact, Concept, and Assumption
Ledgers for Long LLM Conversations (v0.2.3). Zenodo.
https://doi.org/10.5281/zenodo.24338017
```

See [`CITATION.cff`](CITATION.cff).

---

## 10. License

- Documentation and prompts: **CC BY 4.0** ([`LICENSE`](LICENSE))
- Code: **MIT** ([`LICENSE-CODE`](LICENSE-CODE))

## 11. Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Most wanted:

1. **Counterexamples**: cases where CVC made the conversation worse
2. **Prior art**: papers or tools we missed
3. **Data**: annotated long conversations for calibrating thresholds
