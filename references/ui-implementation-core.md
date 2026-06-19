# UI Implementation Core

Use this for user-visible page, screen, dialog, settings, or flow changes.

## Goal

Translate a UI request into a real interface with correct hierarchy, states, and functional binding.

## Required Flow

1. Clarify the page or flow goal.
2. Identify the information hierarchy.
3. Check for existing components and tokens before inventing new patterns.
4. Confirm target-platform design guidelines and interaction expectations unless a deliberate product rule overrides them.
5. Enumerate UI states: loading, empty, error, success, disabled, and permission-limited as applicable.
6. Bind visible actions to real behavior.
7. Check responsive or window-fit behavior.
8. Define at least one verification path that exercises the real user operation flow.
9. Prepare UI acceptance notes for review.

## Guardrails

- Do not redesign the entire product when the task is local.
- Do not ship visual placeholders as working flows.
- Do not leave important states implicit.
- Do not add style weight where hierarchy and spacing should solve the problem.
- Do not drift away from target-platform design guidelines without an explicit reason.
- Do not claim UI completion using only internal methods, functions, interfaces, or ideal-path checks when the acceptance criteria are user-visible.
- If the design intentionally deviates from platform guidance, explain the reason, replacement basis, accessibility impact, consistency impact, and whether extra UI review is needed.

## Required Output

Capture:

1. affected screens or components
2. required states
3. real bindings and data dependencies
4. responsive or layout risks
5. platform-design constraints or justified deviations
6. accessibility or usability concerns
7. real user operation paths that were verified
