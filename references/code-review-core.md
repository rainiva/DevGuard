# Code Review Core

Use this when reviewing changes or when implementation should stay aligned with the eventual review bar.

## Review Priorities

Focus on:

1. behavioral correctness
2. regression risk
3. contract consistency
4. data and state safety
5. permission and security boundaries
6. test adequacy
7. missing evidence

Classify severity with [severity-levels.md](severity-levels.md).
审查报告必须同时给出固定档位 `Verdict`。`Severity Level` 记录最高已确认 finding 严重级别，`Verdict` 必须满足严重级别映射得到的最低严格度，并且只能升级，不能放宽。
Load [official-docs-review-extension.md](official-docs-review-extension.md) when platform, framework, SDK, host, system-API, or design-guideline compliance is part of the review bar.

Keep summaries brief. Findings come first.

## Required Review Checks

Review whether:

1. the rule-loading plan matched the task
2. required project understanding existed before impact analysis or broad edits
3. required official docs check existed before platform, framework, SDK, host, control-template, or design-sensitive edits
4. impact analysis existed before broad edits
5. the Task Contract existed before execution and stayed tighter than the impact analysis
6. the Red phase existed for code changes
7. the implemented behavior is actually bound to the visible entry point
8. interface, data, and permission changes are fully accounted for
9. the stated acceptance criteria were actually verified
10. tests and docs were updated where needed
11. performance or rollback risks were ignored or hand-waved

## Output Shape

Default to:

1. Findings ordered by severity, with file references when available
2. Open questions or assumptions
3. Brief change summary only after findings

## Review Discipline

- Do not praise away risk.
- Do not accept "should work" in place of evidence.
- If there are no findings, say that explicitly and mention any residual risk or testing gap.
