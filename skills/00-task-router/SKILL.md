---
name: devguard-task-router
description: Internal DevGuard module for task routing, risk classification, execution mode selection, skill-chain selection, rule-loading strategy, stage gates, dynamic reroute conditions, and human confirmation points.
---

# DevGuard Task Router

Use this module through the external `DevGuard` skill. Read `references/task-routing.md`, then emit the routing decision, Task Profile, and required rule-loading disclosure before any execution work begins. Decide whether project understanding is required, decide whether official docs check is required, decide the needed project-understanding, official-docs, Impact Analysis, and Task Contract rigor here, and default the outward report to `Execution Summary` plus visible `Task Contract Summary`, with only focused risk or anomaly expansion unless explicit detailed disclosure is actually required.
