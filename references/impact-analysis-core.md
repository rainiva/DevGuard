# Impact Analysis Core

Use this before any non-trivial implementation, refactor, migration, or performance-sensitive change.

## Goal

Understand what the change touches before editing code.

Impact analysis is the change-impact judgment pass. It may fan out across several plausible impact surfaces and unresolved risks.
It is not project understanding, it is not official docs check, and it is not the Task Contract. Use project understanding to establish structural facts first, then use official docs check to establish platform or framework constraints, then use impact analysis to reason about change impact, then use the Task Contract to freeze the approved execution slice.

## Output Depth

Choose the output depth during routing and upgrade it when new facts raise risk. Keep the internal rigor appropriate to the task, but default the outward report to the smallest shape that still preserves safe execution.

### Summary

Use `Impact Analysis Summary` from `references/report-templates.md`.

Default to this for ordinary `FAST` and `STANDARD` work unless detailed traceability is required.

Capture only:

1. Goal
2. Likely touched surfaces
3. Primary risks
4. Required checks
5. Unverified items

### Focused Expansion

Use `Impact Analysis Summary` plus `Impact Analysis Focused Expansion` from `references/report-templates.md`.

Default to this for high-risk, blocker, anomaly, or reroute cases when only the risky surfaces need more detail.

### Full

Use full `Impact Analysis` from `references/report-templates.md`.

Use this only when one of these is true:

1. the user explicitly asks for detailed, verbose, debug, or audit output
2. the task is a formal evidence-capture or forward-testing pass that explicitly requires the canonical full template

High-risk or anomaly status alone does not force the full template if focused expansion is enough.

### Strict Additions

Use full `Impact Analysis` plus `Strict Impact Analysis Additions` from `references/report-templates.md`.
Add compatibility, dependency, observability, rollback, blocker, and confirmation detail needed for the higher-risk slice. Use this only when full output is already required and the task is `STRICT` or touches shared high-risk surfaces.

## Required Questions

Answer these from current evidence:

1. What entry points will change?
2. What interfaces or contracts may change?
3. What data shape, persistence, or migration surfaces are involved?
4. What state transitions or workflow steps may be affected?
5. What permissions, auth, or audit boundaries are involved?
6. What tests must fail first and then pass?
7. What docs, configs, or release notes need sync?
8. What performance, observability, rollback, or compatibility risks exist?
9. Which impact surfaces are likely out of scope for this slice unless rerouting proves otherwise?

## STANDARD Output

Produce:

1. Impacted files or modules
2. Impacted entry points
3. Contract and data risks
4. State and permission risks
5. Required tests
6. Required documentation updates
7. Candidate non-goals or surfaces to keep out of scope
8. Items still unverified

## Guardrails

- Do not begin a broad code edit before this pass exists.
- Do not begin impact analysis when required project understanding has not happened yet.
- Do not begin impact analysis when required official docs check has not happened yet.
- Do not use the Task Contract as a substitute for impact analysis; impact analysis may stay uncertain while the Task Contract must converge.
- Keep the first pass concise; in summary mode, group touched surfaces instead of dumping long file-by-file lists unless a specific file is itself the risk.
- If the task appears small but crosses a contract or data boundary, upgrade the rigor.
- If the task is purely consultative, keep this lightweight and avoid fake implementation planning.
- Except for headings, field labels, and predefined keywords, write the analysis prose in Chinese.
