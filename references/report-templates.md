# Report Templates

Use these templates as compact output shapes. Fill only the sections relevant to the current stage.

## Output Tier Model

| Tier | Name | Default outward blocks | Trigger |
|---|---|---|---|
| T1-lite | lite | `Execution Summary` with embedded `Slice` | `LITE` execute |
| T1 | summary | `Execution Summary` + `Task Contract Summary` | default |
| T1b | completion | `Completion Summary` or `LITE Completion Summary` | task finished |
| T2 | focused-expansion | T1 blocks + `Risk Note` or `Exception Note` (+ optional focused slice) | high-risk or anomaly |
| T3 | detailed | full routing, manifest, IA, TC, completion/review reports | audit, verbose, forward-test evidence |

Rules:

- T1-lite, T1, and T2 are the only tiers allowed for normal pre-execution outward output.
- `LITE` preview (no code) uses `Execution Summary` only with no `Slice`.
- T1b replaces full completion/review reports for ordinary finished work.
- T3 templates below are canonical for audit mode; do not emit them in T1/T2 unless explicitly requested.

### T1-lite outward set

- `Execution Summary` with embedded `Slice` (Goal / Edit / Done)
- do **not** emit a separate `Task Contract Summary` block

### T1 outward set

- `Execution Summary`
- `Task Contract Summary` (4 fields)
- `Completion Summary` (after execution)

### T2 outward additions

- `Risk Note`
- `Exception Note`
- `Official Docs Check Summary` or focused expansion only when official constraints block or reshape the Task Contract

### Internal-only (do not emit as peer T1/T2 blocks)

- `Routing Summary`
- `Rule-Loading Summary`
- `Project Understanding Summary`
- `Impact Analysis Summary`
- `Official Docs Check Summary` when no blocker or contract-shaping constraint exists

### T3 detailed-only

- `Skill Routing Decision`
- `Rule-Loading Manifest`
- `CodeGraph Project Understanding Report`
- `Official Docs Check Report`
- `Impact Analysis`
- `Task Contract` (full)
- `Development Completion Report`
- `Bug-Fix Completion Report`
- `Review Report` (19-section full form)

## Output Language Contract

- Headings, field labels, literal status values, rule names, paths, code identifiers, and predefined keywords may remain in English.
- All explanatory prose, reasons, risks, non-goals, acceptance criteria, test notes, blocker explanations, and remediation text should be written in Chinese.

## Summary Output Discipline

Default pre-execution output should stay compact.

In summary mode:

- Default outward packet should normally be `Execution Summary` plus `Task Contract Summary`, except `LITE execute` uses `Execution Summary` with embedded `Slice` only.
- Keep each section short, usually within 4-8 lines.
- Prefer module groups or up to 3 key files over exhaustive file lists.
- Do not dump full call chains, full test matrices, or long acceptance checklists.
- Use focused-expansion or detailed templates only when routing explicitly requires expansion.
- Do not hide `Task Contract Summary` in default mode once execution is being prepared for `FAST` and above.
- For `LITE execute`, freeze `Slice` inside `Execution Summary` instead of emitting a separate `Task Contract Summary`.
- Do not let official-docs reporting break the default minimal outward packet unless risk, anomaly, or explicit detailed mode requires it.
- Hard default-output cap: summary mode may not emit `Project Understanding Summary`, `Impact Analysis Summary`, or `Official Docs Check Summary` as separate outward blocks by default.
- Treat those stage summaries as internal records unless they carry a blocker, anomaly, implementation-changing official constraint, or risk that cannot fit in `Risk Note` or `Exception Note`.
- If a stage record must surface, prefer `Risk Note` or `Exception Note`; otherwise emit at most one ultra-short stage summary and keep unrelated stage details internal.

## Record Block Discipline

Default summaries must render as standalone record blocks, not as inline prose inside a conversational paragraph.

- Start the record directly with `## Execution Summary` when emitting a pre-execution summary.
- Put each field on its own bullet line.
- Keep explanatory conversation outside the record block.
- Do not insert commentary between a record heading and its field lines.
- Separate adjacent record blocks with exactly one blank line.
- For high-risk or anomaly cases, use `Execution Summary`, then the focused `Risk Note` or `Exception Note`, then `Task Contract Summary` when a valid contract exists.

## Execution Summary

Use for normal tasks by default. This is the default outward summary that replaces separate routing and rule-loading dumps in the common case.

```md
## Execution Summary
- Task:
- Mode:
- Rules:
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED
- Structural tool:
- Next:
```

When structural fallback is active, set `Structural tool` to one compact line, for example:

`CodeGraph unavailable, fallback: limited read`

Other allowed fallback labels: `secondary structural tool`, `ALLOW_WITHOUT_CODEGRAPH`. Omit the line when CodeGraph or another structural tool is healthy and in use.

### LITE Execution Summary

Use for `LITE execute` instead of separate `Execution Summary` + `Task Contract Summary`.

```md
## Execution Summary
- Task:
- Mode: LITE
- Rules:
- Slice:
  - Goal:
  - Edit:
  - Done:
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED
- Next:
```

`Slice` is the frozen Micro Contract. Do not emit `## Task Contract Summary` as a peer block in T1-lite mode.

### LITE preview

When the user requests routing only, omit `Slice` and do not prepare for code changes:

```md
## Execution Summary
- Task:
- Mode: LITE
- Rules:
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED
- Next:
```

## Risk Note

Use for high-risk but non-anomalous tasks that need one short extra explanation block.

```md
## Risk Note
- Focus:
- Why it matters:
- Extra gate:
```

## Exception Note

Use for anomaly cases that need one short corrective block without dumping the full detailed templates.

```md
## Exception Note
- Reason:
- Missing / wrong:
- Required fix:
- Status: BLOCKED / ALLOW_WITH_WARNINGS
```

## Official Docs Check Summary

Use only when official platform, framework, SDK, host, or design constraints need a compact outward summary because they materially affect the Task Contract, create a blocker, or change the implementation path.

```md
## Official Docs Check Summary
- Tool:
- Platform / framework:
- SDK / API / host:
- Query target:
- Key official findings:
- Constraint on this task:
- Source mode:
- Context7 state:
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED
```

## Official Docs Focused Expansion

Use when only the risky official constraints need extra outward explanation.

```md
## Official Docs Focused Expansion
- Expanded area:
- Context7 / source scope:
- Repair / fallback path:
- Need original-doc verification:
- Key official basis:
- Implementation constraints:
- Test or compatibility note:
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED
```

## Focused Expansion Discipline

For high-risk or anomaly cases, keep the summary as the base and expand only the affected part.

- Do not paste the entire detailed template when only one or two surfaces are risky.
- Expand only the fields that explain the blocker, risk, missing rule, or extra guardrail.
- Leave healthy and unrelated surfaces inside the short summary.

## Routing Summary

Internal-only in T1/T2. Use only when routing-only output is explicitly requested before Task Contract creation.

```md
## Routing Summary
- Task type:
- Risk tags:
- Complexity:
- Execution mode:
- Skill chain:
- Project understanding:
- Impact Analysis:
- Task Contract:
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED
- Next step:
```

## Routing Focused Expansion

Use when routing needs to explain only the risky or anomalous part without dumping the full routing decision.

```md
## Routing Focused Expansion
- Trigger:
- Affected risk or anomaly:
- Affected lane:
- Extra gates or confirmations:
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED
```

## Skill Routing Decision

T3 detailed-only. Use only in detailed disclosure mode when full routing traceability is required.

```md
# Skill Routing Decision

## 1. Task Understanding
## 2. Task Profile
## 3. Task Type
## 4. Risk Tags
## 5. Complexity Level
## 6. Risk Score
## 7. Execution Mode
## 8. Project Understanding Requirement
## 9. Project Understanding Depth
## 10. Official Docs Requirement
## 11. Official Docs Depth
## 12. Rule-Loading Strategy
## 13. Impact Analysis Depth
## 14. Task Contract Depth
## 15. Skill Chain
## 16. Needed Extensions
## 17. Needed Playbooks
## 18. Needed Project Rules
## 19. Needed Review Extensions
## 20. Stage Gates
## 21. Dynamic Reroute Conditions
## 22. Human Confirmation Points
## 23. Next Step
```

## Rule-Loading Summary

Internal-only in T1/T2. Use only when rule-loading-specific output is explicitly needed without the rest of the pre-execution packet.

```md
## Rule-Loading Summary
- Task type:
- Execution mode:
- Meta:
- Core:
- Extensions:
- Playbooks:
- Project Rules:
- Review:
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED
```

## Rule-Loading Exception

Use when a rule-loading problem forces targeted expansion.

```md
## Rule-Loading Exception
- Status: BLOCKED / ALLOW_WITH_WARNINGS
- Reason for expansion:

### Reasons
1.

### Required additions or corrections
1.
```

## Rule-Loading Risk Notes

Use for high-risk rule-loading cases that need more explanation but do not justify a full manifest.

```md
## Rule-Loading Risk Notes
- Risk focus:
- Affected rules:
- Why they matter now:
- Extra checks or blockers:
```

## Rule-Loading Manifest

Use only in detailed mode or when traceable evidence explicitly requires the canonical full manifest.

Schema contract:

- Keep this structure exactly for every full manifest.
- Do not rename, remove, merge, or reorder the `Loaded Rules` columns.
- The `Loaded Rules` table must include `Type`, `Rule`, `Path`, `Why loaded`, and `Detail level`.
- Use a table for `Loaded Rules`, `Deferred Rules`, and `Possibly Missing Rules`; do not collapse them into prose or bullet lists.
- If a path is not yet known, write `unverified` or `not yet discovered` in the `Path` cell instead of omitting the column.
- The execution decision must use one of `ALLOW`, `ALLOW_WITH_WARNINGS`, or `BLOCKED`, followed by the reason.

```md
# Initial Rule-Loading Manifest

## 1. Task Identification
- Project:
- Stack:
- Task type:
- Risk tags:
- Complexity:
- Risk score:
- Execution mode:

## 2. Current Stage
- Stage:

## 3. Loaded Rules
| Type | Rule | Path | Why loaded | Detail level |
|---|---|---|---|---|

## 4. Deferred Rules
| Rule | Why deferred | Trigger to load later |
|---|---|---|

## 5. Possibly Missing Rules
| Rule type | Why it may be needed |
|---|---|

## 6. Execution Decision
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED
- Reason:
```

## Project Understanding Summary

Internal-only in T1/T2. Internal record by default when structural understanding is required before impact analysis.

```md
## Project Understanding Summary
- Tooling:
- Tool state:
- Related entries:
- Similar implementations:
- Impacted surfaces:
- Do-not-edit surfaces:
- Risks:
- Repair / fallback path:
- Fallback note:
```

## Project Understanding Focused Expansion

Use when only the risky or anomalous structural surfaces need extra explanation.

```md
## Project Understanding Focused Expansion
- Expanded area:
- Tool state:
- Risky entry points or shared surfaces:
- Critical call-chain note:
- Do-not-edit note:
- Repair / fallback path:
- Why expanded:
```

## CodeGraph Project Understanding Report

Use only when detailed disclosure is required after routing and before impact analysis.

```md
# CodeGraph Project Understanding Report

## 1. Related Entry Points
| Type | Entry | File | Notes |
|---|---|---|---|

## 2. Call Chain
[Write the call chain as plain text lines in execution output.]

## 3. Similar Implementations
| Similar implementation | File | Reusable point | Reuse recommended |
|---|---|---|---|

## 4. Impact Scope
### Direct Impact
### Indirect Impact
### Do Not Edit

## 5. Test Impact
## 6. Risk Points
## 7. Conclusion
- Primary structural tool:
- Tool state:
- Repair / fallback path:
- Allow entry to Impact Analysis:
- Need dynamic reroute:
- Need extra rules:
```

## Official Docs Check Report

Use only when detailed disclosure is required and official platform or framework constraints need a full explicit record.

```md
# Official Docs Check Report

## 1. Platform / Framework Surface
## 2. Query Method And Source Mode
## 3. Official Requirements To Confirm
## 4. Official Sources
## 5. Context7 Findings
## 6. Original Official Verification
## 7. Implementation Constraints
## 8. Test And Compatibility Notes
## 9. Fallback Or Unverified Items
## 10. Conclusion
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED
```

## Strict Project Understanding Additions

Add these sections for `STRICT` work or when the task touches shared or high-risk surfaces.

```md
## 8. Reverse Dependencies
## 9. Shared Module And Global Style Surface
## 10. Permission, State, Performance, And Rollback Paths
```

## Impact Analysis Summary

Internal-only in T1/T2. Internal record by default when explicit impact reconnaissance is still needed before execution.

```md
## Impact Analysis Summary
- Goal:
- Likely touched surfaces:
- Primary risks:
- Required checks:
- Unverified:
```

## Impact Analysis Focused Expansion

Use when only the risky impact surfaces need more detail.

```md
## Impact Analysis Focused Expansion
- Expanded risk area:
- Affected contract, data, state, or permission surface:
- Required tests or checks:
- Blockers or unverified:
```

## Impact Analysis

Use only when detailed disclosure is required after project understanding and before Task Contract freezing.

```md
# Impact Analysis

## 1. Goal
## 2. Likely Impacted Files Or Modules
## 3. Likely Impacted Entry Points
## 4. Contract And Data Risks
## 5. State, Permission, And Audit Risks
## 6. Test And Reproduction Requirements
## 7. Docs, Config, And Release Sync
## 8. Candidate Non-Goals
## 9. Unverified Items
```

## Strict Impact Analysis Additions

Add these sections for `STRICT` work or when high-risk surfaces need deeper traceability.

```md
## 10. Compatibility And Dependency Matrix
## 11. Performance, Observability, And Rollback Risks
## 12. Blockers And Human Confirmation Points
```

## Task Contract Summary

T1 default. Use when explicit scope control is still needed before execution.

```md
## Task Contract Summary
- Goal:
- Scope:
- Tests:
- Acceptance:
- Official constraint:
```

`Official constraint` is optional. When official docs apply, carry **one binding rule in one line** only — for example lifecycle, permission, threading, or deprecated-API limit. Do not paste doc excerpts or multi-bullet official lists into TCS; keep detail in internal Official Docs Check Summary unless a `Risk Note` is required.

Legacy mapping when compressing from detailed notes:

- `Scope` = allowed edit surfaces plus forbidden/out-of-scope surfaces in one line
- `Tests` = failing checks, reproduction path, or minimum verification plan
- `Acceptance` = done-when criteria
- `Official constraint` = single binding official rule when platform docs govern the slice; omit when not applicable

## Task Contract Focused Expansion

Use when only the risky contract slices need extra tightening or explanation.

```md
## Task Contract Focused Expansion
- Tightened scope:
- Added constraints:
- Added acceptance checks:
- Stop or rollback condition:
```

## Task Contract

T3 detailed-only. Use only when detailed disclosure is required after impact analysis and before execution begins.

```md
# Task Contract

## 1. Task Goal
## 2. Non-Goals
## 3. Allowed Edit Scope
## 4. Forbidden Scope
## 5. Loaded Rule Summary
## 6. Key Constraints
## 7. TDD / Test Requirements
## 8. Acceptance Criteria
## 9. Risks And Rollback
```

## Strict Task Contract Additions

Add these sections for `STRICT` work or when human confirmation is required.

```md
## 10. Human Confirmation Points
## 11. Phased Execution Plan
## 12. Rollback / Degradation Plan
## 13. Blocking Conditions
```

## Completion Summary

T1b default outward block when work is finished. Use instead of full completion reports in ordinary tasks.

```md
## Completion Summary
- Changed:
- Verified:
- Acceptance:
- Diff scope:
- Unverified:
```

`Diff scope` confirms Minimum Change Constraint compliance: only Task Contract–allowed surfaces changed.

### LITE Completion Summary

Use when `LITE execute` finishes. Shorter than the default T1b completion block.

```md
## Completion Summary
- Changed:
- Done check:
- Unverified:
```

For `bugfix` tasks, do not use LITE completion; use the bug-fix field set below instead:

```md
## Completion Summary
- Repro:
- Red-before:
- Root cause:
- Green-after:
- Diff scope:
- Unverified:
```

## Review Summary

T1b default outward block for review-only tasks. Use instead of the 19-section `Review Report` in ordinary review work.

```md
## Review Summary
- Verdict: APPROVED / APPROVED_WITH_WARNINGS / CHANGES_REQUIRED / BLOCKED
- Severity: NONE / P3 / P2 / P1 / P0
- Findings:
- Required fixes:
- Recommendation:
```

Keep findings as a short bullet list, usually 3-8 items, findings first.

## Development Completion Report

T3 detailed-only. Do not emit in default T1/T2 completion outward.

```md
# Development Completion Report

## 1. Change Summary
## 2. Project Understanding Record
## 3. Task Contract Record
## 4. Rule-Loading Record
## 5. Entry-Point Check
## 6. UI and Functional Binding
## 7. Interfaces and Data
## 8. TDD Record
## 9. Test Verification
## 10. Acceptance Criteria Check
## 11. Performance and Long-Term Maintenance
## 12. Project Rule Compliance
## 13. Documentation Sync
## 14. Risks and Rollback
## 15. Unverified Items
```

## Bug-Fix Completion Report

T3 detailed-only. Do not emit in default T1/T2 completion outward.

```md
# Bug-Fix Completion Report

## 1. Symptom
## 2. Project Understanding Record
## 3. Diagnosis
## 4. Reproduction
## 5. Root-Cause Evidence Chain
## 6. Counter-Evidence Check
## 7. Loaded Playbooks
## 8. Task Contract Record
## 9. Failing Test or Minimal Reproduction
## 10. Minimal Fix
## 11. Regression Verification
## 12. Acceptance Criteria Check
## 13. Unverified Items
## 14. Failure-Retrospective Triggered
```

## Review Verdict Mapping

审查报告的 `Verdict` 必须使用固定档位，`Final Recommendation` 必须与 `Verdict` 保持一致，不得自由漂移。

- `APPROVED`: 没有已确认问题，或最高已确认严重级别仅为 `P3`
- `APPROVED_WITH_WARNINGS`: 最高已确认严重级别为 `P2`
- `CHANGES_REQUIRED`: 最高已确认严重级别为 `P1`
- `BLOCKED`: 最高已确认严重级别为 `P0`

如果缺少必需证据、测试、验收或规则门禁，可以把 `Verdict` 升级到更严格档位，但不能降到映射档位以下。

`Severity Level` 写最高已确认 finding 严重级别；如果没有已确认 finding，写 `NONE`。

## Review Report

T3 detailed-only. Do not emit in default T1/T2 review outward. For ordinary review, use `Review Summary` instead.

```md
# Review Report

## 1. Verdict
- Value: APPROVED / APPROVED_WITH_WARNINGS / CHANGES_REQUIRED / BLOCKED
## 2. Severity Level
- Highest confirmed severity: NONE / P3 / P2 / P1 / P0
## 3. Confirmed Facts
## 4. Unconfirmed Items
## 5. Project Understanding Review
## 6. Task Contract Review
## 7. Rule-Loading Review
## 8. Loaded Review Extensions
## 9. Loaded Project Review Rules
## 10. TDD Review
## 11. Root-Cause Review
## 12. UI Implementation Review
## 13. Performance and Long-Term Maintenance Review
## 14. Project Rule Compliance Review
## 15. Acceptance Criteria Review
## 16. Blocking Issues
## 17. Required Fixes
## 18. Suggested Improvements
## 19. Final Recommendation
- Recommendation must match Verdict and state the next step in concise Chinese.
```
