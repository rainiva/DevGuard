---
name: devguard
description: Progressive-loading AI development guardrails for coding, bug fixing, UI implementation, refactors, reviews, release checks, and project-rule orchestration. Use when Codex should first route a task, classify risk and complexity, perform CodeGraph-first project understanding, confirm official platform or framework constraints before impact analysis when required, load only the minimum required rules, emit the right rule-loading disclosure, freeze a Task Contract before execution, enforce TDD/evidence/blocking gates, or dynamically reroute as new facts appear.
---

# DevGuard

DevGuard is the orchestration skill for a modular AI engineering rule system. Use it to decide how work should proceed, not to replace the domain skill that actually implements the work.

## Core Responsibilities

Do these things:

1. Understand the user intent and identify the real task type.
2. Classify risk tags, complexity level, and execution mode.
3. Choose the minimum skill chain and rule-loading plan.
4. Emit compact pre-execution output before execution begins: `Execution Summary` by default, always keep `Task Contract Summary` visible once it exists, use focused expansion for risky or anomalous parts, and use full manifests or full reports only when the user or audit-style mode explicitly requires them.
5. Run project understanding at the routed rigor before impact analysis when the task changes code or structure.
6. Run official docs check before impact analysis when platform, framework, SDK, host, control-template, system-API, or official design constraints may govern the implementation.
7. Run impact analysis at the routed rigor before non-trivial execution work and freeze a Task Contract before coding, repair, or refactor work starts.
8. Enforce stage gates for evidence, TDD, review, and blocking conditions.
9. Dynamically reroute when new facts change the risk profile, scope boundary, or acceptance bar.
10. Keep verified facts, executed actions, and unverified assumptions clearly separated.

Do not do these things:

1. Do not directly replace a feature, bug-fix, UI, migration, or review skill.
2. Do not load every rule file up front "for safety."
3. Do not claim completion without evidence.
4. Do not let execution begin before the required rule-loading output exists.
5. Do not let impact analysis begin before required project understanding or official docs check exists.
6. Do not let coding, repair, or refactor work begin before the required Task Contract exists.

## Default Workflow

Follow this sequence:

1. Route the task with [task-routing.md](references/task-routing.md).
2. Build the load plan with [rule-loading.md](references/rule-loading.md).
3. Apply the universal gates in [shared-guardrails.md](references/shared-guardrails.md).
4. Emit pre-execution output using [report-templates.md](references/report-templates.md); keep disclosure compact by default with `Execution Summary`, and when risk or anomalies appear expand only the affected parts unless full detail is explicitly required.
5. If the task will change code, UI, behavior, contracts, or data, run project understanding first, then required official docs check, then impact analysis, then freeze the required Task Contract before execution; keep `Task Contract Summary` visible by default and use only focused expansion for risky sections unless explicit detailed disclosure is required.
6. Hand off to the selected execution skill chain.
7. Re-run routing if the task changes, fails repeatedly, or enters review or release stages.

## Internal Skill Modules

DevGuard is the external skill name. Internally, route work through the modular skill files under `skills/` when a task needs a concrete execution lane.

- `skills/00-task-router/SKILL.md`
- `skills/10-impact-analysis/SKILL.md`
- `skills/12-codegraph-project-understanding/SKILL.md`
- `skills/13-official-docs-check/SKILL.md`
- `skills/15-tdd-workflow/SKILL.md`
- `skills/20-daily-development/SKILL.md`
- `skills/25-performance-impact-analysis/SKILL.md`
- `skills/30-ui-implementation/SKILL.md`
- `skills/40-bug-fix/SKILL.md`
- `skills/45-failure-retrospective/SKILL.md`
- `skills/50-migration-refactor/SKILL.md`
- `skills/60-ai-llm-feature/SKILL.md`
- `skills/70-release-check/SKILL.md`
- `skills/85-performance-review/SKILL.md`
- `skills/90-code-review/SKILL.md`

## What To Read And When

- Read [task-routing.md](references/task-routing.md) for task types, risk tags, complexity levels, execution modes, and default skill chains.
- Read [rule-loading.md](references/rule-loading.md) when deciding what to load now, what to defer, and what budgets apply in `FAST`, `STANDARD`, or `STRICT` mode.
- Read [rule-disclosure-index.md](references/rule-disclosure-index.md) during routing to use metadata first, summaries second, and full files only when the stage requires them.
- Read [shared-guardrails.md](references/shared-guardrails.md) before execution when you need the TDD floor, evidence rules, blocking conditions, or dynamic reroute triggers.
- Read [severity-levels.md](references/severity-levels.md) when classifying review findings, blockers, or routing risk.
- Read [report-templates.md](references/report-templates.md) when you need the routing report, rule-loading summary, detailed manifest, project understanding report, Impact Analysis, Task Contract, development report, bug-fix report, or review report structure.
- Read [codegraph-project-understanding.md](references/codegraph-project-understanding.md) before impact analysis when the task needs structural project understanding.
- Read [official-docs-check.md](references/official-docs-check.md) before impact analysis when platform, framework, SDK, host, control-template, system-API, or design-guideline constraints may govern the implementation.
- Read [impact-analysis-core.md](references/impact-analysis-core.md) before any non-trivial implementation, refactor, or migration work.
- Read [compatibility-impact-analysis.md](references/compatibility-impact-analysis.md) when a task touches platform, version, environment, or backward-compatibility behavior.
- Read [tdd-workflow-core.md](references/tdd-workflow-core.md) when code changes should follow `Red -> Green -> Refactor`.
- Read [daily-development-core.md](references/daily-development-core.md) for normal feature or change execution after routing is complete.
- Read [code-review-core.md](references/code-review-core.md) when the task enters review or when you need the review acceptance frame during implementation.
- Read [official-docs-review-extension.md](references/official-docs-review-extension.md) when review must verify compliance with official platform, framework, SDK, host, or design guidance.
- Read [release-check-core.md](references/release-check-core.md) when a task affects packaging, rollout, rollback, or go-live safety.
- Read [ui-implementation-core.md](references/ui-implementation-core.md) and [ui-review-extension.md](references/ui-review-extension.md) for UI implementation or visual flow changes.
- Read [bug-fix-core.md](references/bug-fix-core.md) and [bug-fix-review-extension.md](references/bug-fix-review-extension.md) when fixing concrete defects.
- Read [migration-refactor-core.md](references/migration-refactor-core.md) and [migration-refactor-review-extension.md](references/migration-refactor-review-extension.md) for structural reshaping, compatibility refactors, or migrations.
- Read [ai-llm-feature-core.md](references/ai-llm-feature-core.md) and [ai-llm-review-extension.md](references/ai-llm-review-extension.md) for AI, agent, tool-call, memory, or cost-sensitive flows.
- Read [performance-impact-core.md](references/performance-impact-core.md) and [performance-review-extension.md](references/performance-review-extension.md) when performance risk, throughput, latency, or scale behavior is part of the task.
- Read [performance-review-core.md](references/performance-review-core.md) when a review task is primarily about performance readiness.
- Read [failure-retrospective-core.md](references/failure-retrospective-core.md) after two failed repair attempts or when repair quality is collapsing into trial and error.
- Read [dynamic-reroute-core.md](references/dynamic-reroute-core.md) when new facts change task type, risk, mode, or loaded-rule sufficiency.
- Read [playbook-conventions.md](references/playbook-conventions.md) when the task needs issue-specific troubleshooting or handling guides.
- Read [playbook-index.md](references/playbook-index.md) when deciding which concrete playbook, if any, matches a bug or review task.
- Read [project-rule-index-conventions.md](references/project-rule-index-conventions.md) and [selective-project-loading.md](references/selective-project-loading.md) when shaping or loading project-specific rule packs.
- Read [review-mirroring-rules.md](references/review-mirroring-rules.md) when deciding how development-side rule loading must map into review-side verification.
- Read [example-prompts.md](references/example-prompts.md) when you need ready-to-use prompt shapes for realistic DevGuard invocations.
- Read [forward-testing.md](references/forward-testing.md) when validating DevGuard with fresh-agent scenarios.
- Read [batch-roadmap.md](references/batch-roadmap.md) only when extending DevGuard itself and deciding what the next implementation slice should add.

## Helper Scripts

- Run `python scripts/generate_rule_loading_manifest.py --format summary ...` as the canonical generator for the default outward packet. It emits `Execution Summary` and appends `Task Contract Summary` when contract fields are provided.
- Run `python scripts/generate_rule_loading_manifest.py --format rule-summary ...` only when a standalone `Rule-Loading Summary` is explicitly needed.
- Run `python scripts/generate_rule_loading_manifest.py --format risk` or `--format exception` for the default outward packet plus focused expansion, and `--format full` only when explicit detailed disclosure is required.
- Run `python scripts/check_devguard_bundle.py` to verify that the expected DevGuard bundle files exist before installing or forward-testing.

## Operating Rules

- Prefer summary-level guidance first and full details only when the current stage truly needs them.
- Separate execution rigor from disclosure size. Internal reasoning may be richer, but default external output should stay compact unless traceability or explicit user mode requires expansion.
- Default outward pre-execution disclosure should normally be `Execution Summary` plus `Task Contract Summary`. Do not hide the Task Contract in default mode once execution is being prepared.
- Render summary disclosures as standalone record blocks: start directly with the summary heading, keep each field on its own bullet line, and keep conversational explanation outside the block.
- Even in high-risk or anomaly cases, expand only the risky or anomalous sections by default. Do not dump unrelated detail from the rest of the route, analysis, or contract.
- Prefer CodeGraph or equivalent structural project-understanding tools over plain full-text search when the task changes code.
- Let project understanding establish structural facts first, let official docs check establish platform or framework constraints second, then let impact analysis reason about change impact, then let the Task Contract freeze execution.
- Let impact analysis fan out to identify possible impact and risk, then use the Task Contract to converge the approved goal, scope, constraints, tests, and acceptance criteria.
- Except for headings, field labels, literal status values, rule names, paths, code identifiers, and predefined keywords, DevGuard output prose should be written in Chinese.
- Keep all references one hop away from this file. Do not build deep reference chains.
- Treat project rules as higher priority than generic rules, but only load the project files that the current task actually hits.
- If a required rule file is missing, say so explicitly and mark the task blocked or partially routed instead of inventing the missing rule.
- If the same problem fails twice without new evidence, reroute into failure analysis before trying a third fix.

## Current Scope

The current implementation covers:

- Task routing
- Progressive rule loading
- Summary-first `Execution Summary` plus visible `Task Contract Summary`, with focused risk expansion by default and full expansion only when explicitly required
- Tiered rule-loading disclosure with summary, focused risk or anomaly expansion, and detailed manifest
- CodeGraph-first project understanding with depth-based outputs and fallback paths
- Official platform, framework, SDK, host, and design-guideline checks before impact analysis when required
- Tiered Impact Analysis output with summary, full analysis, and strict additions
- Shared gates
- Task Contract gating before execution
- Severity classification
- Reporting templates
- Internal modular skill files under `skills/`
- Execution-core references for impact analysis, TDD, daily development, review, and release checks
- High-frequency domain cores for UI, bug fixing, refactor or migration, AI or LLM work, and performance impact
- Compatibility impact analysis, failure retrospective, dynamic reroute, and performance review lanes
- Paired review extensions for those high-frequency domains
- Official docs review coverage for platform-sensitive work
- Playbook packaging conventions
- Concrete playbook index for WPF UI, WPF scrollbar, API contract, frontend performance, and AI memory issues
- Project-rule indexing and selective loading guidance
- Sample playbooks and sample project-rule pack
- Review mirroring rules for matching implementation and review surfaces
- Helper scripts for bundle checks and manifest generation
- Example prompts and forward-testing guidance

The current implementation includes sample project-rule and playbook packs. Real projects should add their own packs under `project-rules/<project>/` instead of editing generic core files.
