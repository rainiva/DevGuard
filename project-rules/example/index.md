# Example Project Rule Index

Version: `0.1.0`

## Project Overview

This sample pack demonstrates how a project-specific rule index should route project facts without loading every project rule file.

## Stack Summary

- UI: project-specific UI rules live in `ui.md`
- API: project-specific API rules live in `api.md`
- Data: project-specific data rules live in `data.md`

## Domain Map

| Task area | Load |
|---|---|
| UI or visual flow | `ui.md`, then `review-ui.md` during review |
| API contract | `api.md`, then `review-api.md` during review |
| Data shape or migration | `data.md` |

## Hard Blockers

- Do not skip project review companions when the task enters review.
- Do not copy these sample rules into a real project without replacing the project facts.

## Review Companions

- `ui.md` mirrors to `review-ui.md`
- `api.md` mirrors to `review-api.md`
