# Rule Loading

Use this reference to decide what to load now, what to defer, and how to stay small.

## Layer Model

Load in this order:

1. Meta rules
2. Pre-execution gates
3. Execution core
4. Extensions
5. Project rules
6. Playbooks
7. Review extensions

## Loading Principles

- Load in batches.
- Load on demand.
- Load by stage.
- Prefer summaries before full detail.
- Use [rule-disclosure-index.md](rule-disclosure-index.md) for metadata-level routing, summary-level analysis, and full-file execution.
- Add rules dynamically as risk grows or the stage changes.
- Review the loaded set again before review or release.

## What Each Layer Should Contain

- Meta rules: routing principle, disclosure policy, rule-loading output requirement, dynamic reroute requirement, and other global decision policy.
- Pre-execution gates: project understanding, official-docs check, impact analysis, TDD setup, Task Contract freeze, and blocking-floor checks required before execution.
- Execution core: stable process for the selected implementation, repair, release, review, or refactor lane.
- Extensions: stack-specific or scenario-specific requirements.
- Project rules: project facts, business boundaries, UI rules, prohibited actions, acceptance constraints.
- Playbooks: focused troubleshooting or handling instructions for a concrete issue type.
- Review extensions: validation expectations that mirror the loaded development extensions.

## Loading Budgets

Use these as a pressure check, not as a hard mechanical cap.

Meta rules and mandatory pre-execution gates do not consume the execution-core budget. Count them separately so routing safety does not appear to compete with implementation-lane rules.

### FAST

- Core: `1-2`
- Extensions: `0-2`
- Project rules: `0-2`
- Playbooks: `0-1`

### STANDARD

- Core: `1-4`
- Extensions: `0-4`
- Project rules: `0-4`
- Playbooks: `0-3`

### STRICT

- Load as needed, but explain why every added rule is required now.

If you exceed the usual budget, explain:

1. Why the extra load is necessary now.
2. Which rules remain deferred.
3. What risk would exist without the additional load.

If the extra load is justified, mark the task `ALLOW_WITH_WARNINGS` and use focused expansion for the budget overrun. If the extra load cannot be justified, mark the task `BLOCKED` until the rule set is narrowed or the missing rationale is supplied.

## Deferred Loading

Do not load a rule yet if:

- The current stage does not need it.
- The task has not hit that platform, subsystem, or project area.
- A summary is enough for routing and only full detail is needed during execution.
- The task is still exploratory and not yet moving into implementation.

## Forbidden Loading Patterns

- Do not load the entire rule system into every task.
- Do not load all playbooks "just in case."
- Do not load large project packs when only one project subdomain is relevant.
- Do not load broad official documentation packs when only one API, control, SDK, host, or design surface is relevant.
- Do not skip rule-loading output because the task feels small.

## Rule-Loading Disclosure Requirements

Before execution, always emit a rule-loading disclosure. The disclosure format depends on the output mode below.

Minimum content in every disclosure:

1. What was loaded
2. Whether execution may proceed

In default mode, this disclosure should normally live inside `Execution Summary` instead of a separate rule-loading block.

Full manifest content (deferred unless detailed mode explicitly requires the canonical full manifest):

3. Why each rule was loaded
4. At what detail level it was loaded
5. What was deferred
6. What appears missing

## Rule-Loading Output Modes

To reduce token cost, use three disclosure modes. Default to the smallest mode that still prevents missed loads.

### 1. Default Mode: Minimal Summary

For normal tasks, output only the minimal summary from `references/report-templates.md`.

The canonical default outward packet is `Execution Summary`, with `Task Contract Summary` appended once a valid contract exists. Use standalone `Rule-Loading Summary` only when rule-loading-specific output is explicitly requested.

Render the default packet as standalone record blocks. Do not embed the summary fields inside ordinary conversation, and do not place explanatory prose between the heading and the bullet fields.

Include:

1. Task
2. Execution mode
3. Loaded rules as one compact `Rules` line
4. Status: `ALLOW`, `ALLOW_WITH_WARNINGS`, or `BLOCKED`
5. Next step

Keep `Task Contract Summary` visible separately in default mode once execution is being prepared.

Do not output the full manifest table in default mode.

### 2. Focused Expansion Mode

Use the summary as the base, then expand only the risky or anomalous rule-loading parts.

Use this when one of these is true and the user did not explicitly ask for a full manifest:

1. complexity is `S3` or `S4`
2. execution mode is `STRICT`
3. the task involves high-risk operations such as release, migration, auth, payments, or data migration
4. a required rule appears missing
5. the wrong project rules were loaded
6. a rule path does not exist or cannot be confirmed
7. loaded rules do not match the task type
8. a high-risk task lacks a required specialized rule
9. the rule-loading budget is exceeded
10. you cannot explain why a rule was loaded or deferred

In focused-expansion mode:

1. expand only the affected rules, missing rules, blockers, or deferrals
2. do not dump the full loaded-rules table when unaffected rows add no decision value
3. keep unrelated healthy rule rows inside the summary, not the expansion block

### 3. Detailed Mode: Full Manifest

Output the full rule-loading manifest only when one of these is true:

1. the user explicitly asks for a full manifest, detailed output, verbose mode, debug mode, or audit mode
2. the task is being used to forward-test DevGuard itself
3. a formal evidence-capture task explicitly requires the canonical full manifest schema

Do not use the full manifest merely because the task is high-risk or anomalous if focused expansion is enough.

### Output Principle

```text
Normal tasks: Execution Summary + Task Contract Summary
High-risk tasks: Execution Summary + Risk Note + Task Contract Summary
Rule anomalies: Execution Summary + Exception Note + Task Contract Summary when available
Debug, verbose, audit, or full-manifest tasks: canonical full manifest
```

Stage summaries are internal records by default. In normal summary mode, do not emit `Project Understanding Summary`, `Impact Analysis Summary`, or `Official Docs Check Summary` as peer outward blocks. Surface them only when they contain a blocker, anomaly, implementation-changing official constraint, or risk that cannot fit in `Risk Note` or `Exception Note`.

## Relationship To Task Contract

Rule-loading output answers "which rules are active now and may we proceed."
Project understanding answers "what does the project structure currently look like."
Official docs check answers "what do the platform, framework, SDK, host, or design rules officially require here."
Impact analysis answers "what might this task affect."
Task Contract answers "what is frozen for this execution slice."

Normal tasks should see only the compact outward packet by default. Keep project-understanding, official-docs-check, and impact-analysis records internal unless traceability, explicit user mode, blocker, anomaly, or implementation-changing risk actually requires a visible focused note. Keep `Task Contract Summary` visible by default once execution is being prepared.

Do not skip from routing straight into implementation. The normal execution sequence is:

1. route the task
2. emit rule-loading output
3. run required project understanding
4. run required official docs check
5. run impact analysis
6. freeze the required Task Contract
7. start Red

## Manifest Schema Discipline

When detailed mode is active, the manifest schema is part of the safety contract, not cosmetic formatting.

- Use the canonical manifest shape from `references/report-templates.md`.
- Keep the loaded-rules table columns exactly as `Type | Rule | Path | Why loaded | Detail level`.
- Do not rename `Path` to prose, merge it into `Rule`, or omit it because a path is obvious.
- If a path is not yet discovered, write `unverified` or `not yet discovered` in the `Path` cell.
- Keep deferred rules and possibly missing rules in tables, not bullet lists.
- Use `ALLOW`, `ALLOW_WITH_WARNINGS`, or `BLOCKED` for the execution decision.
- If the user asks to stop before implementation, the initial routing disclosure should normally be `BLOCKED` or `ALLOW_WITH_WARNINGS` for execution, with a clear reason that implementation is intentionally paused.

## Dynamic Additions

Add more rules when:

- The risk profile increases
- The task enters review or release
- A concrete bug category becomes clear
- Project-specific facts become relevant
- Repeated failures suggest the current rule set is insufficient
