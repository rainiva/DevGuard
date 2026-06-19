# Batch Roadmap

Use this reference when extending DevGuard itself. Build it in slices instead of recreating the original all-in-one rules document.

## Batch 1

Goal: establish the orchestration control plane.

Include:

- `SKILL.md`
- `task-routing.md`
- `rule-loading.md`
- `shared-guardrails.md`
- `report-templates.md`
- `agents/openai.yaml`

Status: implemented in the current slice.

## Batch 2

Goal: add execution-core references that DevGuard routes to most often.

Recommended additions:

- `impact-analysis-core.md`
- `tdd-workflow-core.md`
- `daily-development-core.md`
- `code-review-core.md`
- `release-check-core.md`

Status: implemented in the current slice.

## Batch 3

Goal: add high-frequency domain extensions.

Recommended additions:

- `ui-implementation-core.md`
- `bug-fix-core.md`
- `migration-refactor-core.md`
- `ai-llm-feature-core.md`
- `performance-impact-core.md`
- paired review-extension references

Status: implemented in the current slice.

## Batch 4

Goal: add playbook and project-rule packaging conventions.

Recommended additions:

- playbook directory conventions
- project-rule index conventions
- selective project-file loading guidance
- review-extension mirroring rules

Status: implemented in the current slice.

## Batch 5

Goal: add forward-testing guidance and optional helper scripts.

Recommended additions:

- lightweight validation or manifest-generation scripts
- example prompts for realistic routing tasks
- forward-test scenarios for feature, bug, UI, migration, and review work

Status: implemented in the current slice.

## Batch 6

Goal: reduce token cost while preserving rule-loading safety through tiered disclosure.

Recommended additions:

- default minimal rule-loading summary
- focused expansion for high-risk or anomaly cases, with detailed manifest reserved for debug, verbose, audit, forward-testing, or formal evidence-capture cases
- automatic exception expansion when rules are missing, mismatched, or unverifiable
- script support for `summary`, `risk`, `exception`, `rule-summary`, and `full` output formats

Status: implemented in the current slice.

## Sequencing Rule

Do not jump ahead just because the full target architecture is known. Finish the smallest batch that creates real leverage, validate it, then add the next layer.
