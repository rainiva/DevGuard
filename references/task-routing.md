# Task Routing

Use this reference to classify the task before any execution begins.

## Task Types

Use one or more of these labels:

- `feature`
- `change`
- `ui`
- `bugfix`
- `refactor`
- `migration`
- `review`
- `release`
- `doc`
- `test`
- `config`
- `security`
- `data`
- `api`
- `ai_llm`
- `performance`

## Risk Tags

Apply only the tags supported by current facts:

- `ui_binding`
- `api_contract`
- `auth_permission`
- `data_consistency`
- `state_machine`
- `frontend_state`
- `security`
- `secret`
- `privacy`
- `performance`
- `migration`
- `release`
- `ai_output`
- `tool_call`
- `memory`
- `dependency`
- `i18n_time`
- `observability`
- `rollback`
- `degradation`
- `compatibility`
- `ux_flow`
- `data_lifecycle`
- `cost`
- `long_running_task`
- `cancelable_task`
- `recoverability`
- `filesystem`
- `multi_instance`
- `installation`
- `versioning`
- `mock_quality`
- `repair_failure`
- `codegraph_required`
- `project_understanding`
- `call_graph`
- `symbol_reference`
- `official_docs_required`
- `platform_api`
- `framework_lifecycle`
- `threading_model`
- `sdk_usage`
- `control_template`
- `host_compatibility`
- `deprecated_api`
- `platform_design`
- `native_ui_guideline`

## Complexity Levels

- `S0`: consultative, analysis-only, or documentation-only work with no code change.
- `S1`: small low-risk change in one file or a few tightly scoped files.
- `S2`: medium change across multiple modules or UI plus logic.
- `S3`: high-risk change touching contracts, data, permissions, config, or release surfaces.
- `S4`: critical-path change involving auth, payments, orders, state machines, migrations, AI tool chains, or long-term memory.

## Execution Modes

- `FAST`: low-risk small work. Load meta rules, the relevant core skill, the minimum review floor, and only the smallest required project-understanding, impact-analysis, and TDD layers.
- `STANDARD`: normal engineering work. Load meta rules, project understanding, the relevant core skill, required extensions, required project rules, impact analysis, TDD, and code review.
- `STRICT`: high-risk work. Load meta rules, deep project understanding, core skill, multiple extensions, project rules, playbooks, impact analysis, TDD, review extensions, release or rollback controls, and explicit confirmation points.

Execution mode decides process rigor. It does not force full default disclosure.

## Default Skill Chains

`official-docs-check?` means route the check only when the Official Docs Check Gate says platform, framework, SDK, host, control-template, lifecycle, threading, permission, installer, component-library, or design constraints may govern the task. `task-contract-freeze` means freeze the Task Contract from `references/report-templates.md` before TDD or execution.

- New feature: `codegraph-project-understanding -> official-docs-check? -> impact-analysis -> task-contract-freeze -> tdd-workflow -> daily-development -> code-review`
- UI implementation: `codegraph-project-understanding -> official-docs-check? -> impact-analysis -> task-contract-freeze -> tdd-workflow -> ui-implementation -> code-review`
- Bug fix: `codegraph-project-understanding -> official-docs-check? -> bug-fix(diagnosis-only) -> impact-analysis -> task-contract-freeze -> tdd-workflow -> bug-fix(minimal-repair) -> code-review`
- WPF or desktop UI bug: `codegraph-project-understanding -> official-docs-check? -> bug-fix(diagnosis-only) -> compatibility-impact-analysis -> impact-analysis -> task-contract-freeze -> tdd-workflow -> ui-implementation -> bug-fix(regression-verification) -> code-review`
- Performance-sensitive change: `codegraph-project-understanding -> official-docs-check? -> impact-analysis -> performance-impact-analysis -> task-contract-freeze -> tdd-workflow -> daily-development -> performance-review-core -> code-review`
- Refactor or migration: `codegraph-project-understanding -> official-docs-check? -> impact-analysis -> migration-refactor -> task-contract-freeze -> tdd-workflow -> code-review -> release-check`
- AI or LLM feature: `codegraph-project-understanding -> official-docs-check? -> impact-analysis -> task-contract-freeze -> ai-llm-feature -> tdd-workflow -> code-review`
- Release or go-live: `release-check`
- Repeated failed repair: `codegraph-project-understanding -> official-docs-check? -> failure-retrospective-core -> bug-fix(diagnosis-only) -> impact-analysis -> dynamic-reroute-core -> task-contract-freeze -> tdd-workflow -> bug-fix(minimal-repair) -> code-review`

## Task Profile

Before execution, turn the request into a compact Task Profile that states:

1. the real problem to solve
2. the requested outcome
3. explicit non-goals
4. the surfaces that may be touched, such as pages, modules, APIs, data, permissions, or states
5. the task family, such as bugfix, UI, feature, refactor, performance, or release

Task Profile is exploratory. It prepares project understanding, impact analysis, and Task Contract generation, but it does not freeze execution scope yet.

## Project Understanding Gate

Default to required project understanding for any code-modifying task unless the task is clearly one of these:

1. documentation-only work
2. a tiny copy or text tweak inside a single already-known file
3. a user-specified single-line or single-location edit with no structural uncertainty
4. pure consultation with no code change

When project understanding is required, place it before impact analysis and before any Task Contract.

## Official Docs Check Gate

Default to required official docs check when the task touches platform, framework, SDK, system API, host-integration, control-template, lifecycle, threading-model, permission, installer, service, registry, startup, ORM, AI SDK, MCP integration, UI component libraries, or platform-design constraints.

Usually skip only when the task is clearly local business logic, documentation-only work, or a tiny text change with no platform-facing behavior.

When official docs check is required, place it after project understanding and before impact analysis.

Do not query broad official documentation packs or load official docs broadly. First identify the specific platform surface from project understanding, then load only the official material for that API, control, SDK, host behavior, lifecycle rule, or design guideline.

If Context7 or an equivalent official-docs MCP is available, use it first to fetch version-scoped official guidance for the exact surface identified by project understanding.

If the task is high-risk, lifecycle-sensitive, threading-sensitive, permission-sensitive, compatibility-sensitive, or already failed multiple times, require original official docs or API-reference verification before treating the official guidance as authoritative.

## Output Detail Decisions

Keep internal routing rigor and external disclosure size separate.

- `summary`: use `Execution Summary` plus `Task Contract Summary` as the default outward packet.
- `focused-expansion`: keep the summary outputs, then add only the focused expansion blocks for the risky or anomalous parts, including official-docs findings when they materially constrain the task.
- `detailed`: use full `Skill Routing Decision`, full `CodeGraph Project Understanding Report`, full `Official Docs Check Report`, full `Impact Analysis`, and full `Task Contract`. Add strict sections only when the detailed request intersects with strict-risk work.

Default to `summary` for ordinary `FAST` and `STANDARD` work.

Default to `focused-expansion` when one of these is true and the user did not explicitly ask for full detail:

1. the route contains anomalies, missing rules, missing evidence, or unclear blockers
2. complexity is `S3` or `S4`
3. execution mode is `STRICT`
4. the task touches high-risk shared surfaces such as release, migration, auth, permission, data lifecycle, or rollback-sensitive paths
5. rerouting after repeated failed repairs needs more local evidence

Expand to `detailed` only when one of these is true:

1. the user explicitly asks for detailed output, full detail, verbose mode, debug mode, or audit mode
2. the task is being used to forward-test DevGuard itself
3. a formal evidence-capture task explicitly requires the canonical full templates

## Implemented Route Targets

- `task-router`: `skills/00-task-router/SKILL.md` and `references/task-routing.md`
- `codegraph-project-understanding`: `skills/12-codegraph-project-understanding/SKILL.md` and `references/codegraph-project-understanding.md`
- `official-docs-check?`: optional `skills/13-official-docs-check/SKILL.md` and `references/official-docs-check.md`, loaded only when the Official Docs Check Gate requires it
- `impact-analysis`: `skills/10-impact-analysis/SKILL.md` and `references/impact-analysis-core.md`
- `task-contract-freeze`: freeze the contract using `references/report-templates.md`; this is a required stage, not a separate skill file
- `tdd-workflow`: `skills/15-tdd-workflow/SKILL.md` and `references/tdd-workflow-core.md`
- `daily-development`: `skills/20-daily-development/SKILL.md` and `references/daily-development-core.md`
- `performance-impact-analysis`: `skills/25-performance-impact-analysis/SKILL.md` and `references/performance-impact-core.md`
- `ui-implementation`: `skills/30-ui-implementation/SKILL.md` and `references/ui-implementation-core.md`
- `bug-fix`: `skills/40-bug-fix/SKILL.md` and `references/bug-fix-core.md`
- `failure-retrospective-core`: `skills/45-failure-retrospective/SKILL.md` and `references/failure-retrospective-core.md`
- `migration-refactor`: `skills/50-migration-refactor/SKILL.md` and `references/migration-refactor-core.md`
- `ai-llm-feature`: `skills/60-ai-llm-feature/SKILL.md` and `references/ai-llm-feature-core.md`
- `release-check`: `skills/70-release-check/SKILL.md` and `references/release-check-core.md`
- `performance-review-core`: `skills/85-performance-review/SKILL.md` and `references/performance-review-core.md`
- `code-review`: `skills/90-code-review/SKILL.md` and `references/code-review-core.md`
- `compatibility-impact-analysis`: `references/compatibility-impact-analysis.md`
- `dynamic-reroute-core`: `references/dynamic-reroute-core.md`

## Routing Output

Always decide the routing fields internally.

Default outward output for normal tasks should be `Execution Summary`.

Once execution is being prepared, keep `Task Contract Summary` visible by default.

Use `Routing Focused Expansion` when only the risky or anomalous routing parts need to be shown.

Use full `Skill Routing Decision` only when `detailed` disclosure is active.

In summary mode, do not duplicate loaded rule lists across multiple blocks; keep the loaded-rule disclosure compact inside `Execution Summary`.

The router should still determine:

1. User intent
2. Task Profile
3. Task type
4. Risk tags
5. Complexity level
6. Risk score
7. Execution mode
8. Project understanding requirement
9. Project understanding depth
10. Official docs requirement
11. Official docs depth
12. Rule-loading output mode
13. Impact Analysis depth
14. Task Contract depth
15. Skill chain
16. Needed extensions
17. Needed playbooks
18. Needed project rules
19. Needed review extensions
20. Stage gates
21. Dynamic reroute conditions
22. Human confirmation points

## Routing Discipline

- Route by actual task behavior, not by keyword matching alone.
- Prefer CodeGraph, symbol-index, call-graph, or structural project-understanding tools over plain full-text search when the task changes code.
- Mark project understanding required when entry points, call chains, similar implementations, or impact boundaries are not already trivial and local.
- Mark official docs check required when platform, framework, SDK, host, lifecycle, threading, control-template, permission, installer, component-library, MCP, or platform-design constraints could govern the implementation.
- Decide project-understanding, Impact Analysis, and Task Contract disclosure together: summary by default, focused expansion for risky or anomalous parts, and full detail only when explicitly required.
- Decide official-docs disclosure with the same principle: keep it internal or summary-level by default, and expand only when risk, anomaly, or explicit detailed mode requires it.
- Keep `Task Contract Summary` visible in default mode once execution is being prepared, even if routing and rule-loading output are compressed.
- Do not let `STRICT` execution mode automatically force full outward disclosure; prefer focused expansion unless the user or stage explicitly needs the full record.
- If project identity is known, load only the project rule index first, then the matching project files.
- If the task changes phase, reroute it. Development, review, release, and failure analysis are different phases.
