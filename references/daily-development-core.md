# Daily Development Core

Use this for ordinary feature work or scoped behavior changes after routing, required project understanding, required official docs check, and impact analysis are done.

## Execution Flow

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

## Engineering Floor

Always pay attention to:

1. Single clear entry point for the new behavior
2. Consistent interface and contract handling
3. Real UI-to-function binding for user-visible flows
4. Controlled edit scope
5. Task Contract scope discipline
6. Test synchronization with behavior
7. Documentation synchronization
8. Official platform or framework constraints when they apply
9. Early consideration of performance and safety

## Do Not Normalize These Mistakes

- editing multiple unrelated areas "while here"
- widening scope beyond the Task Contract without rerouting
- adding placeholders that masquerade as real behavior
- leaving new states untested
- changing output shape without updating the contract surface
- claiming completion before rerunning the checks

## Completion Frame

Before calling the change done, be able to explain:

1. What changed
2. Why that scope stayed inside the Task Contract
3. What was verified
4. What remains unverified
