# Shared Guardrails

Use this reference for the non-negotiable execution floor.

## Evidence Rules

Always separate:

1. Files actually read
2. Commands actually run
3. Results actually observed
4. Static inference
5. Unverified items

Never present inference as verification.

## Minimum Change Constraint

**Default to the simplest change that correctly solves the approved slice — nothing more.**

This is the unified edit-scope floor for feature work, bug fixes, refactors, UI bindings, and migrations. It applies to code, tests, configs, and docs touched during execution.

### Principles

1. **Contract-bound scope** — edit only surfaces allowed by the frozen Task Contract `Scope`. Treat everything else as out of scope until reroute.
2. **Simplest correct diff** — prefer the smallest code, test, and doc change that satisfies the failing check or acceptance criterion.
3. **Evidence-bound expansion** — widen scope only when evidence or an unresolved blocker forces it; reroute and amend the Task Contract before editing new surfaces.
4. **No drive-by edits** — do not refactor, reformat, rename, or "clean up while here" outside the approved slice.
5. **No silent scope creep** — do not add dependencies, APIs, abstractions, or behavior not required by the current slice.

### Required Behavior By Phase

| Phase | Minimum-change rule |
|---|---|
| Task Contract | `Scope` names allowed surfaces and forbidden/out-of-scope surfaces in one line |
| Red | smallest failing check or reproduction that proves the target problem |
| Green | smallest implementation that makes the failing check pass |
| Bug repair | smallest fix relative to proven root cause; diff limited to Contract scope |
| Refactor | behavior-preserving; external behavior changes require disclosure and reroute |
| Completion | diff review confirms only Contract-allowed files/behaviors changed |

### Forbidden Without Reroute

- editing unrelated files or modules
- widening behavior beyond Task Contract acceptance
- introducing new dependencies or public surfaces "for later"
- mixing bug fix, refactor, and feature work in one unreviewed slice
- weakening, deleting, or skipping tests to shrink the diff

### When Scope Must Expand

Stop and reroute when:

1. evidence shows the root cause or required fix lies outside current `Scope`
2. a contract, data, permission, or compatibility surface appears that the Contract did not cover
3. the user changes the requested outcome

Then amend or rebuild the Task Contract before further edits.

### Verification

Before calling work done, confirm:

1. every changed file is inside Task Contract `Scope`
2. the diff is no larger than the proven problem requires
3. regression checks still pass
4. remaining scope pressure is disclosed, not smuggled in

Lane-specific detail still lives in execution cores — for example [bug-fix-core.md](bug-fix-core.md) for evidence-first repair — but they must not relax this floor.

## TDD Floor

Default to `Red -> Green -> Refactor` for code changes, bug fixes, UI feature bindings, and refactors.

- `Red`: write the failing test or the smallest failing reproduction first.
- `Green`: implement the smallest change that makes the failing check pass.
- `Refactor`: improve structure only after the checks pass.

If no failing test or reproduction exists, do not claim TDD compliance.

For user-visible UI, dialog, page, settings, or interaction-flow work, at least one failing check or acceptance check must exercise a real user operation path such as click, type, select, open, close, scroll, drag, keyboard navigation, or equivalent end-user interaction. Internal function, method, interface, or ideal-path-only checks are not enough on their own.

## Blocking Conditions

Blocking is layered. Resolve P0 before execution continues. P1 must be loaded, verified, or explicitly deferred with rationale before calling work done. P2 does not block by itself unless paired with a P0 or P1 violation.

### P0 Hard Blocks

Mark the task `BLOCKED` and emit `Exception Note` if any of these is true:

1. Execution starts without rule-loading output.
2. A required pre-execution gate is skipped: project understanding, official docs check, or impact analysis when the Gate Matrix requires it.
3. Coding, repair, or refactor work starts without the required Task Contract.
4. Tests or checks are reported as passing without actually running them, or results are otherwise fabricated.
5. A fix, root cause, or verification claim is made without the required evidence chain.
6. TDD is claimed without a failing test or reproduction.
7. Files, APIs, components, permissions, or test results are invented.
8. The same issue failed twice and the next attempt adds no new evidence chain.

Bug-fix P0 additions (same blocking severity):

9. Repair code is written or applied before a failing test or reproduction exists — **no failing check = no bug claim and no repair**.
10. A bug is claimed fixed without red-before / green-after evidence for the repro check and regression coverage.
11. Tests are deleted, skipped, or weakened to hide the problem or force green.

### P1 Domain Gates

Mark the task `BLOCKED` until resolved, or `ALLOW_WITH_WARNINGS` only when the gap is explicitly disclosed and execution cannot proceed safely otherwise:

1. A clearly needed rule type was not loaded and no reason was given.
2. A Task Contract is generated before required project understanding, required official docs check, or impact analysis, or it ignores unresolved structural or impact risk.
3. A user-visible feature is not bound to real functionality.
4. Mock or placeholder behavior is presented as real functionality.
5. A new entry point bypasses permission, validation, logging, idempotency, or audit requirements.
6. A contract changed without contract updates.
7. Data structure changes lack migration, rollback, or compatibility notes.
8. Sensitive operations rely only on front-end permissions.
9. Secrets or credentials are written into code or logs.
10. Refactoring changes external behavior without disclosure.
11. High-risk migration has no rollback plan.
12. Privacy-sensitive data is collected or transmitted without need.
13. Release risk is uncontrolled.
14. AI or agent loops lack token, cost, or iteration caps.
15. Long-running work has no progress, timeout, cancel, or recovery path.
16. A user-visible UI or interaction-flow change is claimed verified using only internal function, method, interface, or ideal-path checks, with no real user operation path evidence.
17. A project-specific hard block is violated.
18. Code changes touch files, modules, dependencies, or behaviors outside the frozen Task Contract `Scope` without reroute — **no drive-by edits, no scope creep**.

### P2 Warnings

Mark the task `ALLOW_WITH_WARNINGS` and emit `Risk Note` when these are true and no P0 or P1 violation exists:

1. Rule-loading budget is exceeded without a focused expansion rationale.
2. Mock quality is weak but clearly labeled and not presented as production behavior.
3. Clear performance risk is deferred with no analysis.
4. Large lists or hot APIs lack pagination or limiting controls.
5. Core flows lack enough logging to diagnose failure.

## Failure Escalation

If the same issue fails twice without a new evidence chain:

1. Stop trial-and-error repair.
2. Enter failure retrospective mode.
3. Require a new root-cause hypothesis and a new minimal validation plan before a third attempt.

## Review Alignment

Development requirements and review requirements must match. If development required a rule or extension, review must verify it was actually respected.
