# Changelog

All notable changes to DevGuard will be documented in this file.

## v0.3.0 - 2026-06-19

### Changed (P7)

- **Three-phase workflow**: Orient → Prepare → Act (`references/control-plane-core.md`)
- **Single entry**: SKILL.md authoritative; README trimmed to install + phase diagram
- **Single lookup**: `references/devguard-lookup.md` replaces scattered runtime tables
- **Module registry**: `references/devguard-module-registry.md`; 12 wrapper skills stubbed (3 thin wrappers kept)
- **T3 externalized**: `references/report-templates-detailed.md`; main `report-templates.md` ≤280 lines
- **Scripts**: `validate_outward_packet.py`, `sync_devguard_install.py`, `simulate_scenarios.py` in CI
- **Benchmark**: 18 development + 3 held-out scenarios (+socratic, lite-skip, three-phase, prepare-blocked)

### Validation

- `check_devguard_bundle.py`, `run_skillopt_judge.py --dataset all`, `simulate_scenarios.py` — all pass
- Fresh-agent benchmark: **21/21** (2026-06-19); see `docs/REFINEMENT_BASELINE.md`

## v0.2.1 - 2026-06-19

### Added

- **Socratic inquiry** module (`skills/05-socratic-inquiry`, `references/socratic-inquiry-core.md`)
- Smart gate: auto-trigger when Task Profile is ambiguous; skip for `LITE` execute whitelist matches
- `Inquiry Note` template and `INQUIRY` execution status
- Chain integration: `socratic-inquiry?` before project understanding on default feature, UI, bugfix, and refactor chains

## v0.2.0 - 2026-06-19

### Added

- **`LITE` execution mode** for daily micro-edits: Micro Slice in `Execution Summary`, no separate TCS, `route:lite-daily`, `/devguard lite` trigger
- Refinement execution plan and baseline docs (`docs/REFINEMENT_PLAN.md`, `docs/REFINEMENT_BASELINE.md`)
- Skillopt regression datasets (12 benchmark + 3 held-out) and bundle-integrated validation
- Output Tier Model (T1 / T1b / T2 / T3) with `Completion Summary` and `Review Summary`
- Primary (12) and Secondary risk tags, Gate Matrix, and eight Named Routes
- P0 / P1 / P2 layered blocking conditions
- Unified Minimum Change Constraint and bug-fix Evidence Gate (six items + red line)
- Coexistence Rules for domain-skill pairing and `/devguard fast|strict|review` short triggers
- CodeGraph No-Index Fallback (`codegraph_unavailable`, limited read, `ALLOW_WITHOUT_CODEGRAPH`)
- Official Docs depth levels L1 / L2 / L3 and one-line `Official constraint` in Task Contract Summary
- `references/glossary.md` core terminology index

### Changed

- `SKILL.md` and `README.md` trimmed and re-indexed; `shared/` paths redirect to `references/`
- Default outward output remains `Execution Summary` + `Task Contract Summary`; stage summaries internal by default
- `agents/openai.yaml` default prompt shortened to <= 120 characters
- Four high-frequency core references use Metadata / Summary / Full Rule structure
- Dynamic reroute trigger table and outward ES-only update on reroute

### Validation

- Run `python scripts/check_devguard_bundle.py --skill-dir .`
- Run `python scripts/run_skillopt_judge.py --skill-dir . --dataset all`

## v0.1.0 - 2026-06-14

### Added

- Initial public DevGuard skill bundle
- Progressive rule-loading with summary-first disclosure
- CodeGraph-first project understanding and official docs check stages
- Tiered Impact Analysis and Task Contract outputs
- TDD, review, performance, migration, AI/LLM, and release-check lanes
- Sample playbooks, sample project rules, helper scripts, and forward-testing references
- MIT license, GitHub issue forms, PR template, and release metadata support
