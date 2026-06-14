---
name: devguard-official-docs-check
description: Internal DevGuard module for confirming official platform, framework, SDK, host-integration, and platform-design constraints before impact analysis, preferring Context7-style official-docs lookup first and original official-doc verification for high-risk work.
---

# DevGuard Official Docs Check

Use this module through the external `DevGuard` skill. Read `references/official-docs-check.md`, assume required project understanding already happened, and confirm the official platform or framework constraints before impact analysis begins.

When available, prefer Context7 or an equivalent official-docs MCP for version-scoped official guidance. When the task is high-risk, disputed, or version-sensitive, verify the original official docs or API reference before treating the official guidance as authoritative.

Keep the default outward output compact. Surface only the required summary or focused expansion unless the route explicitly requires detailed or audit-style evidence.
