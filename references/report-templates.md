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
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED / INQUIRY
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
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED / INQUIRY
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
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED / INQUIRY
- Next:
```

Use `INQUIRY` only while Socratic inquiry is active. During inquiry, do not emit `Task Contract Summary`.

## Inquiry Note

Use while `Status: INQUIRY` for one Socratic question per message.

```md
## Inquiry Note
- Gap:
- Question:
- Options:
- Recommendation:
- Why:
- Status: INQUIRY
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
- Tool:
- Platform / framework:
- SDK / API / host:
- Query target:
- Key official findings:
- Constraint on this task:
- Source mode:
- Context7 state:
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED / INQUIRY
```

## Official Docs Focused Expansion
- Expanded area:
- Context7 / source scope:
- Repair / fallback path:
- Need original-doc verification:
- Key official basis:
- Implementation constraints:
- Test or compatibility note:
- Status: ALLOW / ALLOW_WITH_WARNINGS / BLOCKED / INQUIRY
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

- Official constraint: optional one-line binding rule when platform docs govern the slice.

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

## T3 Detailed Templates

See [report-templates-detailed.md](report-templates-detailed.md).

