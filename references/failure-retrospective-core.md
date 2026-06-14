# Failure Retrospective Core

## Metadata

- Layer: core
- Load level: metadata, summary, full
- Use when: the same issue has failed twice, the evidence chain is weak, or repairs are turning into trial and error.
- Risk tags: `repair_failure`, `observability`, `recoverability`

## Summary

Stop further repairs until the previous attempts, assumptions, missing evidence, and new validation path are explicit.

## Full Rule

Before a third attempt:

1. List the previous attempts and observed outcomes.
2. Separate proven facts from guesses.
3. Identify why the previous hypothesis failed.
4. Gather at least one new piece of evidence.
5. Form a new root-cause hypothesis.
6. Define a smallest validation check for the next attempt.
7. If platform, framework, SDK, host, control-template, or system-API behavior may be involved, rerun official docs check before another repair attempt.
8. Decide whether a new playbook, project rule, or review extension must be loaded.

Do not continue with another code edit if the new attempt has no new evidence.
