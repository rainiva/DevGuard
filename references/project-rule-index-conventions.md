# Project Rule Index Conventions

Use this when shaping project-specific rule packs or deciding how a project rule set should be entered.

## Goal

Make project rules discoverable without forcing full-project rule loading.

## Index Responsibilities

Each project rule pack should start with a small index file that tells DevGuard:

1. what the project is
2. what major domains exist
3. which files matter for which task families
4. which project-specific hard blocks exist
5. which review-side files mirror the implementation-side files

## Index Content

At minimum, include:

- project overview
- version
- stack summary
- domain map
- file-to-domain routing hints
- task-family entrypoints
- hard blockers
- review companions

## Packaging Rules

- Put project facts in project files, not in generic core references.
- Keep the index short enough to load early.
- Split detailed project rules by domain or subsystem.
- Prefer stable paths and naming that reveal the domain.
- Version project-rule changes so reviewers can tell whether the loaded rules match the task date and project state.

## Example Shape

Possible project pack layout:

- `project-rules/<project>/index.md`
- `project-rules/<project>/ui.md`
- `project-rules/<project>/api.md`
- `project-rules/<project>/data.md`
- `project-rules/<project>/review-ui.md`
- `project-rules/<project>/review-api.md`
