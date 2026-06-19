# Forward Testing

Use this when validating DevGuard itself with a fresh agent or a fresh thread.

## Goal

Test whether DevGuard can generalize from its own instructions instead of succeeding only because the evaluator leaked the intended answer.

## Core Rules

1. Use a fresh thread or fresh agent when possible.
2. Pass the skill path and a realistic user request.
3. Do not tell the tester what rule should load or what the correct answer is.
4. Review the tester's actual outward transcript blocks first, then review any internal routing, rule-loading, project-understanding, official-docs, and Task Contract decisions that justified them.
5. Clean up temporary artifacts if the forward test writes anything.

When default outward output is expected, judge the result by exact block shape, not by a subjective feeling that it is "compact enough."

## Good Prompt Shape

Use prompts like:

- `Use $devguard at <DEVGUARD_PATH> to route this medium-risk feature task, run project understanding before impact analysis, keep the outward output to Execution Summary plus Task Contract Summary, and freeze the Task Contract before coding.`
- `Use $devguard at <DEVGUARD_PATH> to route this medium-risk feature task, keep the outward routing, project-understanding, impact-analysis, and Task Contract output compact by default, and if risk appears expand only the affected parts unless I explicitly ask for full detail.`
- `Use $devguard at <DEVGUARD_PATH> to route this platform-sensitive task, confirm official platform or framework constraints before impact analysis, and block if the implementation would rely on unofficial assumptions.`
- `Use $devguard at <DEVGUARD_PATH> to handle this bug report. Reproduce first, load only the needed rules, and stop if the evidence chain is weak.`
- `Use $devguard at <DEVGUARD_PATH> to review this UI change and verify whether the implementation-side rules were mirrored into review.`
- `Use $devguard at <DEVGUARD_PATH> to route this multi-file refactor, prefer CodeGraph first for project understanding, attempt structural-tool repair before fallback, and keep the outward output compact unless a blocker appears.`
- `Use $devguard at <DEVGUARD_PATH> to route this multi-file change, verify CodeGraph index freshness before structural queries, refresh or rebuild the index if needed, and only then continue into impact analysis.`

## What To Check

Verify whether the test agent:

1. classifies task type, risk tags, and execution mode coherently
2. emits `Execution Summary` before execution and keeps `Task Contract Summary` visible by default once execution is being prepared
3. keeps routing, project-understanding, and impact-analysis disclosure compact by default for normal tasks
4. performs project understanding before impact analysis when the task changes code
5. performs official docs check before impact analysis when platform, framework, SDK, host, control-template, or design constraints matter
6. loads the right domain core and review extension pair
7. distinguishes verified facts from guesses
8. blocks or escalates when required
9. uses `Execution Summary` plus visible `Task Contract Summary` by default, uses focused expansion for risky or anomalous parts, and preserves the canonical detailed schemas only when explicit detailed mode is required
10. runs impact analysis before freezing the Task Contract for execution work
11. keeps the Task Contract tighter than the impact analysis instead of repeating exploratory uncertainty
12. attempts CodeGraph or lower-priority structural-tool repair before search-only fallback when the project-understanding toolchain is repairable
13. keeps the default outward transcript to the allowed block set for the route, instead of emitting extra peer stage summaries
14. checks CodeGraph index freshness before structural queries and refreshes or rebuilds a stale index before trusting it
15. for user-visible UI or interaction-flow work, requires at least one verification path that exercises real user operations instead of relying only on internal function, method, interface, or ideal-path checks
16. for completed work in default mode, uses `Completion Summary` instead of full completion reports
17. for review-only work in default mode, uses compact findings output or `Review Summary` instead of the 19-section `Review Report`
18. `Task Contract Summary` in T1 mode uses Goal / Scope / Tests / Acceptance, with optional one-line `Official constraint` when platform docs govern the slice
19. for bug fixes, blocks repair without a failing test or reproduction and requires red-before / green-after evidence before claiming fixed
20. keeps edits inside Task Contract scope and applies the Minimum Change Constraint — no drive-by refactors or scope creep without reroute
21. when CodeGraph is unavailable after repair, records `codegraph_unavailable`, applies No-Index Fallback, and sets `Structural tool` in `Execution Summary`
22. picks official-docs depth L1 / L2 / L3 correctly and keeps at most one `Official constraint` line in TCS
23. `LITE execute` freezes `Slice` inside `Execution Summary` and does not emit separate `Task Contract Summary`; `LITE` upgrades to `FAST`+ for bugfix or Primary-tag work

## Failure Signals

Treat these as forward-test failures:

- loads nearly everything by default
- skips the rule-loading disclosure
- skips required project understanding and jumps to impact analysis or coding
- skips required official docs check and still edits platform-sensitive code
- emits a full manifest table for a normal low-risk task without being asked
- emits a full routing decision, full project-understanding report, full Impact Analysis, or full Task Contract for a normal task without a real expansion trigger
- emits `Project Understanding Summary`, `Impact Analysis Summary`, or `Official Docs Check Summary` as peer outward blocks in default mode without a real expansion trigger
- emits the full detail for unrelated healthy surfaces when only one risky or anomalous slice needed expansion
- compresses a required full manifest into prose or omits required schema columns such as `Path`
- starts coding without the required Task Contract
- jumps into implementation before routing
- claims evidence that was never gathered
- ignores review mirroring
- misses obvious high-risk domain routing
- silently demotes from CodeGraph or another repairable structural tool to plain-search fallback without recording the concrete failure mode
- trusts CodeGraph results from a stale, unhealthy, incomplete, or wrong-root index without first repairing or refreshing it
- claims a user-visible UI or interaction-flow task is verified using only internal function, method, interface, or ideal-path checks
- emits `Development Completion Report`, `Bug-Fix Completion Report`, or the 19-section `Review Report` in default T1/T2 mode without explicit detailed-mode request
- emits legacy 4-field Task Contract labels (`Non-goals`, `Allowed edits`, `Acceptance criteria`) in default T1 outward output instead of Goal / Scope / Tests / Acceptance
- writes or applies bug-fix repair code before a failing test or reproduction exists
- claims a bug is fixed without red-before / green-after evidence
- weakens, deletes, or skips tests to force green on a bug-fix task
- touches files, dependencies, or behaviors outside frozen Task Contract scope without reroute
- bundles drive-by refactors, renames, or cleanup unrelated to the approved slice
- silently continues on a stale or unavailable CodeGraph index without No-Index Fallback disclosure
- puts long official-doc excerpts or multi-bullet platform rules into `Task Contract Summary` instead of one `Official constraint` line
- emits separate `Task Contract Summary` on a whitelist `LITE execute` task instead of embedded `Slice`
- keeps `Mode: LITE` for `bugfix`, auth, UI flow, or other Primary-tag work without upgrading to `FAST` or `STANDARD`

## Regression Example Set

Use these four regression scenarios after any change to DevGuard disclosure policy, routing output, Task Contract visibility rules, or official-docs disclosure behavior.

Any change to CodeGraph routing, freshness, repair, or fallback rules should also be checked against the freshness expectations below.

### 1. Normal Task Default Output

- Goal: verify the default outward packet stays minimal for an ordinary engineering task.
- Prompt:
  `Use $devguard at <DEVGUARD_PATH> to route this medium-risk feature task. Keep the default outward output compact, and freeze the Task Contract before coding.`
- Expected outward shape:
  1. `Execution Summary`
  2. `Task Contract Summary`
- Allowed extras:
  1. none, unless the task naturally discovers a real risk or anomaly
- Must not appear:
  1. `Risk Note`
  2. `Exception Note`
  3. `Project Understanding Summary`
  4. `Impact Analysis Summary`
  5. `Official Docs Check Summary`
  6. full `Skill Routing Decision`
  7. full `Rule-Loading Manifest`
  8. full `CodeGraph Project Understanding Report`
  9. full `Impact Analysis`
  10. full `Task Contract`

### 2. High-Risk Without Anomaly

- Goal: verify high-risk work expands only the risky slice and does not auto-upgrade to full detail.
- Prompt:
  `Use $devguard at <DEVGUARD_PATH> to route a hotfix for installer recovery replay gating. Treat rollback, recoverability, release validation, and focused failing tests as first-class concerns, but keep outward output compact unless full detail is explicitly required.`
- Expected outward shape:
  1. `Execution Summary`
  2. `Risk Note`
  3. `Task Contract Summary`
- Allowed extras:
  1. only risk-related focused-expansion blocks when the risky slice cannot be explained by `Risk Note` alone
- Must not appear:
  1. `Exception Note`
  2. `Project Understanding Summary`, `Impact Analysis Summary`, or `Official Docs Check Summary` as unrelated peer blocks without a real focused-expansion trigger
  3. full `Skill Routing Decision`
  4. full `Rule-Loading Manifest`
  5. unrelated healthy-surface detail
  6. full `CodeGraph Project Understanding Report`, full `Impact Analysis`, or full `Task Contract` without an explicit detailed-mode trigger

### 3. Anomaly Blocking With Missing Rule Or Path

- Goal: verify anomaly handling blocks early and expands only the missing or broken slice.
- Setup:
  1. use a fixture, temp copy, or project state where the task will naturally hit a missing required rule, wrong project rule, or non-existent rule path
- Prompt:
  `Use $devguard at <DEVGUARD_PATH> to route this desktop WPF scrollbar bugfix. Keep the outward output compact, but stop if required rules, playbooks, or rule paths are missing.`
- Expected outward shape:
  1. `Execution Summary`
  2. `Exception Note`
  3. `Task Contract Summary` only when a valid Task Contract can still be formed; otherwise remain blocked before Task Contract creation
- Allowed extras:
  1. only the focused exception or routing expansion needed to explain the blocker
- Must not appear:
  1. invented rule paths
  2. invented project-rule success
  3. full `Skill Routing Decision`
  4. full `Rule-Loading Manifest` unless the test explicitly requests detailed or audit output
  5. a fabricated `Task Contract Summary` when required rules are still missing and execution is blocked before contract freeze

### 4. Platform Or SDK Constraint Path

- Goal: verify platform-sensitive work triggers official docs check before impact analysis without breaking the default minimal outward packet.
- Prompt:
  `Use $devguard at <DEVGUARD_PATH> to route this WPF control-template fix. Confirm official WPF control-template, ResourceDictionary, Dispatcher, and DPI guidance before impact analysis, keep outward output compact, and stop if the implementation would violate official constraints.`
- Expected outward shape:
  1. `Execution Summary`
  2. `Task Contract Summary`
- Allowed extras:
  1. `Risk Note`
  2. `Official Docs Check Summary`
  3. `Official Docs Focused Expansion`
- Must not appear:
  1. full `Official Docs Check Report` unless detailed mode was explicitly requested
  2. coding approval without official-docs confirmation when the task is clearly platform-sensitive

## Recommended Scenarios

For every scenario above, inspect the final outward transcript as an ordered block packet. Treat any extra peer block outside the allowed shape as a regression, even if the added text is individually correct.

Cover at least:

1. the scenarios in `Regression Example Set`
2. `Platform Or SDK Constraint Path`
3. a UI change
4. a bug fix with incomplete evidence
5. a compatibility refactor
6. an AI tool-calling workflow
7. a review-only request (`Review Summary` or findings-first compact output; not the 19-section `Review Report` unless detailed mode)
8. a structural-tool repair-before-fallback case where CodeGraph is missing, uninitialized, or host-disconnected
9. a stale-index case where `codegraph_status` is not healthy until refresh or rebuild completes
10. a completed implementation task (`Completion Summary` only; not `Development Completion Report` unless detailed mode)
