# Release Check Core

Use this when a task affects packaging, rollout, installation, migration, deployment, or any user-facing release surface.

## Goal

Prevent changes from being treated as releasable without explicit go-live evidence.

## Required Checks

Check these areas as applicable:

1. build or packaging status
2. config and environment dependencies
3. migration and compatibility notes
4. rollback path
5. degradation or feature-flag path
6. observability and diagnostics readiness
7. release-note or operator-facing documentation updates
8. official host, installer, service, or platform constraints when the release surface depends on them

## Release Guardrails

- Do not equate build success with release readiness.
- Do not ship high-risk changes without rollback thinking.
- Do not claim rollout safety if the live path was not verified.
- Do not hide environment assumptions.

## Minimum Release Output

Produce:

1. what was validated
2. what remains unvalidated
3. rollback or mitigation path
4. blockers to release, if any
