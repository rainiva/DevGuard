# TDD Workflow Core

Use this for code changes unless the task is analysis-only or the environment truly cannot support a meaningful failing check.

## Default Sequence

Follow `Red -> Green -> Refactor`.

## Red

Create one of these first:

- a failing automated test
- a failing reproduction script
- a smallest possible manual reproduction with explicit steps and expected failure

The Red artifact must prove the problem or missing behavior exists before implementation.
Base the Red artifact on the Task Contract acceptance criteria and keep it focused on the approved scope.

## Green

Implement only the smallest change needed to satisfy the failing check.

Do not bundle in:

- opportunistic cleanup
- unrelated refactors
- style-only rewrites outside the touched logic
- speculative extra features

## Refactor

Refactor only after the failing check passes.

Safe refactor goals:

- simplify control flow
- improve naming
- reduce duplication
- isolate dependencies
- clarify tests

## Exceptions

If full TDD is not practical, still create the closest equivalent evidence-first check and state the limitation explicitly. Never quietly skip the Red phase and still call it TDD.

## Required Record

Capture:

1. What failed first
2. What change made it pass
3. Which Task Contract acceptance criteria the checks cover
4. What verification was rerun after refactor
