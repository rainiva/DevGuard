# CodeGraph Project Understanding

## Metadata

- Layer: core
- Load level: metadata, summary, full
- Use when: any code-modifying task needs structural understanding before impact analysis.
- Risk tags: `codegraph_required`, `project_understanding`, `call_graph`, `symbol_reference`

## Summary

Before impact analysis, use structural project-understanding tools to learn what the project currently looks like. Prefer CodeGraph first, then other symbol or call-graph tools, and only then fall back to plain search-based understanding.

## Full Rule

### Preferred Tool Order

Use tools in this order when available:

1. CodeGraph tools such as `codegraph_context`, `codegraph_search`, `codegraph_explore`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files`, and `codegraph_status`
2. Other graph or symbol-index tools such as `Understand-anything`, `graphify`, language-server symbol search, or reference search
3. Fallback structure discovery with file-tree analysis, symbol search, caller search, reference search, test search, and document search

If CodeGraph is unavailable, but another structural tool exists, use that before plain text search.

If no structural tool is available, say exactly:

`CodeGraph 不可用，已使用降级项目理解方式。`

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

Use `Project Understanding Summary` from `references/report-templates.md`.

Default to this for ordinary `FAST` and `STANDARD` work.

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
7. conclusion about whether impact analysis may begin

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
- In summary mode, name only the key entry points, similar implementations, and risks. Do not spill the full call chain unless expanded output is required.
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
