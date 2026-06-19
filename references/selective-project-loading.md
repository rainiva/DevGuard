# Selective Project Loading

Use this when a project is known but only part of its rule pack is relevant to the current task.

## Core Rule

Load the project index first, then only the project files the current task actually hits.

If the project identity is known and the task depends on project-specific behavior, the project index is a required rule file, not an optional convenience.

## Selection Flow

1. Identify the project.
2. Load its index.
3. Match the task to project domains or subsystems.
4. Load only the domain files needed now.
5. Add review-side project files when the task enters review.

## Missing Project Rule Gate

If the project identity is known but `project-rules/<project>/` or the project index cannot be found or confirmed:

1. emit `Exception Note`
2. set status to `BLOCKED` when project rules are required for safe execution
3. set status to `ALLOW_WITH_WARNINGS` only when the task is explicitly generic and project-specific rules are not needed yet
4. say which project path or index is missing
5. do not invent project-rule paths, loaded-rule success, or project-specific constraints

If the project identity is unknown but project-specific behavior may matter, keep the project-rule status unverified, defer project domain files, and use focused expansion to explain what would trigger loading or blocking.

## What To Avoid

- loading the whole project pack because the project name is known
- loading installer rules for a UI-only change
- loading unrelated business domains just because they exist nearby
- forcing review files into implementation if the task has not reached review

## Decision Prompts

Ask these internally:

1. Which project domain does the task touch?
2. Which project rule files govern that domain?
3. Which project files are explicitly out of scope?
4. What would trigger loading more project files later?

## Rule-Loading Output Requirement

If project rules are involved, the rule-loading output should say:

1. which project index was loaded
2. which domain files were loaded
3. which project files were deliberately deferred
4. whether project-rule loading is complete, deferred, warning-only, or blocked

If full-manifest mode is active, keep those project rows in the canonical loaded and deferred tables instead of collapsing them into prose.
