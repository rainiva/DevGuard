# Review Mirroring Rules

Use this when deciding how implementation-side rule loading must be reflected during review.

## Core Principle

If a rule or extension changed how the work should be done, review must check whether that rule was actually followed.

## Mirroring Rules

- A loaded development core implies review should verify its required outputs.
- A loaded domain core implies the matching review extension should be considered during review.
- A loaded `official-docs-check` pass implies review should verify the matching official platform, framework, SDK, host, or design-guideline constraints.
- A loaded project implementation file implies the matching project review file should be considered when review begins.
- A loaded playbook implies review should verify the playbook's promised evidence and validation path.

## Required Review Questions

1. Which implementation-side rules were loaded?
2. Which review-side rules mirror them?
3. What did the Task Contract require and forbid?
4. Which required artifacts should now exist because those rules were loaded?
5. Did the actual work produce those artifacts and stay inside the contract?

## Failure Modes

Flag review problems when:

- implementation invoked a rule set but produced none of its expected outputs
- review ignores a domain-specific risk that implementation was supposed to handle
- project-specific hard blocks were checked during implementation but not during review
- the rule-loading output does not explain the implementation-to-review mapping
- review ignores contract-defined non-goals or out-of-scope boundaries

## Manifest Guidance

The routing report or review report should make the mirror explicit whenever the task is non-trivial, and the review report should say whether the final work still matches the Task Contract.
