# Bug-Fix Review Extension

Use this when reviewing a bug fix.

## Review Checks

Verify the six-item Evidence Gate from [bug-fix-core.md](bug-fix-core.md):

1. reproducible input was captured
2. a failing check existed before repair (red-before recorded)
3. minimal repro scope was confirmed
4. root-cause statement names condition, location, and mechanism — not vague guesswork
5. repro plus regression checks are all green after repair
6. diff stays inside Task Contract scope with no unrelated refactors, new deps, or test weakening — per [Minimum Change Constraint](shared-guardrails.md#minimum-change-constraint)

Also verify:

7. the fix is minimal relative to the proven cause
8. surrounding behavior did not silently change
9. repair did not start before Task Contract freeze and Red check

## Findings Focus

Prefer findings around:

- missing reproduction evidence or missing red-before proof
- repair code present without a prior failing check
- weak or vague root-cause claims ("probably null", "looks wrong")
- over-broad repairs or drive-by refactors in the diff
- missing regression coverage
- tests weakened, deleted, or skipped to force green
- repeated trial-and-error behavior

## Red Line

**No failing test or reproduction = no accepted bug fix.**
