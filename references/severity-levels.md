# Severity Levels

## Metadata

- Layer: shared
- Load level: metadata, summary, full
- Use when: classifying review findings, blockers, routing risk, or release readiness.

## Summary

Use severity to make decisions clear and reviewable. Severity is about user impact, blast radius, reversibility, and evidence quality.

## Review Verdict Mapping

审查报告的 `Verdict` 必须使用固定档位：`APPROVED`、`APPROVED_WITH_WARNINGS`、`CHANGES_REQUIRED`、`BLOCKED`。

默认按最高已确认严重级别映射：

- `P0` -> `BLOCKED`
- `P1` -> `CHANGES_REQUIRED`
- `P2` -> `APPROVED_WITH_WARNINGS`
- `P3` -> `APPROVED`
- no confirmed findings -> `APPROVED`

严格度顺序为：`APPROVED` < `APPROVED_WITH_WARNINGS` < `CHANGES_REQUIRED` < `BLOCKED`。

`Severity Level` 字段只记录最高已确认 finding 严重级别；如果没有已确认 finding，写 `NONE`。

如果缺少必需证据、必需测试、必需验收、必需规则门禁，或存在不可接受的不确定性，可以把 `Verdict` 升级到更严格档位；禁止把 `Verdict` 放宽到低于最高已确认严重级别所允许的档位。

## Full Rule

- `P0 Blocker`: unsafe to proceed. Data loss, security exposure, broken release path, invented evidence, missing required gate, or critical user-flow failure.
- `P1 Must Fix`: high-risk correctness, contract, migration, permission, or release issue that should block completion until fixed.
- `P2 Should Fix`: meaningful maintainability, test, observability, UI state, or edge-case issue that can cause avoidable rework or defects.
- `P3 Consider`: useful improvement that is not required for this task to be accepted.

When in doubt, explain the uncertainty and classify based on the worst credible impact.
