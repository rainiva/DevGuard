# Migration Refactor Core

Use this for structural changes, responsibility moves, contract reshaping, compatibility refactors, or data or config migrations.

## Goal

Change structure without losing behavioral truth or rollout safety.

## Required Flow

1. Freeze current behavior with tests, fixtures, or explicit baselines.
2. Map current and target boundaries.
3. Identify contract, config, data, and packaging surfaces.
4. Break the work into reversible slices.
5. Keep compatibility notes explicit while both old and new paths coexist.
6. Re-verify behavior after each slice.
7. Record rollback or fallback expectations where applicable.

## Guardrails

- Do not refactor first and define behavior later.
- Do not merge compatibility and cleanup concerns into one opaque change set.
- Do not hide externally visible behavior changes under the label of refactor.
- Do not migrate data or config without compatibility and rollback thinking.

## Required Output

Capture:

1. frozen baseline
2. target boundary
3. migration or compatibility risks
4. slice plan
5. rollback or fallback path
