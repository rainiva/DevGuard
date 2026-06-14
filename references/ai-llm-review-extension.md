# AI LLM Review Extension

Use this when reviewing AI or agent features.

## Review Checks

Verify:

1. the AI feature has a clear user-facing contract
2. tool use, memory use, and retry behavior are bounded
3. success claims distinguish real integration from mock behavior
4. logging or traces are sufficient to diagnose failures
5. cost, latency, and fallback behavior were considered

## Findings Focus

Prefer findings around:

- unbounded loops or retries
- unverifiable prompt-only claims
- fake integration success
- missing observability
- missing fallback behavior
