# Performance Impact Core

Use this when the task touches hot paths, large collections, high-frequency APIs, rendering-heavy UI, batch processing, AI loops, or any surface where latency or throughput matters.

## Goal

Force performance thinking before the change becomes expensive to unwind.

## Required Flow

1. Identify the hot path or scale-sensitive surface.
2. State the likely performance risk: latency, throughput, memory, render cost, query cost, startup time, or background load.
3. Check whether the task needs measurement, profiling, or at least a reasoned budget.
4. Look for pagination, batching, caching, debounce, backpressure, or concurrency concerns as applicable.
5. Decide what must be verified now versus later.

## Guardrails

- Do not mark an obvious hot path risk as "future optimization" with no analysis.
- Do not assume small sample behavior will scale.
- Do not accept large-list or high-frequency changes without limiting strategy.
- Do not ignore AI cost or iteration growth when it is part of the performance surface.

## Required Output

Capture:

1. hot path
2. risk type
3. limiting or scaling strategy
4. measurement or verification plan
5. unverified performance assumptions
