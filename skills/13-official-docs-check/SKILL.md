---
name: devguard-official-docs-check
description: Internal DevGuard module for confirming official platform, framework, SDK, host-integration, and platform-design constraints before impact analysis, preferring Context7-style official-docs lookup first and original official-doc verification for high-risk work.
---

# DevGuard Official Docs Check

Use this module through the external `DevGuard` skill. Read `references/official-docs-check.md`, assume required project understanding already happened, and confirm the official platform or framework constraints before impact analysis begins.

When available, prefer Context7 or an equivalent official-docs MCP for L1 scoped summary. Apply L2 original-doc verification for `S3+`, deprecated APIs, permission, installer, or security surfaces. Apply L3 human confirmation for `STRICT` plus release work. Carry at most one `Official constraint` line in Task Contract Summary.

If Context7 is missing, misconfigured, unreachable, or version-ambiguous, follow the availability, repair, retry, and fallback flow in `references/official-docs-check.md`. Do not degrade immediately, and do not treat a tooling-setup request as an ordinary docs-fallback case.

Keep the default outward output compact. Keep the official-docs record internal by default, and do not emit a separate `Official Docs Check Summary` outward unless the route explicitly requires focused or detailed disclosure, or an official constraint materially changes the Task Contract, blocks work, or explains an anomaly.
