# Playbook Conventions

Use this when a task needs a focused troubleshooting or handling guide for a concrete issue category.

## What A Playbook Is

A playbook is a narrow, issue-specific guide. It exists to help once the problem class is already known.

Examples:

- `wpf-scrollbar-bug`
- `api-contract-breakage`
- `frontend-render-performance`
- `memory-loop-failure`

## What A Playbook Is Not

- not a replacement for routing
- not a generic core workflow
- not a dumping ground for every rule in a subsystem

## Packaging Rules

- Group playbooks by problem family, not by broad platform name alone.
- Keep each playbook tight around one issue class.
- Link to playbooks from the main skill or the relevant core layer, but keep the references one hop away from `SKILL.md`.
- Prefer a short summary and a concrete checklist over long narrative prose.

## Suggested Structure

Each playbook should capture:

1. issue class
2. common symptoms
3. likely root-cause families
4. reproduction guidance
5. evidence to collect
6. minimal validation path
7. common false leads
8. review focus

## Loading Rule

Load a playbook only after the issue class is concrete enough. Do not load every playbook for every bug.

When an index points to a concrete playbook path, resolve that path relative to the DevGuard skill root before declaring it missing.
