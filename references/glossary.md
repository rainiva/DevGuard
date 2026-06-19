# DevGuard Glossary

Compact definitions for outward disclosure, routing, and gate vocabulary. Canonical rules live in the linked references.

| Term | Meaning | Canonical reference |
|---|---|---|
| Task Profile | Exploratory pre-contract snapshot: problem, outcome, non-goals, touched surfaces, task family | [task-routing.md](task-routing.md) |
| Socratic Inquiry | Structured one-question-per-turn clarification when Task Profile ambiguity blocks safe routing or contract freeze | [socratic-inquiry-core.md](socratic-inquiry-core.md) |
| Inquiry Note | T2 outward block surfacing the current Socratic question while `Status: INQUIRY` | [report-templates.md](report-templates.md) |
| Task Contract | Frozen execution slice: allowed scope, tests, acceptance, constraints — tighter than impact analysis | [report-templates.md](report-templates.md) |
| Task Contract Summary (TCS) | T1 outward contract block: Goal, Scope, Tests, Acceptance, optional one-line Official constraint | [report-templates.md](report-templates.md) |
| Impact Analysis | Change-impact judgment after project understanding and official docs check; not a substitute for Contract | [impact-analysis-core.md](impact-analysis-core.md) |
| Execution Summary (ES) | Default T1 outward routing packet: Task, Mode, Rules, Status, optional Structural tool, Next | [report-templates.md](report-templates.md) |
| Risk Note | T2 focused block for high-risk but non-anomalous slices | [report-templates.md](report-templates.md) |
| Exception Note | T2 focused block for blockers, missing rules, or anomalies | [report-templates.md](report-templates.md) |
| Completion Summary | T1b outward block when work finishes; bugfix variant adds Repro / Red-before / Root cause / Green-after / Diff scope | [report-templates.md](report-templates.md) |
| Review Summary | T1b outward review block with Verdict, Severity, Findings | [report-templates.md](report-templates.md) |
| FAST | Low-rigour execution mode; smallest gates and rule load per Gate Matrix | [task-routing.md](task-routing.md) |
| STANDARD | Normal engineering mode; full pre-execution gates for typical code work | [task-routing.md](task-routing.md) |
| STRICT | High-rigour mode; deep gates, focused expansion, L3 official docs when release applies | [task-routing.md](task-routing.md) |
| metadata / summary / full | Rule disclosure load levels: index hint, compact operating rule, full reference file | [rule-disclosure-index.md](rule-disclosure-index.md) |
| ALLOW | Execution may proceed; gates satisfied | [shared-guardrails.md](shared-guardrails.md) |
| ALLOW_WITH_WARNINGS | Proceed with disclosed gaps; emit Risk Note when outward | [shared-guardrails.md](shared-guardrails.md) |
| BLOCKED | Hard stop; emit Exception Note; resolve P0/P1 first | [shared-guardrails.md](shared-guardrails.md) |
| Named Route | Preset route ID (for example route:bugfix-standard) mapping to a skill chain and expected rule count | [task-routing.md](task-routing.md) |
| Gate Matrix | Complexity x execution-mode table for project understanding, official docs, IA, Contract, TDD Red | [task-routing.md](task-routing.md) |
| Primary Risk Tags | Twelve tags that drive mode and gate depth (for example api_contract, security) | [task-routing.md](task-routing.md) |
| Secondary Risk Tags | Factual tags that load extensions but do not alone pick FAST/STANDARD/STRICT | [task-routing.md](task-routing.md) |
| Output Tier Model | T1 pre-exec, T1b completion/review, T2 focused expansion, T3 detailed audit templates | [report-templates.md](report-templates.md) |
| Coexistence Rules | How DevGuard shares work with domain skills: DevGuard owns gates; domain owns technique | [SKILL.md](../SKILL.md) |
| Minimum Change Constraint | Unified edit floor: simplest correct diff inside frozen Contract scope; reroute to expand | [shared-guardrails.md](shared-guardrails.md) |
| Evidence Gate | Bug-fix six-item hard gate: repro input, Red, minimal scope, root cause, all green, diff scope | [bug-fix-core.md](bug-fix-core.md) |
| No-Index Fallback | When codegraph_unavailable: S1 limited read; S2+ init or ALLOW_WITHOUT_CODEGRAPH | [codegraph-project-understanding.md](codegraph-project-understanding.md) |
| Official Docs L1 | Context7 or equivalent scoped summary — enough for IA on ordinary platform touch | [official-docs-check.md](official-docs-check.md) |
| Official Docs L2 | Original official doc or API reference verification for high-risk surfaces | [official-docs-check.md](official-docs-check.md) |
| Official Docs L3 | L2 plus explicit human confirmation for STRICT release or go-live | [official-docs-check.md](official-docs-check.md) |
| Official constraint | Single one-line platform rule in TCS when docs govern the slice | [report-templates.md](report-templates.md) |
| Structural tool | Execution Summary field reporting CodeGraph or fallback state | [report-templates.md](report-templates.md) |
| LITE | Daily micro-edit mode: Slice in ES for execute; ES-only for preview; upgrades to FAST+ on bugfix/Primary tags | [task-routing.md](task-routing.md) |
| Short trigger | /devguard fast, /devguard strict, or /devguard review prepended to a task | [example-prompts.md](example-prompts.md) |
