---
name: devguard
description: Route, gate, Contract. Use for LITE micro edits; FAST+ for bugfix/UI. Not for unscoped work.
---

# DevGuard

Orchestration: route and gate; domain skills execute inside frozen Contract.

## Default Workflow

**Orient -> Prepare -> Act** — [control-plane-core.md](references/control-plane-core.md)

| Phase | Outward |
|---|---|
| Orient | Execution Summary + Task Contract Summary; LITE: ES+Slice; inquiry: Inquiry Note |
| Prepare | silent; validate before Act |
| Act | Completion / Review Summary |

Lookup: [devguard-lookup.md](references/devguard-lookup.md). Modules: [devguard-module-registry.md](references/devguard-module-registry.md).

## Coexistence Rules

1. **DevGuard owns** routing, gates, Task Contract freeze, and rule loading.
2. **Domain skills own** concrete execution inside the frozen Contract.
3. **On conflict**, DevGuard gates win.
4. **Do not duplicate** domain TDD/debug detail in DevGuard output.
5. **When the user names a domain skill explicitly**, DevGuard limits itself to routing + Contract.

## Operating Rules

- Default outward packet: `Execution Summary` + `Task Contract Summary` for FAST+.
- **Hard default-output cap**: do not emit `Project Understanding Summary`, `Impact Analysis Summary`, or `Official Docs Check Summary` as separate outward blocks.
- Render **standalone record blocks**; conversation outside blocks.
- require at least one test, reproduction, or acceptance check that exercises the real user operation path
- Do not treat internal function, method, interface, or ideal-path-only checks as sufficient evidence for UI completion.
- no repair code without a failing test or reproduction
- **Minimum Change Constraint**: simplest correct diff inside frozen Task Contract scope
- `--format rule-summary` for explicit rule-loading disclosure

## Helper Scripts

```bash
python scripts/generate_rule_loading_manifest.py --format summary ...
python scripts/validate_outward_packet.py --self-test
python scripts/check_devguard_bundle.py
```