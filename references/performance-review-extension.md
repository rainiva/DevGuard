# Performance Review Extension

Use this when reviewing performance-sensitive work.

## Review Checks

Verify:

1. the hot path or scale-sensitive surface was identified explicitly
2. the change includes a credible limiting or scaling strategy
3. obvious performance risks were not deferred without analysis
4. measurement, profiling, or verification plans match the risk
5. AI cost or iteration growth is handled when applicable

## Findings Focus

Prefer findings around:

- unbounded list or API behavior
- missing scale strategy
- hand-waved latency or memory risk
- no measurement plan on clearly risky changes
