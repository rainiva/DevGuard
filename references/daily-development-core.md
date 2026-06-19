# Daily Development Core

## Metadata

- Layer: execution core
- Load level: metadata, summary, full
- Use when: ordinary feature work or scoped behavior changes after routing, required project understanding, required official docs check, and impact analysis are done.
- Risk tags: `api_contract`, `ux_flow`, `data_consistency`, `performance`, `official_docs_required`

## Summary

Freeze the Task Contract, establish Red, implement the minimum viable change inside scope, rerun checks, sync docs, and prepare for review. Obey the unified [Minimum Change Constraint](shared-guardrails.md#minimum-change-constraint); reroute before expanding scope.

## Full Rule

### Execution Flow

1. Confirm the requested outcome and boundaries.
2. Run required project understanding.
3. Run required official docs check.
4. Run impact analysis.
5. Freeze the required Task Contract.
6. Establish the Red check.
7. Implement the minimum viable change.
8. Re-run the relevant checks.
9. Update docs, configs, or references that must stay aligned.
10. Prepare the work for review.

### Engineering Floor

Always pay attention to:

1. Single clear entry point for the new behavior
2. Consistent interface and contract handling
3. Real UI-to-function binding for user-visible flows
4. [Minimum Change Constraint](shared-guardrails.md#minimum-change-constraint) — controlled edit scope and Task Contract discipline
5. Test synchronization with behavior
6. Documentation synchronization
7. Official platform or framework constraints when they apply
8. Early consideration of performance and safety

### Do Not Normalize These Mistakes

Violations of the Minimum Change Constraint — see [shared-guardrails.md](shared-guardrails.md#minimum-change-constraint) for the canonical list:

- editing multiple unrelated areas "while here"
- widening scope beyond the Task Contract without rerouting
- adding placeholders that masquerade as real behavior
- leaving new states untested
- changing output shape without updating the contract surface
- claiming completion before rerunning the checks

### Completion Frame

Before calling the change done, be able to explain:

1. What changed
2. Why that scope stayed inside the Task Contract
3. What was verified
4. What remains unverified
