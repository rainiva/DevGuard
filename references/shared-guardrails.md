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

## TDD Floor

Default to `Red -> Green -> Refactor` for code changes, bug fixes, UI feature bindings, and refactors.

- `Red`: write the failing test or the smallest failing reproduction first.
- `Green`: implement the smallest change that makes the failing check pass.
- `Refactor`: improve structure only after the checks pass.

If no failing test or reproduction exists, do not claim TDD compliance.

## Blocking Conditions

Mark the task blocked if any of these is true:

1. Execution starts without rule-loading output.
2. A code-modifying task that required project understanding begins impact analysis or coding without it.
3. A platform, framework, SDK, host, control-template, system-API, or platform-design-sensitive task begins impact analysis or coding without required official docs check.
4. Coding, repair, or refactor work starts without the required Task Contract.
5. A clearly needed rule type was not loaded and no reason was given.
6. Large code changes begin without impact analysis.
7. A Task Contract is generated before required project understanding, required official docs check, or impact analysis, or it ignores unresolved structural or impact risk.
8. TDD is claimed without a failing test or reproduction.
9. Tests were not run but are reported as passing.
10. A user-visible feature is not bound to real functionality.
11. Mock or placeholder behavior is presented as real functionality.
12. A new entry point bypasses permission, validation, logging, idempotency, or audit requirements.
13. A contract changed without contract updates.
14. Data structure changes lack migration, rollback, or compatibility notes.
15. Sensitive operations rely only on front-end permissions.
16. Secrets or credentials are written into code or logs.
17. A bug is claimed fixed without reproduction evidence.
18. A root cause is claimed without evidence.
19. Tests are deleted, skipped, or weakened to hide the problem.
20. Refactoring changes external behavior without disclosure.
21. High-risk migration has no rollback plan.
22. Files, APIs, components, or test results are invented.
23. Privacy-sensitive data is collected or transmitted without need.
24. Release risk is uncontrolled.
25. Clear performance risk is deferred with no analysis.
26. Large lists or hot APIs lack pagination or limiting controls.
27. AI or agent loops lack token, cost, or iteration caps.
28. Long-running work has no progress, timeout, cancel, or recovery path.
29. Core flows lack enough logging to diagnose failure.
30. The same issue failed twice and the next attempt adds no new evidence.
31. A project-specific hard block is violated.

## Failure Escalation

If the same issue fails twice without a new evidence chain:

1. Stop trial-and-error repair.
2. Enter failure retrospective mode.
3. Require a new root-cause hypothesis and a new minimal validation plan before a third attempt.

## Review Alignment

Development requirements and review requirements must match. If development required a rule or extension, review must verify it was actually respected.
