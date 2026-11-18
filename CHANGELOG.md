# Changelog

All notable changes to this project will be documented in this file.

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
