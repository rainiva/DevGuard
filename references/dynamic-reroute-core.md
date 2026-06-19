# Dynamic Reroute Core

## Metadata

- Layer: core
- Load level: metadata, summary, full
- Use when: new evidence changes task type, risk tags, complexity, loaded-rule sufficiency, or execution stage.
- Risk tags: `repair_failure`, `release`, `security`, `migration`, `performance`, `ai_output`

## Summary

Reroute when the original route no longer matches the task reality. Rerouting is a normal control mechanism, not a failure.

Default outward reroute update: refresh only `Execution Summary` fields for Mode, Rules, Status, and Next. Do not dump a full routing transcript unless detailed disclosure is active.

## Full Rule

### Reroute Trigger Table

| Trigger | Action |
|---|---|
| Phase shifts to review or release | Load review or release rules; switch Named Route to `route:review-only` or release chain |
| Hidden contract, data, permission, or compatibility surface appears | Rerun impact analysis; amend or rebuild Task Contract before further execution |
| Concrete bug category becomes clear and needs a playbook | Load the matching playbook; refresh rule-loading output |
| Same issue fails twice | Enter failure retrospective; reroute through `failure-retrospective-core -> dynamic-reroute-core` |
| User changes requested outcome | Rebuild Task Profile; amend or rebuild Task Contract |
| Socratic inquiry reveals new task family, scope, or success bar | Rerun Socratic inquiry or rebuild Task Profile before project understanding |
| Blocker appears | Emit `Exception Note`; set status to `BLOCKED` until the blocker clears |

### Reroute Procedure

On reroute:

1. Emit a short updated routing decision internally.
2. Refresh the required rule-loading output.
3. Rerun Socratic inquiry when Task Profile ambiguity reappears.
4. Rerun project understanding when entry points or shared surfaces changed.
5. Rerun official docs check when platform, framework, SDK, host, control-template, or design constraints changed.
6. Amend or rebuild the Task Contract before further execution if scope, risk, or acceptance criteria changed.

### Outward Disclosure On Reroute

In default summary mode, update only these `Execution Summary` fields outward:

- Mode
- Rules
- Status
- Next

Keep the reroute rationale compact inside `Risk Note` or `Exception Note` when the user needs to see why the route changed. Use full `Skill Routing Decision` only when detailed disclosure is active.
