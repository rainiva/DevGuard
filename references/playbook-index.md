# Playbook Index

## Metadata

- Layer: playbook-index
- Load level: metadata, summary, full
- Use when: a concrete bug or review task may need a focused playbook.

## Summary

Use this index to decide whether a concrete playbook exists before saying one is missing.

## Full Rule

Load only the playbook that matches the concrete issue class.

All playbook paths are relative to the DevGuard skill root. Before reporting a playbook as missing, check the resolved path under the skill root. If the file exists, list it as a needed or loaded playbook, not as a missing rule.

| Issue class | Trigger | Playbook |
|---|---|---|
| WPF UI bug | WPF rendering, layout, resource, theme, binding, or visual-tree defect | `playbooks/ui/wpf-ui-bug.md` |
| WPF scrollbar bug | WPF scrollbar missing, hidden, template, thumb, track, extent, or `ScrollViewer` behavior | `playbooks/ui/wpf-scrollbar-bug.md` |
| API contract bug | request or response shape mismatch, undocumented contract change, producer-consumer break | `playbooks/backend/api-contract-bug.md` |
| Frontend performance bug | visible latency, list rendering, animation, interaction, or render-count issue | `playbooks/performance/frontend-performance-bug.md` |
| AI memory bug | stale, missing, leaked, contaminated, or wrongly scoped AI memory behavior | `playbooks/ai/memory-bug.md` |

If no concrete playbook matches, say that no matching playbook is available and continue with the relevant core workflow.
