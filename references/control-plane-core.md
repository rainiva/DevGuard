# DevGuard Control Plane

Authoritative three-phase workflow. Entry: SKILL.md. Lookup: devguard-lookup.md.

## Three Phases

Orient -> Prepare -> Act

| Phase | Default outward | Sub-gates |
|---|---|---|
| Orient | ES + TCS (FAST+); LITE ES+Slice; inquiry ES+Inquiry Note | route, Socratic?, load plan |
| Prepare | silent (in TCS) | PU, docs?, IA, Contract |
| Act | Completion / Review Summary | TDD, domain, review |

## Orient

Route (task-routing.md), Socratic? (socratic-inquiry-core.md), rule load (rule-loading.md), emit report-templates.md.

Exit: ALLOW/ALLOW_WITH_WARNINGS + valid packet; or INQUIRY; or BLOCKED.

## Prepare

PU -> official-docs? -> IA -> Task Contract freeze. bug-fix(diagnosis-only) inside Prepare when chain requires.

Exit: Contract frozen; validate_outward_packet.py pass for FAST+.

## Act

TDD Red -> domain core -> review -> Completion Summary.

## Reroute

Facts change -> back to Orient; update ES Mode/Rules/Status/Next only. See dynamic-reroute-core.md.