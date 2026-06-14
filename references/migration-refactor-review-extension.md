# Migration Refactor Review Extension

Use this when reviewing migrations or refactors.

## Review Checks

Verify:

1. current behavior was frozen before reshaping internals
2. the refactor claims do not mask external behavior changes
3. compatibility handling is explicit where old and new paths overlap
4. migration, packaging, or config surfaces were not skipped
5. rollback or fallback thinking exists for risky moves

## Findings Focus

Prefer findings around:

- missing baseline
- hidden behavior drift
- unsafe bundling of too many structural changes
- compatibility gaps
- no rollback story for risky migrations
