# Performance Review Core

## Metadata

- Layer: review
- Load level: metadata, summary, full
- Use when: review is primarily about latency, throughput, memory, rendering, query cost, background load, or AI cost.
- Risk tags: `performance`, `cost`, `long_running_task`, `observability`

## Summary

Verify that performance-sensitive work identified the hot path, used a credible limiting strategy, and did not defer obvious risk without analysis.

## Full Rule

Review:

1. The named hot path or scale-sensitive surface.
2. The expected risk type.
3. Pagination, batching, caching, throttling, debounce, backpressure, or concurrency limits.
4. Measurement, profiling, benchmark, or reasoned budget.
5. AI iteration, token, latency, and cost growth where applicable.
6. Observability needed to diagnose slow behavior.

Block if a large-list, hot API, AI loop, or long-running task has no bounds and no performance verification plan.
