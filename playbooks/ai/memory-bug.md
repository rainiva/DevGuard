# AI Memory Bug Playbook

## Metadata

- Issue class: AI memory retrieval, persistence, contamination, or stale-context defect
- Load level: metadata, summary, full

## Summary

Use when an AI feature appears to recall, store, omit, or leak memory incorrectly.

## Full Rule

Check:

1. memory write trigger
2. memory retrieval query
3. freshness and scope
4. privacy boundaries
5. stale or contradictory memory handling
6. regression prompt that proves the memory behavior
