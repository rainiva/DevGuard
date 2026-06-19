---
name: devguard-codegraph-project-understanding
description: Internal DevGuard module for CodeGraph-first project structure understanding before impact analysis for code changes, bug fixes, feature work, refactors, API or state changes, multi-page UI or global style work, performance issues, or when entry points are unclear.
---

# DevGuard CodeGraph Project Understanding

Use this module through the external `DevGuard` skill. Read `references/codegraph-project-understanding.md`, prefer CodeGraph first, run the documented freshness gate before trusting any structural answer, attempt the documented host-specific repair and retry flow before dropping to lower-priority structural tools, and if CodeGraph stays unavailable apply the documented No-Index Fallback (`codegraph_unavailable`, limited read for `S1`, init or `ALLOW_WITHOUT_CODEGRAPH` for `S2+`). Record `Structural tool` in `Execution Summary` when fallback is active. Establish the project-understanding record at the routed depth before impact analysis or Task Contract work begins. Keep that record internal by default. Do not emit a separate `Project Understanding Summary` outward unless the route explicitly calls for focused or detailed disclosure, or a blocker, anomaly, reroute trigger, or implementation-changing risk requires it.
