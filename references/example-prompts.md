# Example Prompts

Use these prompts to invoke DevGuard in a realistic way. Replace the task details, but keep the shape compact and concrete.

## Feature Work

`Use $devguard to route a medium-risk feature request in this repo, load only the minimum required rules, keep the default outward output to Execution Summary plus Task Contract Summary, and if risk appears expand only the affected part unless I ask for full detail.`

## UI Work

`Use $devguard to handle a UI implementation task for this screen change. Route it first, use CodeGraph-style project understanding, check the target platform's official design guidance before impact analysis when it matters, load the right UI core and review extension, and keep the visual work bound to real functionality.`

## Bug Fix

`Use $devguard to handle this bug report. Reproduce first, use project understanding to find the entry points and call chain, run official docs check before impact analysis if platform or SDK behavior may be involved, load only the needed bug-fix and playbook-related rules, and do not let implementation start before the evidence chain is clear.`

## Refactor Or Migration

`Use $devguard to plan this refactor. Start with project understanding, run official docs check if platform or framework constraints may govern the new shape, freeze current behavior, classify compatibility and rollback risk, and load only the migration-related rules needed for the current slice.`

## AI Or Agent Feature

`Use $devguard to route this AI feature task. Treat tool calls, memory boundaries, observability, and cost controls as first-class routing factors, run project understanding before impact analysis, run official docs check if SDK constraints matter, emit Execution Summary plus Task Contract Summary by default, and if risk appears expand only the affected part before freezing the Task Contract.`

## Platform Or SDK Work

`Use $devguard to route this platform-sensitive task. Use project understanding to learn the code path, confirm the official platform or framework constraints before impact analysis, keep the default outward output minimal, and block if the implementation would violate official requirements or uses deprecated APIs without a reason.`

## Review

`Use $devguard to review this change set. Mirror the implementation-side rules into review-side verification, list findings first, and call out any missing evidence or missing gates.`

## Project Rule Loading

`Use $devguard to determine which project-specific rules should be loaded for this task. Load the project index first, then only the matching domain files, state which project files remain deferred, and expand to a full manifest only if the task or mode requires it.`
