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

## Primary Risk Tags

Use only these twelve tags to drive execution mode, complexity escalation, and gate depth. Apply only tags supported by current facts:

- `api_contract`
- `auth_permission`
- `data_consistency`
- `migration`
- `release`
- `security`
- `performance`
- `official_docs_required`
- `codegraph_required`
- `compatibility`
- `ai_output`
- `ux_flow`

## Secondary Risk Tags

Apply when supported by current facts, but do not use Secondary tags alone to choose `FAST`, `STANDARD`, or `STRICT`. Load extensions, playbooks, or focused checks when relevant:

- `ui_binding`
- `state_machine`
- `frontend_state`
- `secret`
- `privacy`
- `tool_call`
- `memory`
- `dependency`
- `i18n_time`
- `observability`
- `rollback`
- `degradation`
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
- `project_understanding`
- `call_graph`
- `symbol_reference`
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
- `S1-micro`: daily micro-edit in one known file with user-specified location and no structural uncertainty; typical for `LITE` execute.
- `S1`: small low-risk change in one file or a few tightly scoped files.
- `S2`: medium change across multiple modules or UI plus logic.
- `S3`: high-risk change touching contracts, data, permissions, config, or release surfaces.
- `S4`: critical-path change involving auth, payments, orders, state machines, migrations, AI tool chains, or long-term memory.

## Execution Modes

- `LITE`: daily micro-tasks and routing preview. For **execute**: one known file, no Primary risk tags, not `bugfix`, freeze a **Micro Slice** inside `Execution Summary`, skip project understanding / impact analysis / official docs when the whitelist matches. For **preview**: route only, no Slice, no code. Lighter than `FAST` in outward shape and rule load; does **not** relax P0 gates once code changes.
- `FAST`: low-risk small work. Load meta rules, the relevant core skill, the minimum review floor, and only the smallest required project-understanding, impact-analysis, and TDD layers.
- `STANDARD`: normal engineering work. Load meta rules, project understanding, the relevant core skill, required extensions, required project rules, impact analysis, TDD, and code review.
- `STRICT`: high-risk work. Load meta rules, deep project understanding, core skill, multiple extensions, project rules, playbooks, impact analysis, TDD, review extensions, release or rollback controls, and explicit confirmation points.

Execution mode decides process rigor. It does not force full default disclosure.

## LITE Mode

Use `LITE` for very small daily execution **or** routing preview.

### LITE execute whitelist

All must be true before `LITE` execute and code changes:

1. single file, or the same file with at most three tightly related edits
2. file and intent are already specified; no structural uncertainty
3. no active Primary risk tag
4. task family is **not** `bugfix`, `ui`, `release`, `migration`, `security`, or `ai_llm`
5. no platform, SDK, auth, data, API contract, or user-visible flow change
6. Micro Slice is frozen in `Execution Summary` before editing — see [report-templates.md](report-templates.md)

### LITE preview

When the user wants routing only (`/devguard lite` + no implementation), emit `Execution Summary` only. Do not freeze Slice. Do not edit code.

### Upgrade off LITE

Reroute to `FAST` or `STANDARD` and switch to `Task Contract Summary` when any of these appears:

1. `bugfix` or broken-behavior repair
2. multiple modules, unclear entry points, or Primary risk tags
3. UI, platform, official-docs, or security surfaces
4. user expands scope beyond the frozen Slice
5. CodeGraph or structural understanding becomes necessary

Explain the upgrade in `Execution Summary` or a short `Risk Note`. Do not stay on `LITE` to avoid Evidence Gate or Contract requirements.

## Gate Matrix

Use this matrix to decide which pre-execution gates are required before coding, repair, or refactor. `LITE` is for daily micro-edits; `FAST` must not over-gate small work; `STRICT` must not skip gates on high-risk surfaces.

| Gate | S0 | LITE execute | S1 / FAST | S2 / STANDARD | S3+ / STRICT |
|---|---|---|---|---|---|
| Socratic Inquiry | conditional | no | conditional | conditional | conditional |
| Project Understanding | no | no | light / conditional | yes | deep |
| Official Docs Check | no | no | conditional | conditional | yes |
| Impact Analysis | no | no | light | yes | deep |
| Contract freeze | no | **Micro Slice** | compact TCS | yes | strict |
| TDD Red | no | Done check in Slice | repro may substitute | yes | yes |

Gate notes:

- **Socratic Inquiry** runs after routing when the smart gate fires. See [socratic-inquiry-core.md](socratic-inquiry-core.md). Skip when `LITE` execute whitelist matches or Task Profile is already unambiguous. While `Status: INQUIRY`, do not freeze Task Contract or start required project understanding.
- `S0` consultative work may require Socratic inquiry when deliverable shape is unclear; it still skips coding gates.
- `LITE execute` uses **Micro Slice** (Goal / Edit / Done) inside `Execution Summary` instead of a separate `Task Contract Summary`. No project understanding, impact analysis, or official docs when the whitelist matches.
- `LITE` does **not** apply to `bugfix`; bug fixes require at least `FAST` and the Evidence Gate.
- `S1 / FAST` still requires a compact Task Contract before code changes, but may use a minimal reproduction instead of a full failing test when risk is truly local and the task family is **not** `bugfix`.
- `S2 / STANDARD` requires project understanding, impact analysis, Task Contract, and TDD Red before implementation.
- `S3+ / STRICT` upgrades project understanding, official docs check, and impact analysis depth; Task Contract must stay tighter than the impact analysis.
- Official Docs Check stays conditional in `FAST` and `STANDARD` unless a Primary tag such as `official_docs_required`, `compatibility`, or platform-facing `security` is active.

## Default Skill Chains

Phase labels: **[Orient]** route / Socratic? / load plan / ES+TCS · **[Prepare]** PU / docs? / IA / Contract · **[Act]** TDD / domain / review. See [control-plane-core.md](control-plane-core.md).

`socratic-inquiry?` means run Socratic inquiry only when the Socratic Gate in [socratic-inquiry-core.md](socratic-inquiry-core.md) fires. `official-docs-check?` means route the check only when the Official Docs Check Gate says platform, framework, SDK, host, control-template, lifecycle, threading, permission, installer, component-library, or design constraints may govern the task. `task-contract-freeze` means freeze the Task Contract from `references/report-templates.md` before TDD or execution.

- New feature: `socratic-inquiry? -> codegraph-project-understanding -> official-docs-check? -> impact-analysis -> task-contract-freeze -> tdd-workflow -> daily-development -> code-review` — Orient through socratic?; Prepare through contract-freeze; Act thereafter
- UI implementation: `socratic-inquiry? -> codegraph-project-understanding -> official-docs-check? -> impact-analysis -> task-contract-freeze -> tdd-workflow -> ui-implementation -> code-review` — Orient · Prepare · Act
- Bug fix: `socratic-inquiry? -> codegraph-project-understanding -> official-docs-check? -> bug-fix(diagnosis-only) -> impact-analysis -> task-contract-freeze -> tdd-workflow -> bug-fix(minimal-repair) -> code-review` — Orient · Prepare · Act
- WPF or desktop UI bug: `socratic-inquiry? -> codegraph-project-understanding -> official-docs-check? -> bug-fix(diagnosis-only) -> compatibility-impact-analysis -> impact-analysis -> task-contract-freeze -> tdd-workflow -> ui-implementation -> bug-fix(regression-verification) -> code-review` — Orient · Prepare · Act
- Performance-sensitive change: `socratic-inquiry? -> codegraph-project-understanding -> official-docs-check? -> impact-analysis -> performance-impact-analysis -> task-contract-freeze -> tdd-workflow -> daily-development -> performance-review-core -> code-review` — Orient · Prepare · Act
- Refactor or migration: `socratic-inquiry? -> codegraph-project-understanding -> official-docs-check? -> impact-analysis -> migration-refactor -> task-contract-freeze -> tdd-workflow -> code-review -> release-check` — Orient · Prepare · Act (+ release in Act)
- AI or LLM feature: `socratic-inquiry? -> codegraph-project-understanding -> official-docs-check? -> impact-analysis -> task-contract-freeze -> ai-llm-feature -> tdd-workflow -> code-review` — Orient · Prepare · Act
- Release or go-live: `release-check` — Act only
- Repeated failed repair: `codegraph-project-understanding -> official-docs-check? -> failure-retrospective-core -> bug-fix(diagnosis-only) -> impact-analysis -> dynamic-reroute-core -> task-contract-freeze -> tdd-workflow -> bug-fix(minimal-repair) -> code-review` — Orient entry via reroute; Prepare through contract-freeze; Act thereafter
- LITE daily micro-edit: `task-contract-freeze(micro-slice) -> daily-development` — Orient (router) · Prepare (micro-slice) · Act

## Named Routes

Use these preset route IDs when routing output needs a stable label. Expected rule counts follow [rule-loading.md](rule-loading.md) budgets: core + extensions, excluding meta rules and mandatory pre-execution gates.

| Route ID | Mode | Complexity | Phases | Skill chain | Expected rules (core + ext) |
|---|---|---|---|---|---|
| `route:feature-normal` | STANDARD | S2 | O→P→A | New feature chain | 4-6 |
| `route:ui-implementation` | STANDARD | S2 | O→P→A | UI implementation chain | 4-7 |
| `route:bugfix-standard` | STANDARD | S2 | O→P→A | Bug fix chain | 4-6 |
| `route:bugfix-desktop-ui` | STANDARD | S2-S3 | O→P→A | WPF or desktop UI bug chain | 5-8 |
| `route:refactor-migration` | STANDARD / STRICT | S2-S4 | O→P→A | Refactor or migration chain | 5-9 |
| `route:performance-change` | STANDARD / STRICT | S2-S3 | O→P→A | Performance-sensitive change chain | 5-8 |
| `route:ai-llm-feature` | STANDARD / STRICT | S2-S4 | O→P→A | AI or LLM feature chain | 5-9 |
| `route:review-only` | FAST / STANDARD | S0-S2 | O→A | `code-review` (+ review extensions as needed) | 2-5 |
| `route:lite-daily` | LITE | S1-micro | O→P→A | LITE daily micro-edit chain | 1-2 |

Pick the Named Route that best matches the Default Skill Chain. If the chain diverges materially, reroute instead of forcing the preset label.

## Task Profile

Before execution, turn the request into a compact Task Profile that states:

1. the real problem to solve
2. the requested outcome
3. explicit non-goals
4. the surfaces that may be touched, such as pages, modules, APIs, data, permissions, or states
5. the task family, such as bugfix, UI, feature, refactor, performance, or release

Task Profile is exploratory. It prepares project understanding, impact analysis, and Task Contract generation, but it does not freeze execution scope yet.

When the Socratic Gate fires, refine Task Profile through [socratic-inquiry-core.md](socratic-inquiry-core.md) before project understanding or contract freeze.

## Socratic Inquiry Gate

Default to **skip** Socratic inquiry when intent is already concrete enough to route safely.

Require Socratic inquiry when any of these is true:

1. success criteria are missing, vague, or untestable
2. multiple materially different interpretations remain open
3. scope boundary would change routing or contract shape
4. conflicting constraints lack an explicit priority rule
5. non-goals matter but cannot be inferred safely
6. `S0` consultative work where deliverable shape is still unclear

Always skip when `LITE` execute whitelist fully matches.

While inquiry is active, set outward `Status: INQUIRY`, emit `Inquiry Note`, and do not freeze Task Contract.

## Project Understanding Gate

Default to required project understanding for any code-modifying task unless the task is clearly one of these:

1. documentation-only work
2. a tiny copy or text tweak inside a single already-known file
3. a user-specified single-line or single-location edit with no structural uncertainty
4. pure consultation with no code change

When project understanding is required, place it before impact analysis and before any Task Contract.

If CodeGraph is unavailable after repair, apply the No-Index Fallback in [codegraph-project-understanding.md](codegraph-project-understanding.md) and record `Structural tool` in `Execution Summary`.

## Official Docs Check Gate

Default to required official docs check when the task touches platform, framework, SDK, system API, host-integration, control-template, lifecycle, threading-model, permission, installer, service, registry, startup, ORM, AI SDK, MCP integration, UI component libraries, or platform-design constraints.

Usually skip only when the task is clearly local business logic, documentation-only work, or a tiny text change with no platform-facing behavior.

When official docs check is required, place it after project understanding and before impact analysis.

Do not query broad official documentation packs or load official docs broadly. First identify the specific platform surface from project understanding, then load only the official material for that API, control, SDK, host behavior, lifecycle rule, or design guideline.

If Context7 or an equivalent official-docs MCP is available, use L1 first for scoped summary when L2 is not yet required.

Pick official-docs depth per [official-docs-check.md](official-docs-check.md): **L1** Context7 summary for ordinary platform touch; **L2** original-doc verification for `S3+`, deprecated APIs, permission, installer, or security surfaces; **L3** human confirmation for `STRICT` plus release or go-live.

If the task hits L2 triggers, require original official docs or API-reference verification before treating guidance as authoritative.

## Output Detail Decisions

Keep internal routing rigor and external disclosure size separate.

- `summary`: use `Execution Summary` plus `Task Contract Summary` as the default outward packet, except `LITE execute` uses `Execution Summary` with embedded `Slice` only.
- `focused-expansion`: keep the summary outputs, then add only the focused expansion blocks for the risky or anomalous parts, including official-docs findings when they materially constrain the task.
- `detailed`: use full `Skill Routing Decision`, full `CodeGraph Project Understanding Report`, full `Official Docs Check Report`, full `Impact Analysis`, and full `Task Contract`. Add strict sections only when the detailed request intersects with strict-risk work.

In `summary` mode, keep `Project Understanding Summary`, `Impact Analysis Summary`, and `Official Docs Check Summary` as internal records by default. Do not emit them as peer outward blocks unless they contain a blocker, anomaly, implementation-changing official constraint, reroute trigger, or risk that cannot fit in `Risk Note` or `Exception Note`.

Default to `summary` for ordinary `LITE`, `FAST`, and `STANDARD` work.

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
- `socratic-inquiry?`: optional `skills/05-socratic-inquiry/SKILL.md` and `references/socratic-inquiry-core.md`, loaded only when the Socratic Inquiry Gate requires it
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

### Short Invocation Triggers

When the user prepends a short trigger, apply it before default routing heuristics:

| Trigger | Execution mode | Route bias |
|---|---|---|
| `/devguard lite` | `LITE` | micro daily execute when whitelist matches; preview-only when user asks not to code |
| `/devguard fast` | `FAST` | smallest gates and rule load allowed by Gate Matrix |
| `/devguard strict` | `STRICT` | deep gates; focused expansion on risk |
| `/devguard review` | review-only | `route:review-only`; no implementation |

If the trigger conflicts with evident task risk (for example `strict` work labeled `fast`), keep the safer gates and explain the override in `Risk Note`.

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
- Keep stage summaries internal in default mode; outward output should remain `Execution Summary` plus visible `Task Contract Summary` for `FAST` and above, or `Execution Summary` with embedded `Slice` for `LITE execute`, unless a focused `Risk Note` or `Exception Note` is needed.
- Keep `Task Contract Summary` visible in default mode once execution is being prepared for `FAST` and above; `LITE execute` uses Micro Slice instead of a separate TCS block.
- Do not let `STRICT` execution mode automatically force full outward disclosure; prefer focused expansion unless the user or stage explicitly needs the full record.
- If project identity is known, load only the project rule index first, then the matching project files.
- If the task changes phase, reroute it. Development, review, release, and failure analysis are different phases.
