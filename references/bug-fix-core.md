# Bug-Fix Core

Use this for concrete defects with observable wrong behavior.

## Required Flow

When this module appears before impact analysis or Task Contract freeze, use only the diagnosis portion of this flow. Do not apply a repair until impact analysis, Task Contract freeze, and the required Red check exist.

1. Diagnose the symptom precisely.
2. Reproduce the issue.
3. Gather the evidence chain.
4. List plausible root-cause hypotheses.
5. Check counter-evidence to avoid premature certainty.
6. Create a failing test or minimal reproduction.
7. Prove the root cause as narrowly as possible.
8. Apply the smallest fix.
9. Verify regression coverage.

## Guardrails

- Do not claim a fix before reproduction exists.
- Do not jump straight to code changes without evidence.
- If the entry point, call chain, or similar implementation is unclear, require project understanding before code changes.
- If the bug touches platform behavior, control behavior, system APIs, SDK calls, host integration, lifecycle, threading, or control templates, require official docs check before claiming the root cause.
- Do not widen the scope unless the evidence forces it.
- After two failed repairs, stop and reroute into failure analysis.

## Required Output

Capture:

1. symptom
2. reproduction
3. evidence chain
4. root-cause hypothesis
5. counter-evidence check
6. official-spec counter-check when platform or framework behavior may be involved
7. minimal fix
8. regression verification
