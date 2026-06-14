# Forward Testing

Use this when validating DevGuard itself with a fresh agent or a fresh thread.

## Goal

Test whether DevGuard can generalize from its own instructions instead of succeeding only because the evaluator leaked the intended answer.

## Core Rules

1. Use a fresh thread or fresh agent when possible.
2. Pass the skill path and a realistic user request.
3. Do not tell the tester what rule should load or what the correct answer is.
4. Review the tester's emitted routing report, rule-loading disclosure, project-understanding output, official-docs output when applicable, Task Contract, and decision quality.
5. Clean up temporary artifacts if the forward test writes anything.

## Good Prompt Shape

Use prompts like:

- `Use $devguard at <DEVGUARD_PATH> to route this medium-risk feature task, run project understanding before impact analysis, keep the outward output to Execution Summary plus Task Contract Summary, and freeze the Task Contract before coding.`
- `Use $devguard at <DEVGUARD_PATH> to route this medium-risk feature task, keep the outward routing, project-understanding, impact-analysis, and Task Contract output compact by default, and if risk appears expand only the affected parts unless I explicitly ask for full detail.`
- `Use $devguard at <DEVGUARD_PATH> to route this platform-sensitive task, confirm official platform or framework constraints before impact analysis, and block if the implementation would rely on unofficial assumptions.`
- `Use $devguard at <DEVGUARD_PATH> to handle this bug report. Reproduce first, load only the needed rules, and stop if the evidence chain is weak.`
- `Use $devguard at <DEVGUARD_PATH> to review this UI change and verify whether the implementation-side rules were mirrored into review.`

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

## Failure Signals

Treat these as forward-test failures:

- loads nearly everything by default
- skips the rule-loading disclosure
- skips required project understanding and jumps to impact analysis or coding
- skips required official docs check and still edits platform-sensitive code
- emits a full manifest table for a normal low-risk task without being asked
- emits a full routing decision, full project-understanding report, full Impact Analysis, or full Task Contract for a normal task without a real expansion trigger
- emits the full detail for unrelated healthy surfaces when only one risky or anomalous slice needed expansion
- compresses a required full manifest into prose or omits required schema columns such as `Path`
- starts coding without the required Task Contract
- jumps into implementation before routing
- claims evidence that was never gathered
- ignores review mirroring
- misses obvious high-risk domain routing

## Regression Example Set

Use these four regression scenarios after any change to DevGuard disclosure policy, routing output, Task Contract visibility rules, or official-docs disclosure behavior.

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
  3. full `Skill Routing Decision`
  4. full `Rule-Loading Manifest`
  5. full `CodeGraph Project Understanding Report`
  6. full `Impact Analysis`
  7. full `Task Contract`

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
  2. full `Skill Routing Decision`
  3. full `Rule-Loading Manifest`
  4. unrelated healthy-surface detail
  5. full `CodeGraph Project Understanding Report`, full `Impact Analysis`, or full `Task Contract` without an explicit detailed-mode trigger

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

Cover at least:

1. the scenarios in `Regression Example Set`
2. `Platform Or SDK Constraint Path`
3. a UI change
4. a bug fix with incomplete evidence
5. a compatibility refactor
6. an AI tool-calling workflow
7. a review-only request
