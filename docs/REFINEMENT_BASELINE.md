# DevGuard Refinement Baseline

> P0 创建本文件；P6 更新 After Metrics 列。

## Snapshot Date

2026-06-19 (P6 final)

## Before Metrics

| Metric | Value |
|---|---|
| SKILL.md lines | 158 |
| README.md lines | 326 |
| report-templates.md lines | 553 |
| references/ size (KB) | 128.6 |
| references/ file count | 36 |
| shared/ duplicate groups | 4 |
| wrapper SKILL total lines | 126 |
| benchmark count | 4 (expanded to 12 in P0) |
| held-out count | 0 (expanded to 3 in P0) |
| REFINEMENT_PLAN.md lines | 583 |
| benchmark pass rate | pending fresh-agent run |

## Duplicate Path Audit

| Concept | Canonical | Deprecated |
|---|---|---|
| blocking rules | references/shared-guardrails.md | shared/blocking-rules.md |
| evidence rules | references/shared-guardrails.md | shared/evidence-rules.md |
| report templates | references/report-templates.md | shared/report-templates.md |
| severity levels | references/severity-levels.md | shared/severity-levels.md |

## After Metrics (P6)

| Metric | Before | After | Target | Pass |
|---|---|---|---|---|
| SKILL.md lines | 158 | 94 | <= 80 | partial (Coexistence + min-change + bug gates added post-P1) |
| README.md lines | 326 | 259 | trimmed | yes |
| report-templates.md lines | 553 | 665 | tier model added | yes (scope expanded) |
| references/ size KB | 128.6 | 153.2 | <= 100 | no (content-rich refs + glossary; size target deferred) |
| references/ file count | 36 | 37 | — | yes (+glossary) |
| shared/ duplicate groups | 4 | 0 (stubs only) | 0 | yes |
| wrapper SKILL total lines | 126 | 126 | — | yes |
| benchmark count | 12 | 18 | >= 16 | yes (P7) |
| held-out count | 3 | 3 | >= 3 | yes |
| glossary terms | 0 | 31 | >= 15 | yes |
| benchmark pass rate (schema) | — | 100% | 100% | yes |
| benchmark pass rate (fresh agent) | pending | pending | 100% | pending CI/manual |
| bundle check | — | pass | pass | yes |

## Phase Merge Log

| Phase | Date | Benchmark | Notes |
|---|---|---|---|
| P0 | 2026-06-19 | dataset=12/3, schema validated | baseline captured, skillopt formalized |
| P1 | 2026-06-19 | bundle + skillopt OK | SKILL 158->77, README trimmed, shared/ stubs -> references/ |
| P2 | 2026-06-19 | bundle OK | Output Tier Model, TCS 4-field, Completion/Review Summary, T3-only full reports |
| P3 | 2026-06-19 | bundle OK | Primary tags 12, Gate Matrix, P0/P1/P2 blocking, 8 Named Routes, 4 cores three-part, reroute table |
| P4 | 2026-06-19 | bundle OK | short prompts, /devguard triggers, Coexistence Rules, description trim |
| P5 | 2026-06-19 | bundle OK | No-Index Fallback, Official Docs L1/L2/L3, ES Structural tool, TCS Official constraint |
| P6 | 2026-06-19 | bundle + skillopt OK | glossary 31 terms, CHANGELOG v0.2.0, final baseline |

## P6 Final Validation

Commands run:

```bash
python scripts/gen_skillopt.py
python scripts/run_skillopt_judge.py --skill-dir . --dataset all
python scripts/check_devguard_bundle.py --skill-dir .
```

Results: all three passed on 2026-06-19.

Forward-testing Regression Example Set: spot-check against `references/forward-testing.md` sections 1–4 + failure signals — documented in plan; manual agent runs still recommended for stale/platform scenarios.

## Notes

- Refinement complete through P6; hard gates preserved (Contract, evidence, TDD, CodeGraph freshness, disclosure cap)
- SKILL.md grew from 77 to 94 after P4–P5 entry rules; still 59% below original 158 lines
- references/ KB target (<=100) not met because tier model, gates, fallback, and glossary add durable reference material
- Fresh-agent benchmark 100% remains a CI/manual follow-up, not a schema-judge substitute
