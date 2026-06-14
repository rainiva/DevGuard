# AI LLM Feature Core

Use this for LLM features, agent loops, memory systems, tool-calling workflows, prompt-bound behavior, or cost-sensitive AI flows.

## Goal

Build AI behavior that is observable, bounded, and honest about uncertainty.

## Required Flow

1. Define the user-visible contract of the AI behavior.
2. Identify prompt, tool, memory, and model boundaries.
3. Define what counts as success, fallback, and failure.
4. Bound iterations, tokens, cost, and time where applicable.
5. Capture logging or trace surfaces needed for diagnosis.
6. Build the smallest realistic validation path.
7. Mark unverified claims explicitly.

## Guardrails

- Do not treat prompt text as sufficient verification.
- Do not leave tool loops, retries, or memory growth unbounded.
- Do not present synthetic or mocked tool success as real integration success.
- Do not hide ambiguous behavior behind confident wording.

## Required Output

Capture:

1. user-facing AI contract
2. tool and memory boundaries
3. iteration or cost limits
4. observability hooks
5. realistic validation path
