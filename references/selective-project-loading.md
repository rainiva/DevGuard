# Selective Project Loading

Use this when a project is known but only part of its rule pack is relevant to the current task.

## Core Rule

Load the project index first, then only the project files the current task actually hits.

## Selection Flow

1. Identify the project.
2. Load its index.
3. Match the task to project domains or subsystems.
4. Load only the domain files needed now.
5. Add review-side project files when the task enters review.

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

If full-manifest mode is active, keep those project rows in the canonical loaded and deferred tables instead of collapsing them into prose.
