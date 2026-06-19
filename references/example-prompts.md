# Example Prompts

Compact invocation shapes. Replace `{task}` with the concrete request.

## Short Triggers

| Trigger | Effect |
|---|---|
| `/devguard lite` | Force `LITE` mode; micro daily execute with `Slice` in ES when whitelist matches; preview-only when user says not to code |
| `/devguard fast` | Force `FAST` mode; compact Contract; minimal pre-execution gates per Gate Matrix |
| `/devguard strict` | Force `STRICT` mode; deep gates; focused expansion on risk |
| `/devguard review` | Review-only route; findings first; no code changes |

Usage: prepend the trigger to the task, for example `` `/devguard lite` fix typo in README line 12 `` or `` `/devguard fast` {task} ``.

Default one-liner when no trigger is given:

`Use $devguard: route, load minimal rules, freeze Task Contract before coding. Outward output ES+TCS only.`

## Scenarios (one line each)

- **LITE daily:** `` `/devguard lite` fix the typo in {file} — freeze Slice in ES, no separate TCS, then edit. ``
- **Feature:** `Use $devguard to route {task}. ES+TCS only; expand on risk.`
- **Ambiguous feature:** `Use $devguard to route {task}. If goal, scope, or success criteria are unclear, run Socratic inquiry first — one question per turn with a recommendation — and do not freeze Task Contract until Task Profile is clear.`
- **UI:** `Use $devguard for UI work on {task}. Real user-path verification in Contract; ES+TCS.`
- **Bug fix:** `Use $devguard for bug fix: {task}. Red before repair; minimal diff; ES+TCS.`
- **Refactor / migration:** `Use $devguard to plan refactor: {task}. Compatibility + rollback first; ES+TCS.`
- **AI / agent:** `Use $devguard for AI feature: {task}. Tool/memory/cost gates; ES+TCS.`
- **Platform / SDK:** `Use $devguard for platform work: {task}. Official docs before IA; block on violation.`
- **Review:** `Use $devguard to review {task}. Findings first; mirror dev-side gates.`
- **Project rules:** `Use $devguard to load project rules for {task}. Index first; defer unrelated files.`

## Detailed Templates

Full bug-fix Evidence Gate prompt: [bug-fix-core.md](bug-fix-core.md#prompt-template).
