---
name: devguard-impact-analysis
description: Internal DevGuard module for impact analysis before non-trivial implementation, refactor, migration, UI, API, data, permission, performance, or release-sensitive changes.
---

# DevGuard Impact Analysis

Use this module through the external `DevGuard` skill. Read `references/impact-analysis-core.md`, assume required project understanding already happened, emit the routed Impact Analysis depth, identify the fan-out impact and risk surface, and hand the resulting scope decisions into the Task Contract. Add domain extensions only when the current task hits them.
