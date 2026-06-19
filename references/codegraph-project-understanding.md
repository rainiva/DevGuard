# CodeGraph Project Understanding

## Metadata

- Layer: core
- Load level: metadata, summary, full
- Use when: any code-modifying task needs structural understanding before impact analysis.
- Risk tags: `codegraph_required`, `project_understanding`, `call_graph`, `symbol_reference`

## Summary

Before impact analysis, use structural project-understanding tools to learn what the project currently looks like. Prefer CodeGraph first, repair or retry it before demoting it, then try other structural tools in priority order, and only then fall back to plain search-based understanding.

## Full Rule

### Preferred Tool Order

Use tools in this order when available:

1. CodeGraph tools such as `codegraph_context`, `codegraph_search`, `codegraph_explore`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files`, and `codegraph_status`
2. Persisted project-graph tools such as `Understand-anything`
3. Other graph or symbol-index tools such as `graphify`, language-server symbol search, or reference search
4. Fallback structure discovery with file-tree analysis, symbol search, caller search, reference search, test search, and document search

If CodeGraph is unavailable, but another structural tool exists, use that before plain text search.

If no structural tool is available, say exactly:

`CodeGraph 不可用，已使用降级项目理解方式。`

### Tool Availability And Repair Flow

When structural project-understanding tooling is expected, check these things in order:

1. whether CodeGraph is installed or enabled for the active host and workspace
2. whether the current project root matches the root that CodeGraph or the secondary graph tool expects
3. whether CodeGraph can report healthy status for the current project and answer one narrow structural query
4. whether the next structural tool in priority order is installed, configured, and pointed at the same project root
5. whether a persisted graph or index artifact exists and is fresh enough for the requested task

### CodeGraph Freshness Gate

Before trusting any CodeGraph answer for implementation work, pass this freshness gate:

1. verify the active repository root matches the root that CodeGraph indexed
2. run `codegraph_status` for that root
3. if the project is not initialized, use the documented `codegraph init -i` path before any structural query
4. if the status is unhealthy, stale, incomplete, or otherwise not trustworthy, use the documented host or CLI refresh, rebuild, or reinitialization path before any structural query
5. after refresh or rebuild, rerun `codegraph_status`
6. after status is healthy, run one narrow structural self-test for the exact entry point, symbol, caller, or context the task needs

Do not treat a stale or incomplete index as good enough just because CodeGraph still returns some results.
Do not query broad structural surfaces from a known-stale index and only repair it later.

If the current turn just changed repository files, allow the watcher or indexer to settle before declaring the index stale. If the status still remains stale or incomplete after that settling window, use the documented refresh or rebuild path.

Distinguish these failure modes explicitly when known:

1. CodeGraph not installed or not enabled
2. CodeGraph installed but not initialized for the current project
3. CodeGraph enabled but disconnected from the current host session or workspace
4. CodeGraph connected but pointing at the wrong project root, subdirectory, or worktree
5. CodeGraph connected but index status is unhealthy, stale, or incomplete
6. secondary structural tool installed but its graph or index artifact is missing
7. secondary structural tool graph exists but is stale, incomplete, unreadable, or built for the wrong root
8. secondary structural tool plugin root, runtime, or build dependencies are missing
9. all structural tooling unavailable, misconfigured, or insufficient for the requested surface

If the current task is specifically to install, configure, debug, or verify CodeGraph, Understand-anything, graphify, or related structural tooling, treat that tooling problem as the primary task. Do not route it into ordinary project-understanding fallback.

For ordinary implementation work where project understanding is only a dependency, use this repair-first order before fallback:

1. inspect CodeGraph registration, enablement, and project-root alignment for the active host
2. run the CodeGraph freshness gate and retry one narrow structural query only after freshness is restored
3. if CodeGraph still cannot answer, inspect the next structural tool in priority order for install, artifact, and freshness problems
4. retry the original structural question with the repaired secondary tool
5. only if all higher-priority structural tools still fail should you record the concrete failure mode and continue with search-based fallback

Do not treat "a command exists", "a config entry exists", or "a graph file exists somewhere on disk" as equivalent to "the current project can be understood structurally in this session."

#### Codex Host Repair Steps

When the active host is Codex, prefer this concrete order:

1. inspect `~/.codex/config.toml` or trusted project-scoped `.codex` config for the expected CodeGraph MCP registration
2. use `codex mcp list` or `codex mcp get codegraph` to confirm Codex sees the server as enabled for the current session
3. if the current working tree is a subdirectory or worktree, verify that CodeGraph was initialized for the intended repository root rather than the wrong nested path
4. run `codegraph_status` for the current project root, and if the project is not initialized, use the documented `codegraph init -i` path before declaring CodeGraph unavailable
5. if status is unhealthy, stale, or incomplete, use the documented refresh, rebuild, or reinitialization path for the installed CodeGraph setup before trusting any structural query
6. after config, registration, initialization, or refresh changes, prefer a new Codex thread or app restart when the host requires it before declaring CodeGraph still broken
7. do one narrow Codex-mediated self-test, such as a focused symbol, caller, or context query for the exact entry point the task needs

Do not treat "present in Codex config" as equivalent to "usable for the current project-understanding task."

#### Cursor Host Repair Steps

When the active host is Cursor, prefer this concrete order:

1. inspect both project-scoped `.cursor/mcp.json` and global `~/.cursor/mcp.json`, and determine which scope should own the CodeGraph server
2. verify the configured command or transport, working directory expectations, and whether duplicate server names across scopes could shadow each other
3. inspect `Settings -> Features -> Model Context Protocol` to confirm the server is enabled in the active workspace
4. inspect `Output -> MCP Logs` or the current Cursor log bundle for initialization, connectivity, or workspace-root errors before falling back
5. run the CodeGraph status or initialization flow for the active workspace root, and if status is stale, unhealthy, or incomplete, use the documented refresh, rebuild, or reinitialization path for that setup before trusting any structural query
6. restart Cursor or reopen the active window after config or index-refresh changes when required before declaring the server still broken
7. do one narrow Cursor-mediated self-test, such as a focused symbol, caller, or context query for the exact entry point the task needs

Do not treat "the JSON file parses" as equivalent to "Cursor connected to the right CodeGraph instance for the current workspace."

#### Secondary Structural Tool Repair Notes

When CodeGraph is unavailable or insufficient, repair lower-priority structural tools before falling straight to grep:

1. For `Understand-anything`, confirm the plugin root can be resolved, confirm `.understand-anything/knowledge-graph.json` exists for the current project root, check for worktree or redirected-root mismatches, and if the graph is missing but the plugin is present, prefer running `/understand` or the equivalent graph-build flow before saying the tool is unavailable.
2. For `Understand-anything`, if the graph exists, verify that it is fresh enough for the requested entry points, changed files, or architectural surface before trusting it.
3. For `graphify` or equivalent graph or index tools, confirm the command or plugin exists, confirm the graph or index artifact exists for the current project, and rebuild or refresh it if the current workflow depends on up-to-date structure.
4. For all secondary tools, retry one narrow structural question after the repair.
5. If the repair fails, record whether the issue was install, config, runtime, artifact, staleness, or project-root mismatch before falling back.

### Freshness Decision Rule

Use this decision rule when CodeGraph answers but freshness is still in doubt:

1. if `codegraph_status` is healthy and a narrow self-test matches the requested surface, continue
2. if status is stale, unhealthy, incomplete, or points at the wrong root, refresh or rebuild first
3. if the host exposes no safe refresh path inside the current task scope, record the freshness failure mode and use the next structural tool or search fallback
4. if the task is high-risk and no fresh structural index can be restored, prefer `ALLOW_WITH_WARNINGS` or `BLOCKED` over pretending the structural evidence is current

### No-Index Fallback

When `codegraph_status` is unavailable, the project is not initialized, or CodeGraph cannot be repaired inside the current task scope after the repair-first flow, record tool state as **`codegraph_unavailable`** and apply complexity-based fallback.

| Complexity | Required action | Typical status |
|---|---|---|
| `S1` | **limited read** — read task-identified entry files, direct imports, and bounded grep or reference search only | `ALLOW_WITH_WARNINGS` when local uncertainty stays narrow |
| `S2+` | run documented `codegraph init -i` or host refresh first; if still unavailable, use the next structural tool or explicit `ALLOW_WITHOUT_CODEGRAPH` with narrowed Contract | `ALLOW_WITHOUT_CODEGRAPH` or `BLOCKED` on `S3+` without any structural evidence |

**Limited read rules (`S1`):**

1. read only entry files already named by the task or discovered from one hop of direct imports
2. use bounded grep, reference search, or symbol search — no whole-repo speculative trawls
3. do not treat limited read as equivalent to CodeGraph call-chain proof
4. narrow Task Contract `Scope` to the surfaces actually verified

**`S2+` without CodeGraph:**

1. attempt init or refresh before declaring unavailable
2. if a secondary structural tool can answer the narrow question, use it and record that path
3. if neither CodeGraph nor a secondary tool can restore structural evidence, set status to `ALLOW_WITHOUT_CODEGRAPH` only when the Contract is explicitly narrowed and risk is disclosed
4. for `S3+` or `STRICT` work with no structural path and no safe narrow slice, prefer `BLOCKED`

**Default outward line** when fallback is active — put it in `Execution Summary` field `Structural tool` (or `Risk Note` if ES has no room):

`Structural tool: CodeGraph unavailable, fallback: limited read`

Allowed variants:

- `Structural tool: CodeGraph unavailable, fallback: secondary structural tool`
- `Structural tool: CodeGraph unavailable, fallback: ALLOW_WITHOUT_CODEGRAPH`

Omit the line when CodeGraph or another accepted structural tool is healthy and in use.

### Trigger Conditions

Default to required when the task involves any of these:

1. bug fixes
2. new feature development
3. modifying existing behavior
4. refactor or migration work
5. API or contract changes
6. state-machine or store changes
7. permission-related changes
8. UI work spanning multiple pages or global styles
9. performance problems
10. entry uniqueness checks
11. unclear entry points
12. expected changes across more than one or two files
13. repeated failed repairs
14. large or structurally complex projects

### Usually Skip Conditions

Usually skip only when the task is clearly one of these:

1. documentation-only work
2. a tiny text tweak inside one already-known file
3. a user-specified single-line or single-location change with no structural uncertainty
4. pure consultation with no code changes

### Required Questions

Project understanding must answer:

1. where the related entry points are
2. what the relevant call chain is
3. whether similar implementations already exist
4. whether multiple entry points or duplicate implementations exist
5. which modules and files are involved
6. which files are directly affected
7. which files are indirectly affected
8. which shared modules or global styles may be affected
9. which tests need to be added, updated, or rerun
10. which surfaces should not be modified

### Required Findings

Look for these structural risks when relevant:

1. multiple entry points
2. duplicate implementations
3. incomplete call-chain understanding
4. circular dependencies
5. over-centralized modules
6. global state pollution
7. global style pollution
8. stale or legacy entry points
9. missing tests
10. performance hot spots
11. permission bypass paths

### Output Depth

Keep internal project understanding rigorous enough for the task, but default outward disclosure to the smallest safe shape.

#### Summary

Use `Project Understanding Summary` from `references/report-templates.md` as the internal record shape.

Keep this internal by default for ordinary `FAST` and `STANDARD` work. Emit it outward only when structural facts create a blocker, anomaly, reroute trigger, implementation-changing risk, or risk that cannot fit in `Risk Note` or `Exception Note`.

Keep it lightweight:

1. locate the related files
2. locate key entry points or references
3. find similar implementations
4. note the main risks

#### Focused Expansion

Use `Project Understanding Summary` plus `Project Understanding Focused Expansion`.

Default to this for high-risk, blocker, anomaly, or reroute cases when only the risky structural surfaces need more detail.

#### Full

Use full `CodeGraph Project Understanding Report` from `references/report-templates.md`.

Use this only when one of these is true:

1. the user explicitly asks for detailed, verbose, debug, or audit output
2. the task is a formal evidence-capture or forward-testing pass that explicitly requires the canonical full template

High-risk or anomaly status alone does not force the full template if focused expansion is enough.

Include:

1. related entry points
2. call chain
3. similar implementations
4. impact scope
5. test impact
6. risk points
7. tooling state and repair or fallback record
8. conclusion about whether impact analysis may begin

#### Strict Additions

Use full `CodeGraph Project Understanding Report` plus `Strict Project Understanding Additions`.

Also inspect:

1. reverse dependencies
2. shared-module and global-style surfaces
3. permission and state paths
4. performance hot paths
5. rollback-sensitive surfaces

### Output Discipline

- Do not guess entry points when structural evidence can still be gathered.
- Do not jump into impact analysis before project understanding is complete when this stage is required.
- Do not trust CodeGraph results until the freshness gate has passed.
- Do not silently demote from CodeGraph to lower-priority structural tools or plain search when a repairable host, index, or root-alignment problem still exists.
- In summary mode, name only the key entry points, similar implementations, and risks. Do not spill the full call chain unless expanded output is required.
- In default outward output, do not emit a separate `Project Understanding Summary` block unless the routed disclosure trigger requires it; keep the project-understanding record internal.
- In focused-expansion mode, deepen only the risky entry points, shared surfaces, or call-chain segments that justify the extra disclosure.
- Except for headings, labels, keywords, paths, and code identifiers, write the report prose in Chinese.
- If the fallback path was used, say so explicitly in the report.

### Relationship To Later Stages

Treat these stages differently:

- Project understanding: structural fact finding about what the project is now.
- Official docs check: official platform, framework, SDK, host, or design constraints that govern what the code is allowed to do.
- Impact analysis: change-oriented judgment about what this task could affect.
- Task Contract: execution freeze about what this task is allowed to do and how it will be accepted.

Do not generate a Task Contract before required project understanding, required official docs check, and impact analysis are complete.
