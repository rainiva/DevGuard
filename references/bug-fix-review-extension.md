# Bug-Fix Review Extension

Use this when reviewing a bug fix.

## Review Checks

Verify:

1. the original bug was actually reproduced or captured with a meaningful failing check
2. the proposed root cause is backed by evidence, not guesswork
3. the fix is minimal relative to the proven cause
4. regression checks cover the reported failure mode
5. surrounding behavior did not silently change

## Findings Focus

Prefer findings around:

- missing reproduction evidence
- weak root-cause claims
- over-broad repairs
- missing regression coverage
- repeated trial-and-error behavior
