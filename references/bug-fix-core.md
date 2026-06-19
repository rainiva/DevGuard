# Bug-Fix Core

## Metadata

- Layer: execution core
- Load level: metadata, summary, full
- Use when: concrete defects with observable wrong behavior; diagnosis-only before impact analysis, minimal repair after Task Contract freeze and Red check.
- Risk tags: `repair_failure`, `compatibility`, `security`, `official_docs_required`, `codegraph_required`, `ux_flow`

## Summary

**没有失败测试 = 没有 bug。宣称修复前，先证明它曾经坏过。**

Diagnose with evidence, reproduce, establish Red, state root cause at file/line/condition granularity, apply the smallest fix, verify regression coverage, and keep the diff inside Task Contract scope per the [Minimum Change Constraint](shared-guardrails.md#minimum-change-constraint). Do not write repair code before a failing check or reproduction exists.

## Full Rule

### Why This Gate Is Hard

The most common bug-fix hallucination is: "this line looks wrong, change it and it should work." Without reproduction, without a failing check, and without proof the failure mode was touched, a claimed fix may miss the real root cause entirely.

Bug-fix work therefore follows an evidence-first gate. **No evidence, no repair code.**

### Evidence Gate — Six Required Items

All six must be satisfied before calling a bug fix done. Missing any item blocks repair start or completion.

| # | Requirement | What it means | Owner |
|---|---|---|---|
| 1 | Reproducible input | Clear trigger: user steps, input data, environment or state | Human provides; AI fills boundary cases |
| 2 | Failing check (Red) | Before repair, a test or reproduction must fail and prove the bug is real | Human writes or approves; AI may draft for review |
| 3 | Minimal repro scope | Strip unrelated code; keep only the smallest unit that triggers the bug | AI proposes; human confirms |
| 4 | Root-cause statement | One precise sentence: when condition X holds, method Y at line N fails because Z — not vague labels like "missing null check" | AI states; human reviews |
| 5 | All green after fix | Repro check plus existing regression checks pass after repair | Automated run |
| 6 | No side-effect proof | Diff shows only Task Contract–allowed files; no drive-by refactors, new deps, or test weakening | Human reviews diff |

### Red Line

- **No failing test or reproduction = no bug claim and no repair code.**
- **Before claiming fixed, prove it was broken first.**

The Gate Matrix repro substitute for `S1 / FAST` does **not** apply to `bugfix` tasks. Bug fixes always require Red before `bug-fix(minimal-repair)`.

### Required Flow

When this module appears before impact analysis or Task Contract freeze, use only the diagnosis portion of this flow. Do not apply a repair until impact analysis, Task Contract freeze, and the required Red check exist.

1. Diagnose the symptom precisely.
2. Capture reproducible input (steps, data, environment).
3. Gather the evidence chain.
4. Narrow to minimal repro scope; confirm with human when scope is non-obvious.
5. List plausible root-cause hypotheses.
6. Check counter-evidence to avoid premature certainty.
7. Create or confirm a failing test or minimal reproduction — **must be red before repair**.
8. State root cause at file/line/condition granularity.
9. Apply the smallest fix.
10. Re-run repro check and regression suite — all green.
11. Verify diff scope against Task Contract — no unrelated edits.

### Repair Output Shape

When emitting repair output (default T1b or detailed T3), use this order:

1. **Root-cause analysis** — condition, location, mechanism
2. **Repair** — minimal change only
3. **Verification** — red-before / green-after, regression, diff scope

In default outward mode, compress this into `Completion Summary` with at least: repro evidence, root-cause one-liner, verification, diff scope.

### Guardrails

- Do not write repair code without a failing test or reproduction.
- Do not claim a fix before reproduction exists.
- Do not jump straight to code changes because static reading "looks wrong."
- Do not weaken, delete, or skip tests to make checks pass.
- Do not refactor unrelated code, add new dependencies, or expand scope while fixing.
- If the entry point, call chain, or similar implementation is unclear, require project understanding before code changes.
- If the bug touches platform behavior, control behavior, system APIs, SDK calls, host integration, lifecycle, threading, or control templates, require official docs check before claiming the root cause.
- Do not widen the scope unless the evidence forces it.
- After two failed repairs, stop and reroute into failure analysis.

### Required Output

Capture:

1. symptom
2. reproducible input
3. reproduction or failing check (red state recorded)
4. minimal repro scope
5. evidence chain
6. root-cause statement (file / line / condition / mechanism)
7. counter-evidence check
8. official-spec counter-check when platform or framework behavior may be involved
9. minimal fix
10. regression verification (all green)
11. diff scope / no side-effect proof

### Prompt Template

Use this shape when invoking DevGuard for bug fix. Replace placeholders; keep the evidence gate explicit.

```text
Use $devguard to handle this bug fix. Role: bug-fix engineer — minimal change, evidence first.

Task: {one-line bug description}

Repro conditions:
{inputs, user steps, environment}

Failing check (must be red before repair):
{test name, command, or minimal repro steps + expected failure}

Constraints:
- Hard gate: no repair code without a failing test or reproduction
- Before repair: state root cause (file, line, condition, why)
- After repair: all checks green; diff only touches Task Contract scope
- Forbidden: unrelated refactors, new dependencies, weakening tests to pass
- Output order: 1. root-cause analysis → 2. repair → 3. verification
- Keep outward output to Execution Summary plus Task Contract Summary unless risk requires expansion
```

Canonical copy also lives in [example-prompts.md](example-prompts.md).
