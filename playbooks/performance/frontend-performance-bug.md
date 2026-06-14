# Frontend Performance Bug Playbook

## Metadata

- Issue class: frontend latency, render, list, animation, or interaction performance defect
- Load level: metadata, summary, full

## Summary

Use when a user-visible UI performance issue has a concrete reproduction or clear hot path.

## Full Rule

Check:

1. route or component where slowness appears
2. list size, render count, and expensive effects
3. network or data-fetch contribution
4. layout shift or animation cost
5. measurement before and after the fix
