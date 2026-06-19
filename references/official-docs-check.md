# Official Docs Check

## Metadata

- Layer: core
- Load level: metadata, summary, full
- Use when: platform, framework, SDK, system API, host integration, control template, ORM, or official design-guideline constraints may govern the implementation.
- Risk tags: `official_docs_required`, `platform_api`, `framework_lifecycle`, `threading_model`, `sdk_usage`, `control_template`, `host_compatibility`, `deprecated_api`, `platform_design`, `native_ui_guideline`

## Summary

Before impact analysis, confirm the official platform or framework constraints that define how the implementation is allowed to behave. CodeGraph explains how the project is currently written. Official Docs Check explains what the platform or framework officially requires.

When available, prefer Context7 or an equivalent official-docs MCP to pull the exact version-scoped official guidance into the workflow quickly. For high-risk constraints, treat that as the fast entry point, not as the final authority source.

## Full Rule

### Relationship To Other Stages

Treat these stages differently:

- Project understanding: understand the current code structure and entry points.
- Official Docs Check: confirm the official platform, framework, SDK, host, or design constraints that govern the implementation.
- Impact analysis: judge what this specific change could affect.
- Task Contract: freeze what this task is allowed to change and how it will be accepted.

Do not begin impact analysis when official docs check is required but missing.

### Context7 Positioning

Treat official-docs work as a layered source model:

| Level | Name | Source | Typical use |
|---|---|---|---|
| **L1** | scoped summary | Context7 or equivalent MCP | default for `S0`–`S2` platform touch when dispute is low — enough to enter impact analysis and freeze Task Contract |
| **L2** | original verification | official docs or API reference | required for `S3+`, deprecated APIs, permission/auth, installer/service/registry, security, migration, or repeated failed repairs |
| **L3** | human confirmation | L2 plus explicit human sign-off | required for `STRICT` **and** release or go-live work |

Routing picks the **deepest required level** for the task. Do not skip a level because L1 was convenient.

Legacy two-layer shorthand still applies inside each level:

1. Context7 or equivalent MCP: fast, version-scoped retrieval
2. Original official docs or API reference: authority verification at L2+

CodeGraph explains project facts. Official docs layers explain platform facts.

Do not let Context7 replace project understanding, TDD, review, or project rules.

### Trigger Conditions

Default to required when the task involves any of these:

1. using or modifying a platform API
2. using or modifying system capabilities
3. using or modifying control templates, lifecycle behavior, or threading models
4. modifying permissions, filesystems, registry, services, installers, or startup behavior
5. modifying Office, WPS, browser, mobile, desktop-plugin, or host-integration behavior
6. using or modifying a third-party SDK, AI SDK, ORM, or UI framework
7. repeated failed bug-fix attempts
8. compatibility-sensitive work
9. performance-sensitive work on framework or platform paths
10. platform behavior that does not match expectations
11. refactoring platform-related code
12. using an unfamiliar or uncertain API
13. UI tasks that should follow target-platform design guidelines
14. using or modifying a UI component library or official design system
15. the task may depend on version-specific framework or SDK behavior

### Usually Skip Conditions

Usually skip only when the task is clearly one of these:

1. documentation-only work
2. a tiny local text or copy tweak
3. pure business-logic changes that do not touch platform, framework, SDK, UI-host, or system constraints
4. pure consultation with no code or behavior change

### Required Sources

Prefer these sources in order:

1. Context7 MCP or an equivalent official-docs ingestion tool, when available
2. official documentation
3. official API reference
4. official samples
5. official design guidelines
6. official migration guides
7. official compatibility notes
8. official known issues or limitations
9. official deprecated API or breaking-change notes

Load these sources progressively. Start from the exact platform, API, control, SDK, host, or design surface identified by project understanding. Do not query broad official documentation packs or unrelated platform areas just because the task is platform-sensitive.

### Context7 Availability And Repair Flow

When Context7 or an equivalent official-docs MCP is expected, check these things in order:

1. whether the MCP server is installed or enabled for the active host
2. whether the required URL, headers, environment variables, or secrets are configured
3. whether the server can connect and answer a narrow library, version, or surface lookup
4. whether library resolution matched the exact dependency, framework, SDK, or version that the task depends on

Distinguish these failure modes explicitly when known:

1. not installed or not enabled
2. installed but not configured
3. configured but missing auth, headers, or secrets
4. configured but unreachable, timing out, or failing initialization
5. reachable but matched the wrong library or wrong version
6. reachable but returned incomplete evidence for the required surface

Do not collapse all of these into a generic "Context7 unavailable" statement.

If the current task is specifically to install, configure, debug, or verify Context7 or MCP tooling itself, treat the tooling problem as the primary task. Do not route that task into ordinary docs fallback.

For ordinary implementation work where Context7 is only a dependency, use this repair-first order before fallback:

1. inspect host-local MCP registration or enablement state
2. inspect the required URL, header, env, or secret wiring
3. retry one narrow library-resolution or docs query after a scoped repair or clarification
4. if the retry still fails or still cannot confirm the exact library or version, record the concrete failure mode and continue with fallback sources

Do not make durable user-level config changes silently during an ordinary coding task unless the user explicitly asked to install or fix the MCP setup, or the current environment clearly delegates that setup work to the agent.

#### Codex Host Repair Steps

When the active host is Codex, prefer this concrete order:

1. inspect `~/.codex/config.toml` or trusted project-scoped `.codex/config.toml` for the expected `mcp_servers.context7` entry
2. verify the configured `url`, header mode, and required environment variable or secret wiring
3. use `codex mcp list` or `codex mcp get context7` to confirm Codex sees the server as enabled
4. if auth is OAuth-based, use `codex mcp login`; if the server uses static headers or env-backed headers, verify those inputs instead of attempting OAuth blindly
5. after config or env changes, prefer a new Codex thread or app restart before declaring the server still broken
6. do one narrow Codex-mediated MCP self-test, such as a library-resolution query for the exact framework or SDK surface the task needs

Do not treat "present in config" as equivalent to "usable in the current Codex session."

#### Cursor Host Repair Steps

When the active host is Cursor, prefer this concrete order:

1. inspect both project-scoped `.cursor/mcp.json` and global `~/.cursor/mcp.json`, and determine which scope should own the server
2. verify the configured `url`, header interpolation, env variables, and whether duplicate server names across scopes could cause confusion
3. inspect `Settings -> Features -> Model Context Protocol` to confirm the server is enabled in the active workspace
4. inspect `Output -> MCP Logs` or the current Cursor log bundle for initialization, auth, and connectivity errors before falling back
5. after config or env changes, restart Cursor or reopen the active window before declaring the server still broken
6. do one narrow Cursor-mediated MCP self-test, such as a library-resolution query for the exact framework or SDK surface the task needs, or verify a successful connection plus a successful tool call in logs

Do not treat "the JSON file parses" as equivalent to "Cursor connected and can answer the required query."

For ordinary platform work, an L1 Context7-backed summary may be enough if the library, version, and relevant surface are clear.

For L2 work, do not stop at Context7. Verify the original official docs or API reference directly before freezing the Task Contract.

For L3 work, record an explicit human confirmation point in routing output and do not treat release execution as unblocked until that confirmation is satisfied.

### Official Docs Depth Selection

Default mapping:

- **L1** — platform-sensitive `FAST` / `STANDARD` tasks with no L2 trigger below
- **L2** — any mandatory original-source trigger, or complexity `S3+`
- **L3** — execution mode `STRICT` **and** task family includes release or go-live

L2 triggers (any one forces L2 minimum):

1. complexity `S3+`
2. deprecated API or breaking-change dependency
3. permission, auth, privacy, or security-sensitive platform behavior
4. installer, service, registry, or startup integration
5. repeated failed bug-fix attempts on platform behavior
6. Context7 incomplete, version-ambiguous, or conflicting with observed behavior

### Task Contract Official Constraint Discipline

When official docs constrain execution, `Task Contract Summary` carries **one line only**:

```md
- Official constraint: {single binding rule}
```

Examples: `UI work must stay on UI thread`, `Installer must not write HKLM without elevation`, `API X deprecated; use Y before vNext`.

Do not paste excerpts, multi-bullet official lists, or long API notes into TCS. Keep detailed citations in internal `Official Docs Check Summary`; surface outward through `Risk Note` only when the constraint blocks or reshapes the slice.

### Mandatory Original-Source Verification

Direct original official-doc verification is required when any of these are true:

1. the task affects security, auth, permissions, payments, or privacy-sensitive behavior
2. the task affects data migration, destructive compatibility behavior, or breaking changes
3. the task affects lifecycle, threading, dispatcher, async, teardown, or resource-release behavior
4. the task affects platform compatibility, host integration, installers, services, or system APIs
5. the task depends on known limitations, deprecated APIs, or breaking-change notes
6. the same bug has already failed multiple repair attempts
7. Context7 results are incomplete, version-ambiguous, or appear to match the wrong library
8. Context7 results conflict with project behavior, test results, or observed platform behavior

### Required Questions

Official docs check must answer:

1. which platform, framework, SDK, host, or UI system is involved
2. which lifecycle requirements matter
3. which threading-model requirements matter
4. which permission or security requirements matter
5. which resource-loading or configuration requirements matter
6. which control-template or named-part requirements matter
7. which compatibility or host constraints matter
8. which performance guidance matters
9. which deprecated APIs or breaking changes matter
10. which official design guidelines matter for UI-facing work
11. which constraints must enter the Task Contract
12. which tests or manual checks must prove compliance
13. whether Context7 matched the exact library, version, and surface
14. whether original official docs or API reference must be verified because the risk is high
15. whether official guidance conflicts with project behavior, tests, or observed runtime behavior

### UI Design Priority

For UI design, UI implementation, component implementation, interaction changes, layout, navigation, dialog, state-feedback, icon, motion, or accessibility work, confirm the target platform's official design guidelines by default.

Do not drift away from platform design conventions without an explicit reason.

Allowed reasons for deviation include:

1. the project already uses a deliberate cross-platform design system
2. the project already has a mature UI style guide
3. the product needs a strong branded or creative visual identity
4. default platform controls cannot satisfy the product experience
5. the UI must work across multiple hosts
6. the user explicitly asked for a specific visual style

When deviation is allowed, explain:

1. what is being deviated from
2. why the deviation is needed
3. what replacement basis is used instead
4. whether accessibility is affected
5. whether platform consistency is affected
6. whether extra UI review is required

### Bug-Fix Counter-Proof

If a bug touches platform behavior, control behavior, system APIs, SDK calls, or host integration, root-cause analysis must include the counter-proof question: "Does the current implementation violate official platform or framework requirements?"

Check:

1. wrong lifecycle usage
2. wrong threading-model usage
3. wrong async, dispatcher, or UI-thread usage
4. wrong resource-loading mechanism
5. wrong control-template or required-part usage
6. deprecated API usage
7. missing permission or compatibility requirements
8. known platform limitations that already explain the symptom

### Fallback Rule

Use fallback only after the availability and repair flow above has either:

1. proved that Context7 is not available in the current host
2. proved that Context7 is misconfigured and not safely repairable inside the current task scope
3. proved that Context7 can connect but still cannot confirm the exact library, version, or required surface after one scoped retry

If official sources are unavailable, say exactly:

`无法访问官方资料，已使用项目现有实现、源码注释、测试和稳定实践作为降级依据。`

If Context7 is unavailable or cannot confirm the relevant library or version, fall back in this order:

1. project-linked official docs
2. README or SDK comments
3. local documentation
4. already stable implementation in the project
5. manual note that official guidance is not fully confirmed

When fallback is used, mark the result as `ALLOW_WITH_WARNINGS` or `BLOCKED` based on risk, and explicitly state `官方规范未完全确认`.

Do not pretend the fallback is equivalent to confirmed official guidance.
Do not hide whether fallback happened because Context7 was missing, misconfigured, auth-incomplete, unreachable, or version-ambiguous.

### Output Depth

#### Summary

Use `Official Docs Check Summary` from `references/report-templates.md` as the internal record shape.

Keep this internal by default when the check is required. Emit it outward only when official guidance materially constrains the Task Contract, changes the implementation direction, blocks work, creates an anomaly, or cannot fit in `Risk Note` or `Exception Note`.

#### Focused Expansion

Use `Official Docs Check Summary` plus `Official Docs Focused Expansion`.

Default to this when only the risky official constraints need outward explanation.

#### Full

Use `Official Docs Check Report` from `references/report-templates.md`.

Use this only when one of these is true:

1. the user explicitly asks for detailed, verbose, debug, or audit output
2. the task is a formal evidence-capture or forward-testing pass that explicitly requires the canonical full template

### Output Discipline

- Default outward output should still stay minimal.
- Do not dump long official excerpts into normal-task output.
- Do not load or summarize unrelated official docs. Keep the check scoped to the surfaces that can actually constrain this task.
- In default outward output, do not emit a separate `Official Docs Check Summary` block unless the routed disclosure trigger requires it; keep the official-docs record internal.
- Surface official-docs findings outward only when risk, anomaly, or explicit detailed mode requires it.
- Except for headings, labels, keywords, paths, and code identifiers, write outward report prose in Chinese.
