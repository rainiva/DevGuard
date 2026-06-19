---
name: devguard-impact-analysis
description: Internal DevGuard module for impact analysis before non-trivial implementation, refactor, migration, UI, API, data, permission, performance, or release-sensitive changes.
---

# DevGuard Impact Analysis

Use this module through the external `DevGuard` skill. Read `references/impact-analysis-core.md`, assume required project understanding already happened, establish the impact-analysis record at the routed depth, identify the fan-out impact and risk surface, and hand the resulting scope decisions into the Task Contract. Keep that record internal by default. Do not emit a separate `Impact Analysis Summary` outward unless the route explicitly calls for focused or detailed disclosure, or a blocker, anomaly, reroute trigger, or implementation-changing risk requires it. Add domain extensions only when the current task hits them.
