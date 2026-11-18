# Changelog

All notable changes to this project will be documented in this file.

## [0.2.4] - 2026-11-18

### Added

- Three-topic real run: RMB, gold, Nvidia (10 turns × 2 conditions each)
- `data/revision-log.json`: manual judgment of explicit revision per conversation
- `experiments/auto_annotate.py`: assisted keyword annotation (provisional)
- `experiments/digest.py`: compact transcript digest for annotation

### Changed

- Both system prompts now pin the date and treat user-provided facts as true,
  even when they conflict with the model's training data
- `docs/results.md` rewritten with cross-topic revision results

### Findings

- **Conflict strength beats prompting**: RMB C revised / A did not; gold **both**
  declined to revise; Nvidia **both** revised.
- CVC cannot manufacture revision; it only makes willing revision explicit.
- Over-revision remains (RMB C applied the rule to a policy explanation).
- Keyword annotation inflates concept reuse to ~0.82; only RMB has manual
  frame-level annotation.

## [0.2.3] - 2026-11-18

### Added

- **First real A/C run** on `deepseek-v4-pro` (RMB topic, 10 turns each)
- Raw transcripts and metadata (`data/raw/`)
- Annotations (`data/annotations/`)
- Results write-up (`docs/results.md`)
- API runner (`experiments/run_deepseek.py`)

### Findings

- Explicit revision: C latency `0.0`, A `None`
- Concept reuse: **no improvement** (A 0.633, C 0.636)
- Entropy: slight increase (0.886 → 0.905)
- Over-revision: C applied the revision rule to a policy explanation
- Token cost: essentially equal (49.2k vs 49.5k)

### Notes

- n=1, one topic, one model, one non-blind annotator. Preliminary only.

## [0.2.2] - 2026-11-18

### Added

- Pilot run (`pilots/01-rmb/`), clearly marked as **simulated, not evidence**
- Pilot review (`docs/pilot-results.md`)

### Fixed

- **Revision clock**: latency now starts when the latest contradicting fact
  arrives, not when the old belief was first stated.
- **No-revision penalty**: if facts were introduced but none was revised,
  the latency component now scores `0` instead of a neutral `0.5`.

### Changed

- `BAD_DEMO` no longer revises, so it is a true negative case
- `GOOD_DEMO` latency is now `0.0` (same-turn revision)
- `docs/metrics.md` and `SPEC.md` describe the new clock
- Metric tests updated; 36 tests total

## [0.2.1] - 2026-11-18

### Added

- Three 10-turn experiment scripts (`experiments/scripts/`)
  - RMB: rate differential vs trade surplus
  - Gold: geopolitics vs real rates
  - Nvidia: export controls and governance vs demand
- Experiment run sheet (`experiments/run_sheet.md`)
- Transcript template (`experiments/transcript_template.jsonl`)
- Script validation tests (10 turns, turn-5 conflict fact, no leakage words)

### Changed

- README roadmap now splits scripts (v0.2.1) from data/results (v0.2.2)

## [0.2.0] - 2026-11-18

### Added

- Annotation helper (`eval/annotate.py`)
  - `--template`: build a blank annotation file from raw JSONL
  - `--check`: validate and compute metrics
  - `--summary`: flag turns with no concepts
- Annotation guide (`docs/annotation-guide.md`)
- Experiment protocol (`docs/experiment.md`)
- Raw conversation template (`eval/annotation_template.jsonl`)
- Tests for the annotation helper

### Changed

- `CITATION.cff` and README now use the **concept DOI** (`10.5281/zenodo.24338017`)
- FAQ explains concept DOI vs version DOI
- CI runs an annotation smoke test

## [0.1.1] - 2026-11-18

### Added

- Unit tests (`tests/`) — 25 tests for metrics, validation, and links
- English README (`README.en.md`)
- FAQ (`docs/faq.md`)
- Positive case study (`examples/good-revision.md`)
- English reset protocol (`prompts/en/00-reset-protocol.md`)
- Issue templates (bug, prior-art) and PR template
- Evaluation sample data (`eval/sample_data.json`)
- Eval usage guide (`eval/README.md`)
- `.editorconfig`

### Changed

- `eval/convergence_metrics.py`
  - Input validation with precise error messages and exit code `2`
  - Duplicate revisions now counted once
  - Orphan revisions and unrevised facts surfaced as diagnostics
  - `--version`, `--demo-good`, `--markdown` flags
- `SPEC.md`
  - Versioning policy (§9)
  - Evaluation protocol (§10)
  - Limitations and failure modes (§11)
- CI now runs tests and validates sample data

### Fixed

- Unclear failure mode when `facts_revised` referenced an unknown fact

## [0.1.0] - 2026-11-18

### Added

- Initial specification (`SPEC.md`)
- Three ledger templates: fact, concept, assumption
- Reset protocol prompt
- Five fork lenses
- Metrics definitions (`docs/metrics.md`)
- Reference implementation (`eval/convergence_metrics.py`)
- Case study on the RMB belief-revision failure
- Prior art review

### Notes

- This is a draft. API and prompt formats may change before `v1.0.0`.
