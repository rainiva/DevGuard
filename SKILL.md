---
name: devguard
description: Dev guardrails: route, gates, Contract, minimal rules. Use for code/bugfix/UI/review. Not for typo-only edits.
---

# DevGuard

Orchestration skill for modular AI engineering rules. Route and gate work; do not replace domain execution skills.

## Coexistence Rules

When DevGuard runs alongside domain execution skills (feature, bug-fix, UI, migration, review, etc.):

1. **DevGuard owns** routing, gates, Task Contract freeze, and rule loading.
2. **Domain skills own** concrete execution technique inside the frozen Contract.
3. **On conflict**, DevGuard gates win — do not skip Contract, evidence, or blocking rules.
4. **Do not duplicate** domain skill TDD, debug, or stack-specific detail inside DevGuard output.
5. **When the user names a domain skill explicitly**, DevGuard limits itself to routing + Contract; the named skill executes.

Short triggers: `/devguard fast`, `/devguard strict`, `/devguard review` — see [example-prompts.md](references/example-prompts.md).

## Core Responsibilities

Do:

1. Classify task type, risk, complexity, and execution mode.
2. Choose the minimum skill chain and rule-loading plan.
3. Emit compact pre-execution output (`Execution Summary`; keep `Task Contract Summary` visible once execution is prepared).
4. Run project understanding, then official docs check when required, then impact analysis, then freeze Task Contract before coding.
5. Enforce evidence, TDD, review, and blocking gates; reroute when facts change.
6. Keep every edit inside the [Minimum Change Constraint](references/shared-guardrails.md#minimum-change-constraint): simplest correct diff within frozen Task Contract scope.

Do not:

1. Replace feature, bug-fix, UI, migration, or review skills.
2. Load every rule file up front.
3. Start execution without rule-loading output or Task Contract when required.
4. Claim completion without evidence.
5. Expand edit scope, refactor drive-by, or add dependencies without reroute and Contract update.

## Default Workflow

1. Route with [task-routing.md](references/task-routing.md).
2. Plan loads with [rule-loading.md](references/rule-loading.md) and [rule-disclosure-index.md](references/rule-disclosure-index.md).
3. Apply gates in [shared-guardrails.md](references/shared-guardrails.md).
4. Emit output via [report-templates.md](references/report-templates.md) (default: `Execution Summary` + `Task Contract Summary`).
5. If code/behavior/data/UI changes: project understanding -> official docs check? -> impact analysis -> Task Contract freeze.
6. Hand off to the execution skill chain under `skills/`.
7. Reroute on phase change, repeated failure, or new blockers.

## Internal Skill Modules

| Module | Lane |
|---|---|
| `00-task-router` | routing |
| `10-impact-analysis` | impact analysis |
| `12-codegraph-project-understanding` | project understanding |
| `13-official-docs-check` | official docs |
| `15-tdd-workflow` | TDD |
| `20-daily-development` | feature/change |
| `25-performance-impact-analysis` | performance analysis |
| `30-ui-implementation` | UI |
| `40-bug-fix` | bug fix |
| `45-failure-retrospective` | repair failure |
| `50-migration-refactor` | refactor/migration |
| `60-ai-llm-feature` | AI/LLM |
| `70-release-check` | release |
| `85-performance-review` | performance review |
| `90-code-review` | review |

Full rule selection: [rule-disclosure-index.md](references/rule-disclosure-index.md). Term definitions: [glossary.md](references/glossary.md). Refinement plan: [docs/REFINEMENT_PLAN.md](docs/REFINEMENT_PLAN.md).

## Operating Rules

- Default outward output: `Execution Summary` + `Task Contract Summary`; use `Risk Note` or `Exception Note` only for high-risk or anomaly slices.
- Hard default-output cap: do not emit `Project Understanding Summary`, `Impact Analysis Summary`, or `Official Docs Check Summary` as separate outward blocks in default mode.
- Render summaries as standalone record blocks; keep conversation outside the block.
- Prefer CodeGraph for structural understanding; pass freshness gate before trusting index results.
- For user-visible UI work, require at least one test, reproduction, or acceptance check that exercises the real user operation path. Do not treat internal function, method, interface, or ideal-path-only checks as sufficient evidence for UI completion.
- Output prose in Chinese except headings, field labels, statuses, rule names, paths, and code identifiers.
- Project rules override generic rules when loaded; load only files the task hits.
- Same issue failed twice without new evidence: enter failure retrospective before a third attempt.
- For bug fixes: no repair code without a failing test or reproduction; prove red-before, then green-after, before claiming fixed.
- Minimum change: simplest correct diff inside frozen Task Contract scope; reroute before touching out-of-scope files or drive-by refactors. Canonical rule: [shared-guardrails.md](references/shared-guardrails.md#minimum-change-constraint).

## Helper Scripts

```bash
python scripts/generate_rule_loading_manifest.py --format summary ...
python scripts/generate_rule_loading_manifest.py --format rule-summary ...
python scripts/check_devguard_bundle.py
python scripts/gen_skillopt.py
```
