# Dynamic Reroute Core

## Metadata

- Layer: core
- Load level: metadata, summary, full
- Use when: new evidence changes task type, risk tags, complexity, loaded-rule sufficiency, or execution stage.
- Risk tags: `repair_failure`, `release`, `security`, `migration`, `performance`, `ai_output`

## Summary

Reroute when the original route no longer matches the task reality. Rerouting is a normal control mechanism, not a failure.

## Full Rule

Trigger reroute when:

1. The task shifts phase, such as development to review or release.
2. A hidden contract, data, permission, or compatibility surface appears.
3. A concrete bug category becomes clear and needs a playbook.
4. The same issue fails twice.
5. A blocker appears.
6. A user changes the requested outcome.

On reroute, emit a short updated routing decision, refresh the required rule-loading output, rerun project understanding when entry points or shared surfaces changed, rerun official docs check when platform, framework, SDK, host, control-template, or design constraints changed, and amend or rebuild the Task Contract before further execution if scope, risk, or acceptance criteria changed.
