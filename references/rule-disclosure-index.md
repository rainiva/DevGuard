# Rule Disclosure Index

## Metadata

- Layer: shared
- Load level: metadata, summary, full
- Use when: selecting which DevGuard rule to load and at what depth.

## Summary

DevGuard supports three-stage disclosure without forcing every task to read every full rule file.

## Full Rule

Use this index as the metadata and summary layer. Read the target file only when the task stage requires full guidance.

## Load Levels

- `metadata`: use during routing to identify relevance.
- `summary`: use during impact analysis and load planning.
- `full`: use during execution, review, release, or blocked-state handling.

## Layer Taxonomy

- `meta`: routing, rule-loading, disclosure, and global decision policy.
- `pre-execution`: required gates before coding, repair, refactor, or release execution.
- `execution`: task-lane rules that guide implementation or repair.
- `extension`: stack, compatibility, performance, or scenario-specific additions.
- `project`: project-specific rule packs and project-rule selection policy.
- `playbook`: issue-specific troubleshooting or handling guides.
- `review`: review-side verification rules and mirrored review extensions.
- `shared`: reusable templates, severity scales, and common guardrails.

Use `Layer` for rule-loading taxonomy and `Wrapper path` for the internal skill module that invokes the reference. If `Wrapper path` is `n/a`, the rule is reference-only and should be loaded directly from `Path`.

## Rule Index

| Rule | Wrapper path | Path | Layer | Metadata trigger | Summary |
|---|---|---|---|---|---|
| task-router | skills/00-task-router/SKILL.md | references/task-routing.md | meta | any routed task | classify task type, risk, complexity, mode, and skill chain |
| rule-loading | n/a | references/rule-loading.md | meta | any execution task | decide minimal loaded set, deferred rules, disclosure mode, project-understanding gating, and Task Contract gating |
| codegraph-project-understanding | skills/12-codegraph-project-understanding/SKILL.md | references/codegraph-project-understanding.md | pre-execution | code change larger than tiny known local edit | locate entry points, call chains, similar implementations, and impact surfaces before impact analysis |
| official-docs-check | skills/13-official-docs-check/SKILL.md | references/official-docs-check.md | pre-execution | platform, framework, SDK, host, control-template, system-API, or design-guideline constraints may matter | confirm official constraints before impact analysis and Task Contract freeze |
| shared-guardrails | n/a | references/shared-guardrails.md | shared | any gated task | evidence, TDD floor, blocking conditions, and failure escalation |
| severity-levels | n/a | references/severity-levels.md | shared | review or risk classification | P0-P3 severity model and fixed review verdict mapping |
| impact-analysis | skills/10-impact-analysis/SKILL.md | references/impact-analysis-core.md | pre-execution | non-trivial implementation | identify affected entry points, contracts, data, permissions, tests |
| compatibility-impact-analysis | n/a | references/compatibility-impact-analysis.md | extension | compatibility or version risk | check coexistence, fallback, upgrade, downgrade, and matrix coverage |
| tdd-workflow | skills/15-tdd-workflow/SKILL.md | references/tdd-workflow-core.md | pre-execution | code change requires Red Green Refactor | enforce failing check, minimal implementation, and post-pass refactor |
| daily-development | skills/20-daily-development/SKILL.md | references/daily-development-core.md | execution | normal feature or scoped change | guide implementation after routing and impact analysis |
| code-review | skills/90-code-review/SKILL.md | references/code-review-core.md | review | review task or review alignment | findings-first review with evidence and severity classification |
| official-docs-review-extension | n/a | references/official-docs-review-extension.md | review | review of platform-sensitive implementation | verify official platform, framework, SDK, host, and design-guideline compliance |
| release-check | skills/70-release-check/SKILL.md | references/release-check-core.md | execution | packaging, rollout, install, deploy, go-live | validate release readiness, rollback, degradation, and observability |
| ui-implementation | skills/30-ui-implementation/SKILL.md | references/ui-implementation-core.md | execution | UI implementation or visual flow | cover hierarchy, states, real binding, layout, and accessibility |
| ui-review-extension | n/a | references/ui-review-extension.md | review | review UI implementation | verify states, bindings, visual fit, and usability |
| bug-fix | skills/40-bug-fix/SKILL.md | references/bug-fix-core.md | execution | concrete defect | require diagnosis, reproduction, evidence, root cause, and regression |
| bug-fix-review-extension | n/a | references/bug-fix-review-extension.md | review | review bug fix | verify reproduction, root cause, minimal repair, and regression coverage |
| migration-refactor | skills/50-migration-refactor/SKILL.md | references/migration-refactor-core.md | execution | refactor or migration | freeze behavior, plan slices, compatibility, and rollback |
| migration-refactor-review-extension | n/a | references/migration-refactor-review-extension.md | review | review refactor or migration | verify baseline, behavior preservation, compatibility, and rollback |
| ai-llm-feature | skills/60-ai-llm-feature/SKILL.md | references/ai-llm-feature-core.md | execution | AI, LLM, agent, tool, or memory work | bound tools, memory, iterations, observability, and cost |
| ai-llm-review-extension | n/a | references/ai-llm-review-extension.md | review | review AI or agent work | verify AI contract, bounds, real integration, and fallback |
| performance-impact-analysis | skills/25-performance-impact-analysis/SKILL.md | references/performance-impact-core.md | extension | hot path or scale-sensitive change | identify performance risk, limits, measurement, and assumptions |
| performance-review-extension | n/a | references/performance-review-extension.md | review | review performance-sensitive change | verify scale strategy, measurement, and risk handling |
| failure-retrospective-core | skills/45-failure-retrospective/SKILL.md | references/failure-retrospective-core.md | pre-execution | repeated failed repair | stop trial-and-error, rebuild evidence, define new validation |
| dynamic-reroute-core | n/a | references/dynamic-reroute-core.md | meta | route no longer matches facts | update routing, disclosure, project understanding, and Task Contract when risk or phase changes |
| performance-review-core | skills/85-performance-review/SKILL.md | references/performance-review-core.md | review | performance-focused review | verify hot path, bounds, measurements, and observability |
| playbook-conventions | n/a | references/playbook-conventions.md | playbook | creating or loading playbooks | define focused issue-specific playbook packaging |
| playbook-index | n/a | references/playbook-index.md | playbook | deciding concrete playbooks | map issue classes to concrete playbook paths |
| project-rule-index-conventions | n/a | references/project-rule-index-conventions.md | project | creating project rule packs | define versioned project index and review companion rules |
| selective-project-loading | n/a | references/selective-project-loading.md | project | project known but domain partial | load project index first, then only matching domain files |
| review-mirroring-rules | n/a | references/review-mirroring-rules.md | review | review follows implementation rules | mirror loaded implementation rules into review checks |
| report-templates | n/a | references/report-templates.md | shared | report output needed | provide compact-by-default routing, official-docs, rule-loading, project-understanding, impact-analysis, Task Contract, completion, bug, and review templates |
