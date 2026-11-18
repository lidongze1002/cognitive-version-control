# v1.0.0 — Final: project closed

This is the final release. The project is archived and no longer maintained.

## Why stop

The core question is answered:

> **CVC is a conflict-dependent scaffold, not a general revision fix.**

It can make a willing model revise more explicitly. It cannot make an unwilling
model change its mind. The deciding variable is whether the model made a
falsifiable commitment in the first place.

Continuing would require a different kind of work: multiple models, blind
annotators, pre-registration, larger samples. That is a paper-scale effort, not
a personal project.

## What is in this release

- `docs/final-report.md`: complete retrospective
- Frozen specification (`SPEC.md`)
- 36 passing tests
- 6 real DeepSeek conversations (60 turns)
- Annotation kit, experiment scripts, revision log

## Key results

| Topic | A baseline | C CVC |
|---|---|---|
| RMB | no revision | **revision** |
| Gold | no revision | no revision |
| Nvidia | **revision** | **revision** |

RMB quantitative (manual annotation):

| Metric | A | C |
|---|---|---|
| `concept_reuse_rate` | 0.633 | 0.636 |
| `belief_revision_latency` | None | 0.0 |
| `cvc_score` | 0.412 | 0.717 |

## What was not established

- Effectiveness on other models
- Long-term effectiveness
- Whether the metric thresholds are sound
- Inter-annotator agreement (no second annotator)

## Continuation

See section 7 of `docs/final-report.md`.

## License

- Documentation and prompts: CC BY 4.0
- Code: MIT
