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

## Rule Index

| Rule | Path | Layer | Metadata trigger | Summary |
|---|---|---|---|---|
| task-routing | references/task-routing.md | meta | any routed task | classify task type, risk, complexity, mode, and skill chain |
| rule-loading | references/rule-loading.md | meta | any execution task | decide minimal loaded set, deferred rules, disclosure mode, project-understanding gating, and Task Contract gating |
| codegraph-project-understanding | references/codegraph-project-understanding.md | core | code change larger than tiny known local edit | locate entry points, call chains, similar implementations, and impact surfaces before impact analysis |
| official-docs-check | references/official-docs-check.md | core | platform, framework, SDK, host, control-template, system-API, or design-guideline constraints may matter | confirm official constraints before impact analysis and Task Contract freeze |
| shared-guardrails | references/shared-guardrails.md | shared | any gated task | evidence, TDD floor, blocking conditions, and failure escalation |
| severity-levels | references/severity-levels.md | shared | review or risk classification | P0-P3 severity model and fixed review verdict mapping |
| impact-analysis-core | references/impact-analysis-core.md | core | non-trivial implementation | identify affected entry points, contracts, data, permissions, tests |
| compatibility-impact-analysis | references/compatibility-impact-analysis.md | extension | compatibility or version risk | check coexistence, fallback, upgrade, downgrade, and matrix coverage |
| tdd-workflow-core | references/tdd-workflow-core.md | core | code change requires Red Green Refactor | enforce failing check, minimal implementation, and post-pass refactor |
| daily-development-core | references/daily-development-core.md | core | normal feature or scoped change | guide implementation after routing and impact analysis |
| code-review-core | references/code-review-core.md | review | review task or review alignment | findings-first review with evidence and severity classification |
| official-docs-review-extension | references/official-docs-review-extension.md | review | review of platform-sensitive implementation | verify official platform, framework, SDK, host, and design-guideline compliance |
| release-check-core | references/release-check-core.md | core | packaging, rollout, install, deploy, go-live | validate release readiness, rollback, degradation, and observability |
| ui-implementation-core | references/ui-implementation-core.md | core | UI implementation or visual flow | cover hierarchy, states, real binding, layout, and accessibility |
| ui-review-extension | references/ui-review-extension.md | review | review UI implementation | verify states, bindings, visual fit, and usability |
| bug-fix-core | references/bug-fix-core.md | core | concrete defect | require diagnosis, reproduction, evidence, root cause, and regression |
| bug-fix-review-extension | references/bug-fix-review-extension.md | review | review bug fix | verify reproduction, root cause, minimal repair, and regression coverage |
| migration-refactor-core | references/migration-refactor-core.md | core | refactor or migration | freeze behavior, plan slices, compatibility, and rollback |
| migration-refactor-review-extension | references/migration-refactor-review-extension.md | review | review refactor or migration | verify baseline, behavior preservation, compatibility, and rollback |
| ai-llm-feature-core | references/ai-llm-feature-core.md | core | AI, LLM, agent, tool, or memory work | bound tools, memory, iterations, observability, and cost |
| ai-llm-review-extension | references/ai-llm-review-extension.md | review | review AI or agent work | verify AI contract, bounds, real integration, and fallback |
| performance-impact-core | references/performance-impact-core.md | core | hot path or scale-sensitive change | identify performance risk, limits, measurement, and assumptions |
| performance-review-extension | references/performance-review-extension.md | review | review performance-sensitive change | verify scale strategy, measurement, and risk handling |
| failure-retrospective-core | references/failure-retrospective-core.md | core | repeated failed repair | stop trial-and-error, rebuild evidence, define new validation |
| dynamic-reroute-core | references/dynamic-reroute-core.md | core | route no longer matches facts | update routing, disclosure, project understanding, and Task Contract when risk or phase changes |
| performance-review-core | references/performance-review-core.md | review | performance-focused review | verify hot path, bounds, measurements, and observability |
| playbook-conventions | references/playbook-conventions.md | shared | creating or loading playbooks | define focused issue-specific playbook packaging |
| playbook-index | references/playbook-index.md | shared | deciding concrete playbooks | map issue classes to concrete playbook paths |
| project-rule-index-conventions | references/project-rule-index-conventions.md | shared | creating project rule packs | define versioned project index and review companion rules |
| selective-project-loading | references/selective-project-loading.md | shared | project known but domain partial | load project index first, then only matching domain files |
| review-mirroring-rules | references/review-mirroring-rules.md | shared | review follows implementation rules | mirror loaded implementation rules into review checks |
| report-templates | references/report-templates.md | shared | report output needed | provide compact-by-default routing, official-docs, rule-loading, project-understanding, impact-analysis, Task Contract, completion, bug, and review templates |
