#!/usr/bin/env python3
"""Check DevGuard bundle structure and key disclosure invariants."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


P7_MAX_SKILL_LINES = 65
P7_MAX_REPORT_TEMPLATES_LINES = 280
P7_MAX_LOOKUP_LINES = 200
P7_MAX_ACTIVE_WRAPPER_LINES = 12
P7_ACTIVE_WRAPPER_ALLOWLIST = {
    "skills/00-task-router/SKILL.md",
    "skills/12-codegraph-project-understanding/SKILL.md",
    "skills/15-tdd-workflow/SKILL.md",
}
P7_REQUIRED_FILES = [
    "docs/REFINEMENT_PLAN_P7.md",
    "references/control-plane-core.md",
    "references/devguard-module-registry.md",
    "references/devguard-lookup.md",
    "references/report-templates-detailed.md",
    "scripts/validate_outward_packet.py",
    "scripts/sync_devguard_install.py",
]
P7_SKILL_PHASES = ["Orient", "Prepare", "Act"]
P7_REPORT_TEMPLATE_MAIN_SECTIONS = [
    "## Output Tier Model",
    "## Summary Output Discipline",
    "## Record Block Discipline",
    "## Execution Summary",
    "## Risk Note",
    "## Inquiry Note",
    "## Exception Note",
    "## Completion Summary",
    "## Review Summary",
    "## Task Contract Summary",
]
P7_REPORT_TEMPLATE_DETAILED_SECTIONS = [
    "## Skill Routing Decision",
    "## Rule-Loading Manifest",
    "## CodeGraph Project Understanding Report",
    "## Task Contract",
    "## Development Completion Report",
    "## Review Report",
]

EXPECTED_FILES = [
    "SKILL.md",
    ".gitignore",
    "agents/openai.yaml",
    "references/task-routing.md",
    "references/socratic-inquiry-core.md",
    "references/rule-loading.md",
    "references/rule-disclosure-index.md",
    "references/shared-guardrails.md",
    "references/severity-levels.md",
    "references/report-templates.md",
    "references/codegraph-project-understanding.md",
    "references/official-docs-check.md",
    "references/impact-analysis-core.md",
    "references/compatibility-impact-analysis.md",
    "references/tdd-workflow-core.md",
    "references/daily-development-core.md",
    "references/code-review-core.md",
    "references/official-docs-review-extension.md",
    "references/release-check-core.md",
    "references/ui-implementation-core.md",
    "references/ui-review-extension.md",
    "references/bug-fix-core.md",
    "references/bug-fix-review-extension.md",
    "references/migration-refactor-core.md",
    "references/migration-refactor-review-extension.md",
    "references/ai-llm-feature-core.md",
    "references/ai-llm-review-extension.md",
    "references/performance-impact-core.md",
    "references/performance-review-core.md",
    "references/performance-review-extension.md",
    "references/failure-retrospective-core.md",
    "references/dynamic-reroute-core.md",
    "references/playbook-conventions.md",
    "references/playbook-index.md",
    "references/project-rule-index-conventions.md",
    "references/selective-project-loading.md",
    "references/review-mirroring-rules.md",
    "references/example-prompts.md",
    "references/forward-testing.md",
    "references/glossary.md",
    "references/batch-roadmap.md",
    "scripts/generate_rule_loading_manifest.py",
    "scripts/check_devguard_bundle.py",
    "scripts/gen_skillopt.py",
    "scripts/run_skillopt_judge.py",
    "docs/REFINEMENT_PLAN.md",
    "docs/REFINEMENT_BASELINE.md",
    "skillopt/benchmark.jsonl",
    "skillopt/held-out.jsonl",
    "shared/evidence-rules.md",
    "shared/blocking-rules.md",
    "shared/severity-levels.md",
    "shared/report-templates.md",
    "skills/00-task-router/SKILL.md",
    "skills/05-socratic-inquiry/SKILL.md",
    "skills/10-impact-analysis/SKILL.md",
    "skills/12-codegraph-project-understanding/SKILL.md",
    "skills/13-official-docs-check/SKILL.md",
    "skills/15-tdd-workflow/SKILL.md",
    "skills/20-daily-development/SKILL.md",
    "skills/25-performance-impact-analysis/SKILL.md",
    "skills/30-ui-implementation/SKILL.md",
    "skills/40-bug-fix/SKILL.md",
    "skills/45-failure-retrospective/SKILL.md",
    "skills/50-migration-refactor/SKILL.md",
    "skills/60-ai-llm-feature/SKILL.md",
    "skills/70-release-check/SKILL.md",
    "skills/85-performance-review/SKILL.md",
    "skills/90-code-review/SKILL.md",
    "project-rules/example/index.md",
    "project-rules/example/ui.md",
    "project-rules/example/api.md",
    "project-rules/example/data.md",
    "project-rules/example/review-ui.md",
    "project-rules/example/review-api.md",
    "playbooks/ui/wpf-ui-bug.md",
    "playbooks/ui/wpf-scrollbar-bug.md",
    "playbooks/backend/api-contract-bug.md",
    "playbooks/performance/frontend-performance-bug.md",
    "playbooks/ai/memory-bug.md",
]


DISCLOSURE_INDEX_SECTIONS = ["## Metadata", "## Summary", "## Full Rule", "## Rule Index"]
RULE_LOADING_SECTIONS = [
    "## Rule-Loading Output Modes",
    "### 1. Default Mode: Minimal Summary",
    "### 2. Focused Expansion Mode",
    "### 3. Detailed Mode: Full Manifest",
]
REPORT_TEMPLATE_SECTIONS = [
    "## Output Tier Model",
    "## Summary Output Discipline",
    "## Record Block Discipline",
    "## Execution Summary",
    "## Risk Note",
    "## Inquiry Note",
    "## Exception Note",
    "## Task Contract Summary",
    "## Completion Summary",
    "## Review Summary",
]
SEVERITY_LEVELS_SECTIONS = ["## Metadata", "## Summary", "## Review Verdict Mapping", "## Full Rule"]
CODEGRAPH_UNDERSTANDING_SECTIONS = ["## Metadata", "## Summary", "## Full Rule"]
OFFICIAL_DOCS_SECTIONS = ["## Metadata", "## Summary", "## Full Rule"]
TASK_ROUTING_SECTIONS = [
    "## Primary Risk Tags",
    "## Secondary Risk Tags",
    "## Gate Matrix",
    "## Named Routes",
]
CORE_THREE_PART_SECTIONS = ["## Metadata", "## Summary", "## Full Rule"]
P3_CORE_REFERENCE_FILES = [
    "references/impact-analysis-core.md",
    "references/bug-fix-core.md",
    "references/daily-development-core.md",
    "references/code-review-core.md",
]
PRIMARY_RISK_TAGS = [
    "api_contract",
    "auth_permission",
    "data_consistency",
    "migration",
    "release",
    "security",
    "performance",
    "official_docs_required",
    "codegraph_required",
    "compatibility",
    "ai_output",
    "ux_flow",
]
NAMED_ROUTE_IDS = [
    "route:feature-normal",
    "route:ui-implementation",
    "route:bugfix-standard",
    "route:bugfix-desktop-ui",
    "route:refactor-migration",
    "route:performance-change",
    "route:ai-llm-feature",
    "route:review-only",
    "route:lite-daily",
]
CODEGRAPH_UNDERSTANDING_REQUIRED_PHRASES = [
    "### Tool Availability And Repair Flow",
    "### CodeGraph Freshness Gate",
    "#### Codex Host Repair Steps",
    "#### Cursor Host Repair Steps",
    "### Freshness Decision Rule",
    "#### Secondary Structural Tool Repair Notes",
    "Do not silently demote from CodeGraph",
    "Do not trust CodeGraph results until the freshness gate has passed.",
]
REPORT_TEMPLATE_REQUIRED_PHRASES = [
    "- Tool state:",
    "- Repair / fallback path:",
    "- Primary structural tool:",
]
BUG_FIX_EVIDENCE_REQUIRED_PHRASES = {
    "references/bug-fix-core.md": [
        "No evidence, no repair code",
        "Evidence Gate — Six Required Items",
        "No failing test or reproduction = no bug claim and no repair",
        "does **not** apply to `bugfix` tasks",
        "Do not write repair code without a failing test or reproduction",
    ],
    "references/shared-guardrails.md": [
        "no failing check = no bug claim and no repair",
        "Repair code is written or applied before a failing test or reproduction exists",
    ],
    "references/bug-fix-review-extension.md": [
        "No failing test or reproduction = no accepted bug fix",
        "red-before recorded",
    ],
    "SKILL.md": [
        "no repair code without a failing test or reproduction",
    ],
}
MINIMUM_CHANGE_REQUIRED_PHRASES = {
    "references/shared-guardrails.md": [
        "## Minimum Change Constraint",
        "simplest change that correctly solves the approved slice",
        "No drive-by edits",
        "Forbidden Without Reroute",
    ],
    "SKILL.md": [
        "Minimum Change Constraint",
        "simplest correct diff inside frozen Task Contract scope",
    ],
    "references/daily-development-core.md": [
        "Minimum Change Constraint",
    ],
    "references/tdd-workflow-core.md": [
        "Minimum Change Constraint",
    ],
    "references/code-review-core.md": [
        "Minimum Change Constraint",
    ],
}
P4_MAX_INVOCATION_CHARS = 120
P4_SHORT_TRIGGERS = ["/devguard lite", "/devguard fast", "/devguard strict", "/devguard review"]
P4_COEXISTENCE_PHRASES = [
    "## Coexistence Rules",
    "DevGuard owns",
    "Domain skills own",
    "On conflict",
    "Do not duplicate",
    "When the user names a domain skill explicitly",
]
P5_CODEGRAPH_FALLBACK_PHRASES = [
    "### No-Index Fallback",
    "codegraph_unavailable",
    "fallback: limited read",
    "ALLOW_WITHOUT_CODEGRAPH",
]
P5_OFFICIAL_DOCS_PHRASES = [
    "**L1**",
    "**L2**",
    "**L3**",
    "Task Contract Official Constraint Discipline",
    "Official constraint:",
]
GLOSSARY_MIN_TERMS = 15
GLOSSARY_REQUIRED_TERMS = [
    "Task Profile",
    "Task Contract",
    "Impact Analysis",
    "Execution Summary",
    "Risk Note",
    "Exception Note",
    "Gate Matrix",
    "Named Route",
    "Coexistence Rules",
    "No-Index Fallback",
    "Minimum Change Constraint",
    "LITE",
]
LITE_REQUIRED_PHRASES = {
    "references/task-routing.md": [
        "## LITE Mode",
        "LITE execute whitelist",
        "Micro Slice",
        "route:lite-daily",
        "/devguard lite",
    ],
    "references/report-templates.md": [
        "T1-lite",
        "LITE Execution Summary",
        "LITE Completion Summary",
        "Do not emit `## Task Contract Summary` as a peer block in T1-lite mode",
    ],
    "references/rule-loading.md": [
        "### LITE",
        "Micro Slice inside `Execution Summary` satisfies the Contract freeze",
    ],
    "references/shared-guardrails.md": [
        "### LITE Micro Slice",
    ],
    "references/example-prompts.md": [
        "/devguard lite",
    ],
}
UI_REAL_SCENARIO_REQUIRED_PHRASES = {
    "SKILL.md": [
        "require at least one test, reproduction, or acceptance check that exercises the real user operation path",
        "Do not treat internal function, method, interface, or ideal-path-only checks as sufficient evidence for UI completion.",
    ],
    "references/shared-guardrails.md": [
        "at least one failing check or acceptance check must exercise a real user operation path",
        "Internal function, method, interface, or ideal-path-only checks are not enough on their own.",
        "claimed verified using only internal function, method, interface, or ideal-path checks",
    ],
    "references/tdd-workflow-core.md": [
        "prefer a failing check that exercises the real user path first",
        "does not replace a real UI interaction check",
        "Which real user operation path was exercised",
    ],
    "references/ui-implementation-core.md": [
        "Define at least one verification path that exercises the real user operation flow.",
        "Do not claim UI completion using only internal methods, functions, interfaces, or ideal-path checks",
        "real user operation paths that were verified",
    ],
    "references/forward-testing.md": [
        "requires at least one verification path that exercises real user operations",
        "claims a user-visible UI or interaction-flow task is verified using only internal function, method, interface, or ideal-path checks",
    ],
}
DEFAULT_STAGE_SUMMARY_BLOCKS = [
    "## Project Understanding Summary",
    "## Impact Analysis Summary",
    "## Official Docs Check Summary",
]
DEFAULT_OUTPUT_HARD_CAP_FILES = {
    "SKILL.md": [
        "Hard default-output cap",
        "do not emit `Project Understanding Summary`, `Impact Analysis Summary`, or `Official Docs Check Summary`",
    ],
    "README.md": [
        "`Project Understanding Summary`、`Impact Analysis Summary`、`Official Docs Check Summary` 默认只作为内部记录保留",
    ],
    "references/report-templates.md": [
        "Hard default-output cap",
        "Treat those stage summaries as internal records",
    ],
    "references/rule-loading.md": [
        "Stage summaries are internal records by default",
        "do not emit `Project Understanding Summary`, `Impact Analysis Summary`, or `Official Docs Check Summary`",
    ],
    "references/task-routing.md": [
        "keep `Project Understanding Summary`, `Impact Analysis Summary`, and `Official Docs Check Summary` as internal records",
        "Keep stage summaries internal in default mode",
    ],
    "references/codegraph-project-understanding.md": [
        "CodeGraph Freshness Gate",
        "Keep this internal by default",
        "do not emit a separate `Project Understanding Summary` block",
    ],
    "references/official-docs-check.md": [
        "Keep this internal by default",
        "do not emit a separate `Official Docs Check Summary` block",
    ],
    "references/impact-analysis-core.md": [
        "Keep this internal by default",
        "do not emit a separate `Impact Analysis Summary` block",
    ],
}
FORWARD_TESTING_REQUIRED_PHRASES = [
    "attempts CodeGraph or lower-priority structural-tool repair before search-only fallback",
    "silently demotes from CodeGraph or another repairable structural tool to plain-search fallback",
    "a structural-tool repair-before-fallback case where CodeGraph is missing, uninitialized, or host-disconnected",
    "verify CodeGraph index freshness before structural queries",
    "refreshes or rebuilds a stale index before trusting it",
    "trusts CodeGraph results from a stale, unhealthy, incomplete, or wrong-root index without first repairing or refreshing it",
    "stale-index case where `codegraph_status` is not healthy until refresh or rebuild completes",
    "judge the result by exact block shape",
    "keeps the default outward transcript to the allowed block set",
    "Treat any extra peer block outside the allowed shape as a regression",
    "blocks repair without a failing test or reproduction",
    "Minimum Change Constraint",
    "No-Index Fallback",
    "Official constraint",
    "LITE execute",
]
WRAPPER_DISCLOSURE_REQUIRED_PHRASES = {
    "skills/12-codegraph-project-understanding/SKILL.md": [
        "run the documented freshness gate before trusting any structural answer",
        "Keep that record internal by default",
        "Do not emit a separate `Project Understanding Summary` outward",
    ],
}
ALLOWED_RULE_LAYERS = {
    "meta",
    "pre-execution",
    "execution",
    "extension",
    "project",
    "playbook",
    "review",
    "shared",
}
EXPECTED_SHARED_STUBS = {
    "shared/report-templates.md": "Canonical: [references/report-templates.md]",
    "shared/severity-levels.md": "Canonical: [references/severity-levels.md]",
    "shared/blocking-rules.md": "Canonical: [references/shared-guardrails.md]",
    "shared/evidence-rules.md": "Canonical: [references/shared-guardrails.md]",
}


def normalize_route_target(raw: str) -> str:
    normalized = raw.strip().rstrip("?")
    return re.sub(r"\(.*?\)", "", normalized)


def parse_markdown_table(content: str, section: str) -> list[dict[str, str]]:
    section_match = re.search(
        rf"## {re.escape(section)}\s+(.*?)(?:\n## |\Z)",
        content,
        flags=re.DOTALL,
    )
    if not section_match:
        return []
    rows = []
    headers: list[str] = []
    for line in section_match.group(1).splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r"-+", cell) for cell in cells):
            continue
        if not headers:
            headers = cells
            continue
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def parse_implemented_targets(task_routing_content: str) -> dict[str, dict[str, str]]:
    match = re.search(
        r"## Implemented Route Targets\s+(.*?)\s+## Routing Output",
        task_routing_content,
        flags=re.DOTALL,
    )
    if not match:
        return {}
    targets: dict[str, dict[str, str]] = {}
    for line in match.group(1).splitlines():
        if not line.startswith("- `"):
            continue
        name_match = re.match(r"- `([^`]+)`:", line)
        if not name_match:
            continue
        name = normalize_route_target(name_match.group(1))
        refs = re.findall(r"`([^`]+)`", line)
        targets[name] = {
            "wrapper": next((ref for ref in refs[1:] if ref.startswith("skills/")), "n/a"),
            "path": next((ref for ref in refs[1:] if ref.startswith("references/")), "n/a"),
        }
    return targets


def parse_chain_targets(task_routing_content: str) -> set[str]:
    match = re.search(
        r"## Default Skill Chains\s+(.*?)\s+## Task Profile",
        task_routing_content,
        flags=re.DOTALL,
    )
    if not match:
        return set()
    chain_targets: set[str] = set()
    for line in match.group(1).splitlines():
        if not line.startswith("- "):
            continue
        chain_match = re.search(r"`([^`]+)`", line)
        if not chain_match:
            continue
        for part in chain_match.group(1).split("->"):
            target = normalize_route_target(part)
            if target:
                chain_targets.add(target)
    return chain_targets


def validate_record_packet(
    stdout: str,
    expected_blocks: list[str],
    invalid: list[str],
    label: str,
) -> None:
    lines = stdout.splitlines()
    nonempty = [line for line in lines if line.strip()]
    if not nonempty:
        invalid.append(f"{label} output is empty")
        return
    if nonempty[0] != "## Execution Summary":
        invalid.append(f"{label} output must start directly with ## Execution Summary")
    for block in expected_blocks:
        if block not in stdout:
            invalid.append(f"{label} output missing {block}")
    for index, line in enumerate(lines):
        if line.startswith("## "):
            next_index = index + 1
            if next_index < len(lines) and lines[next_index] and not lines[next_index].startswith("- "):
                invalid.append(f"{label} record heading has non-field prose after it: {line}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill-dir",
        default=".",
        help="Path to the DevGuard skill directory. Defaults to the current directory.",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    missing: list[str] = []
    invalid: list[str] = []

    print(f"Checking DevGuard bundle at: {skill_dir}")
    for rel_path in EXPECTED_FILES:
        full_path = skill_dir / rel_path
        exists = full_path.exists()
        print(f"{'OK   ' if exists else 'MISS '} {rel_path}")
        if not exists:
            missing.append(rel_path)

    disclosure_index = skill_dir / "references/rule-disclosure-index.md"
    disclosure_index_content = ""
    if disclosure_index.exists():
        content = disclosure_index.read_text(encoding="utf-8")
        disclosure_index_content = content
        for section in DISCLOSURE_INDEX_SECTIONS:
            if section not in content:
                invalid.append(f"references/rule-disclosure-index.md missing {section}")
        if "## Layer Taxonomy" not in content:
            invalid.append("references/rule-disclosure-index.md missing Layer Taxonomy")

    rule_loading = skill_dir / "references/rule-loading.md"
    if rule_loading.exists():
        content = rule_loading.read_text(encoding="utf-8")
        for section in RULE_LOADING_SECTIONS:
            if section not in content:
                invalid.append(f"references/rule-loading.md missing {section}")

    severity_levels = skill_dir / "references/severity-levels.md"
    if severity_levels.exists():
        content = severity_levels.read_text(encoding="utf-8")
        for section in SEVERITY_LEVELS_SECTIONS:
            if section not in content:
                invalid.append(f"references/severity-levels.md missing {section}")

    report_templates = skill_dir / "references/report-templates.md"
    detailed_templates = skill_dir / "references/report-templates-detailed.md"
    report_templates_content = ""
    if report_templates.exists():
        content = report_templates.read_text(encoding="utf-8")
        report_templates_content = content
        for section in REPORT_TEMPLATE_SECTIONS:
            if section not in content:
                invalid.append(f"references/report-templates.md missing {section}")

    detailed_content = (
        detailed_templates.read_text(encoding="utf-8") if detailed_templates.exists() else ""
    )
    if report_templates_content:
        for phrase in REPORT_TEMPLATE_REQUIRED_PHRASES:
            if phrase not in report_templates_content and phrase not in detailed_content:
                invalid.append(f"references/report-templates missing structural-tool field: {phrase}")

    codegraph_understanding = skill_dir / "references/codegraph-project-understanding.md"
    if codegraph_understanding.exists():
        content = codegraph_understanding.read_text(encoding="utf-8")
        for section in CODEGRAPH_UNDERSTANDING_SECTIONS:
            if section not in content:
                invalid.append(f"references/codegraph-project-understanding.md missing {section}")
        for phrase in CODEGRAPH_UNDERSTANDING_REQUIRED_PHRASES:
            if phrase not in content:
                invalid.append(
                    "references/codegraph-project-understanding.md missing repair-flow phrase: "
                    + phrase
                )

    official_docs = skill_dir / "references/official-docs-check.md"
    if official_docs.exists():
        content = official_docs.read_text(encoding="utf-8")
        for section in OFFICIAL_DOCS_SECTIONS:
            if section not in content:
                invalid.append(f"references/official-docs-check.md missing {section}")

    skill_md = skill_dir / "SKILL.md"
    skill_content = skill_md.read_text(encoding="utf-8") if skill_md.exists() else ""
    rule_loading_content = rule_loading.read_text(encoding="utf-8") if rule_loading.exists() else ""
    task_routing = skill_dir / "references/task-routing.md"
    task_routing_content = task_routing.read_text(encoding="utf-8") if task_routing.exists() else ""
    forward_testing = skill_dir / "references/forward-testing.md"
    forward_testing_content = forward_testing.read_text(encoding="utf-8") if forward_testing.exists() else ""

    if disclosure_index_content and task_routing_content:
        rule_rows = parse_markdown_table(disclosure_index_content, "Rule Index")
        rule_index = {row.get("Rule", ""): row for row in rule_rows}
        for row in rule_rows:
            layer = row.get("Layer", "")
            if layer not in ALLOWED_RULE_LAYERS:
                invalid.append(
                    f"references/rule-disclosure-index.md has unsupported layer '{layer}' for {row.get('Rule', '')}"
                )
            wrapper_path = row.get("Wrapper path", "")
            reference_path = row.get("Path", "")
            if wrapper_path != "n/a" and not (skill_dir / wrapper_path).exists():
                invalid.append(f"rule-disclosure-index wrapper path missing: {wrapper_path}")
            if reference_path != "n/a" and not (skill_dir / reference_path).exists():
                invalid.append(f"rule-disclosure-index reference path missing: {reference_path}")

        implemented_targets = parse_implemented_targets(task_routing_content)
        chain_targets = parse_chain_targets(task_routing_content)
        implemented_names = set(implemented_targets)
        for target in sorted(chain_targets):
            if target == "task-contract-freeze":
                continue
            if target not in implemented_names:
                invalid.append(f"default skill chain target missing implemented mapping: {target}")

        for target, target_paths in implemented_targets.items():
            if target == "task-contract-freeze":
                continue
            row = rule_index.get(target)
            if not row:
                invalid.append(f"rule-disclosure-index missing implemented target: {target}")
                continue
            if row.get("Wrapper path", "") != target_paths["wrapper"]:
                invalid.append(
                    f"wrapper mismatch for {target}: index={row.get('Wrapper path', '')} "
                    f"routing={target_paths['wrapper']}"
                )
            if row.get("Path", "") != target_paths["path"]:
                invalid.append(
                    f"reference mismatch for {target}: index={row.get('Path', '')} "
                    f"routing={target_paths['path']}"
                )

    if "Execution Summary" not in skill_content or "Task Contract Summary" not in skill_content:
        invalid.append("SKILL.md missing default outward packet contract")
    if "standalone record blocks" not in skill_content:
        invalid.append("SKILL.md missing standalone record-block discipline")
    for rel_path, phrases in DEFAULT_OUTPUT_HARD_CAP_FILES.items():
        hard_cap_path = skill_dir / rel_path
        hard_cap_content = hard_cap_path.read_text(encoding="utf-8") if hard_cap_path.exists() else ""
        for phrase in phrases:
            if phrase not in hard_cap_content:
                invalid.append(f"{rel_path} missing hard default-output cap phrase: {phrase}")
    for rel_path, phrases in UI_REAL_SCENARIO_REQUIRED_PHRASES.items():
        scenario_path = skill_dir / rel_path
        scenario_content = scenario_path.read_text(encoding="utf-8") if scenario_path.exists() else ""
        for phrase in phrases:
            if phrase not in scenario_content:
                invalid.append(f"{rel_path} missing real-UI-scenario phrase: {phrase}")
    for rel_path, phrases in BUG_FIX_EVIDENCE_REQUIRED_PHRASES.items():
        evidence_path = skill_dir / rel_path
        evidence_content = evidence_path.read_text(encoding="utf-8") if evidence_path.exists() else ""
        for phrase in phrases:
            if phrase not in evidence_content:
                invalid.append(f"{rel_path} missing bug-fix evidence phrase: {phrase}")
    for rel_path, phrases in MINIMUM_CHANGE_REQUIRED_PHRASES.items():
        minimum_path = skill_dir / rel_path
        minimum_content = minimum_path.read_text(encoding="utf-8") if minimum_path.exists() else ""
        for phrase in phrases:
            if phrase not in minimum_content:
                invalid.append(f"{rel_path} missing minimum-change phrase: {phrase}")
    for rel_path, phrases in WRAPPER_DISCLOSURE_REQUIRED_PHRASES.items():
        wrapper_path = skill_dir / rel_path
        wrapper_content = wrapper_path.read_text(encoding="utf-8") if wrapper_path.exists() else ""
        for phrase in phrases:
            if phrase not in wrapper_content:
                invalid.append(f"{rel_path} missing wrapper disclosure phrase: {phrase}")

    if "--format rule-summary" not in skill_content:
        invalid.append("SKILL.md missing explicit rule-summary helper guidance")

    description_match = re.search(r"^description:\s*(.+)$", skill_content, re.MULTILINE)
    if not description_match:
        invalid.append("SKILL.md missing frontmatter description")
    else:
        description_text = description_match.group(1).strip().strip('"').strip("'")
        if len(description_text) > P4_MAX_INVOCATION_CHARS:
            invalid.append(
                f"SKILL.md description exceeds {P4_MAX_INVOCATION_CHARS} chars ({len(description_text)})"
            )
        if "Use for" not in description_text and "Use when" not in description_text:
            invalid.append("SKILL.md description missing When to use guidance")
        if "Not for" not in description_text and "Do not use" not in description_text:
            invalid.append("SKILL.md description missing When NOT to use guidance")
    for phrase in P4_COEXISTENCE_PHRASES:
        if phrase not in skill_content:
            invalid.append(f"SKILL.md missing coexistence phrase: {phrase}")

    openai_yaml = skill_dir / "agents/openai.yaml"
    openai_content = openai_yaml.read_text(encoding="utf-8") if openai_yaml.exists() else ""
    prompt_match = re.search(r'default_prompt:\s*"([^"]+)"', openai_content)
    if not prompt_match:
        invalid.append("agents/openai.yaml missing quoted default_prompt")
    else:
        prompt_text = prompt_match.group(1)
        if len(prompt_text) > P4_MAX_INVOCATION_CHARS:
            invalid.append(
                f"agents/openai.yaml default_prompt exceeds {P4_MAX_INVOCATION_CHARS} chars ({len(prompt_text)})"
            )

    example_prompts = skill_dir / "references/example-prompts.md"
    example_prompts_content = (
        example_prompts.read_text(encoding="utf-8") if example_prompts.exists() else ""
    )
    if "## Short Triggers" not in example_prompts_content:
        invalid.append("references/example-prompts.md missing Short Triggers section")
    for trigger in P4_SHORT_TRIGGERS:
        if trigger not in example_prompts_content:
            invalid.append(f"references/example-prompts.md missing short trigger: {trigger}")
    if "### Short Invocation Triggers" not in task_routing_content:
        invalid.append("references/task-routing.md missing Short Invocation Triggers section")
    for trigger in P4_SHORT_TRIGGERS:
        if trigger not in task_routing_content:
            invalid.append(f"references/task-routing.md missing short trigger: {trigger}")

    for phrase in P5_CODEGRAPH_FALLBACK_PHRASES:
        if phrase not in codegraph_understanding.read_text(encoding="utf-8") if codegraph_understanding.exists() else "":
            invalid.append(f"references/codegraph-project-understanding.md missing no-index phrase: {phrase}")
    official_docs_content_early = official_docs.read_text(encoding="utf-8") if official_docs.exists() else ""
    for phrase in P5_OFFICIAL_DOCS_PHRASES:
        if phrase not in official_docs_content_early:
            invalid.append(f"references/official-docs-check.md missing official-docs layer phrase: {phrase}")
    if "- Structural tool:" not in report_templates_content:
        invalid.append("references/report-templates.md missing Execution Summary Structural tool field")
    if "- Official constraint:" not in report_templates_content:
        invalid.append("references/report-templates.md missing Task Contract Official constraint field")

    glossary = skill_dir / "references/glossary.md"
    glossary_content = glossary.read_text(encoding="utf-8") if glossary.exists() else ""
    glossary_rows = [
        line
        for line in glossary_content.splitlines()
        if line.startswith("| ") and not line.startswith("| Term") and not line.startswith("|---")
    ]
    if len(glossary_rows) < GLOSSARY_MIN_TERMS:
        invalid.append(
            f"references/glossary.md has {len(glossary_rows)} terms; need at least {GLOSSARY_MIN_TERMS}"
        )
    for term in GLOSSARY_REQUIRED_TERMS:
        if term not in glossary_content:
            invalid.append(f"references/glossary.md missing glossary term: {term}")

    for rel_path, phrases in LITE_REQUIRED_PHRASES.items():
        lite_path = skill_dir / rel_path
        lite_content = lite_path.read_text(encoding="utf-8") if lite_path.exists() else ""
        for phrase in phrases:
            if phrase not in lite_content:
                invalid.append(f"{rel_path} missing LITE phrase: {phrase}")

    if rule_loading_content.count("- Meta rules:") != 1:
        invalid.append("references/rule-loading.md should define Meta rules once")

    if (
        "Execution Summary + Task Contract Summary" not in rule_loading_content
        or "standalone `Rule-Loading Summary` only when rule-loading-specific output is explicitly requested"
        not in rule_loading_content
    ):
        invalid.append("references/rule-loading.md missing canonical default-packet guidance")
    if "Pre-execution gates" not in rule_loading_content or "Execution core" not in rule_loading_content:
        invalid.append("references/rule-loading.md missing pre-execution/execution layer split")
    if "Meta rules and mandatory pre-execution gates do not consume the execution-core budget" not in rule_loading_content:
        invalid.append("references/rule-loading.md missing budget taxonomy rule")
    if "If the extra load is justified, mark the task `ALLOW_WITH_WARNINGS`" not in rule_loading_content:
        invalid.append("references/rule-loading.md missing hard budget-overrun action")
    if "execution mode is `STRICT`" not in rule_loading_content:
        invalid.append("references/rule-loading.md missing STRICT focused-expansion trigger")
    if "standalone record blocks" not in report_templates_content:
        invalid.append("references/report-templates.md missing standalone record-block discipline")
    if "standalone record blocks" not in rule_loading_content:
        invalid.append("references/rule-loading.md missing standalone record-block discipline")

    if "Do not let `STRICT` execution mode automatically force full outward disclosure" not in task_routing_content:
        invalid.append("references/task-routing.md missing STRICT disclosure decoupling rule")

    official_docs_content = official_docs.read_text(encoding="utf-8") if official_docs.exists() else ""
    if "Do not query broad official documentation packs" not in task_routing_content:
        invalid.append("references/task-routing.md missing on-demand official-docs loading rule")
    if "Do not query broad official documentation packs" not in official_docs_content:
        invalid.append("references/official-docs-check.md missing on-demand official-docs loading rule")
    if "Context7" not in official_docs_content:
        invalid.append("references/official-docs-check.md missing Context7 guidance")
    if "original official docs" not in official_docs_content and "original official docs or API reference" not in official_docs_content:
        invalid.append("references/official-docs-check.md missing original official-doc verification rule")
    if "native_ui_guideline" not in task_routing_content:
        invalid.append("references/task-routing.md missing native_ui_guideline risk tag")

    for section in TASK_ROUTING_SECTIONS:
        if section not in task_routing_content:
            invalid.append(f"references/task-routing.md missing {section}")
    for tag in PRIMARY_RISK_TAGS:
        if f"`{tag}`" not in task_routing_content:
            invalid.append(f"references/task-routing.md missing primary risk tag: {tag}")
    for route_id in NAMED_ROUTE_IDS:
        if route_id not in task_routing_content:
            invalid.append(f"references/task-routing.md missing named route: {route_id}")
    if "FAST` must not over-gate" not in task_routing_content:
        invalid.append("references/task-routing.md missing FAST over-gate guard")

    shared_guardrails = skill_dir / "references/shared-guardrails.md"
    shared_guardrails_content = (
        shared_guardrails.read_text(encoding="utf-8") if shared_guardrails.exists() else ""
    )
    for section in ["### P0 Hard Blocks", "### P1 Domain Gates", "### P2 Warnings"]:
        if section not in shared_guardrails_content:
            invalid.append(f"references/shared-guardrails.md missing {section}")

    dynamic_reroute = skill_dir / "references/dynamic-reroute-core.md"
    dynamic_reroute_content = (
        dynamic_reroute.read_text(encoding="utf-8") if dynamic_reroute.exists() else ""
    )
    if "### Reroute Trigger Table" not in dynamic_reroute_content:
        invalid.append("references/dynamic-reroute-core.md missing Reroute Trigger Table")
    if "refresh only `Execution Summary` fields for Mode, Rules, Status, and Next" not in dynamic_reroute_content:
        invalid.append("references/dynamic-reroute-core.md missing outward reroute disclosure rule")

    for rel_path in P3_CORE_REFERENCE_FILES:
        core_path = skill_dir / rel_path
        if core_path.exists():
            core_content = core_path.read_text(encoding="utf-8")
            for section in CORE_THREE_PART_SECTIONS:
                if section not in core_content:
                    invalid.append(f"{rel_path} missing {section}")

    selective_project_loading = skill_dir / "references/selective-project-loading.md"
    selective_project_content = (
        selective_project_loading.read_text(encoding="utf-8")
        if selective_project_loading.exists()
        else ""
    )
    for phrase in [
        "## Missing Project Rule Gate",
        "emit `Exception Note`",
        "set status to `BLOCKED` when project rules are required for safe execution",
        "do not invent project-rule paths",
    ]:
        if phrase not in selective_project_content:
            invalid.append(f"references/selective-project-loading.md missing project-rule gate phrase: {phrase}")

    for rel_path, expected_text in EXPECTED_SHARED_STUBS.items():
        stub_path = skill_dir / rel_path
        if stub_path.exists():
            stub_content = stub_path.read_text(encoding="utf-8")
            if expected_text not in stub_content:
                invalid.append(f"{rel_path} no longer points to the canonical reference text")

    chains_match = re.search(
        r"## Default Skill Chains\s+(.*?)\s+## Task Profile",
        task_routing_content,
        flags=re.DOTALL,
    )
    if not chains_match:
        invalid.append("references/task-routing.md missing default skill chains section")
    else:
        chains_block = chains_match.group(1)
        if "official-docs-check ->" in chains_block:
            invalid.append("default skill chains must use optional official-docs-check? routing")
        if "official-docs-check?" not in chains_block:
            invalid.append("default skill chains missing optional official-docs-check? marker")
        for line in chains_block.splitlines():
            if line.startswith("- ") and "Release or go-live" not in line:
                if "task-contract-freeze" not in line:
                    invalid.append(f"default chain missing task-contract-freeze: {line}")
        if "bug-fix(diagnosis-only)" not in chains_block or "bug-fix(minimal-repair)" not in chains_block:
            invalid.append("bug-fix chains must separate diagnosis from minimal repair")

    forbidden_report_template_phrases = [
        "detailed or strict disclosure",
        "detailed or strict templates",
    ]
    for phrase in forbidden_report_template_phrases:
        if phrase in report_templates_content:
            invalid.append(f"references/report-templates.md still contains forbidden phrase: {phrase}")

    if forward_testing_content:
        for phrase in FORWARD_TESTING_REQUIRED_PHRASES:
            if phrase not in forward_testing_content:
                invalid.append(f"references/forward-testing.md missing structural-tool test phrase: {phrase}")
        match = re.search(
            r"## Regression Example Set\s+(.*?)\s+## Recommended Scenarios",
            forward_testing_content,
            flags=re.DOTALL,
        )
        if not match:
            invalid.append("references/forward-testing.md missing regression example section")
        else:
            regression_block = match.group(1)
            scenario_count = len(re.findall(r"^### \d+\.", regression_block, flags=re.MULTILINE))
            if "Use these four regression scenarios" not in forward_testing_content:
                invalid.append("references/forward-testing.md regression count summary is not updated")
            if scenario_count != 4:
                invalid.append(
                    f"references/forward-testing.md expected 4 regression scenarios, found {scenario_count}"
                )
            normal_task_match = re.search(
                r"### 1\. Normal Task Default Output\s+(.*?)(?:\n### 2\.|\Z)",
                regression_block,
                flags=re.DOTALL,
            )
            if not normal_task_match:
                invalid.append("references/forward-testing.md missing normal-task regression block")
            else:
                normal_task_block = normal_task_match.group(1)
                for phrase in [
                    "`Project Understanding Summary`",
                    "`Impact Analysis Summary`",
                    "`Official Docs Check Summary`",
                ]:
                    if phrase not in normal_task_block:
                        invalid.append(
                            "references/forward-testing.md normal-task regression block missing stage-summary ban: "
                            + phrase
                        )

    generator_script = skill_dir / "scripts/generate_rule_loading_manifest.py"
    if generator_script.exists():
        summary_proc = subprocess.run(
            [
                sys.executable,
                str(generator_script),
                "--format",
                "summary",
                "--task",
                "demo task",
                "--task-type",
                "bugfix + ui",
                "--execution-mode",
                "STANDARD",
                "--status",
                "ALLOW",
                "--next-step",
                "freeze contract",
                "--loaded",
                "meta|task-router|path|why|summary",
                "--loaded",
                "core|impact-analysis|path|why|summary",
                "--contract-goal",
                "fix the issue",
                "--contract-non-goals",
                "no refactor",
                "--contract-allowed-edits",
                "ExampleSettingsPage.xaml",
                "--contract-acceptance-criteria",
                "UI works",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if summary_proc.returncode != 0:
            invalid.append(
                "scripts/generate_rule_loading_manifest.py summary smoke test failed: "
                + summary_proc.stderr.strip()
            )
        else:
            stdout = summary_proc.stdout
            validate_record_packet(
                stdout,
                ["## Execution Summary", "## Task Contract Summary"],
                invalid,
                "summary format",
            )
            for stage_block in DEFAULT_STAGE_SUMMARY_BLOCKS:
                if stage_block in stdout:
                    invalid.append(f"summary format must not emit {stage_block}")
            if "## Rule-Loading Summary" in stdout:
                invalid.append("summary format still emits standalone Rule-Loading Summary")
            if "Meta: task-router" not in stdout:
                invalid.append("summary format must include loaded meta rules")
            if "Core: task-router" in stdout:
                invalid.append("summary format must not relabel meta rules as core rules")

        rule_summary_proc = subprocess.run(
            [
                sys.executable,
                str(generator_script),
                "--format",
                "rule-summary",
                "--task-type",
                "bugfix + ui",
                "--execution-mode",
                "STANDARD",
                "--status",
                "ALLOW",
                "--loaded",
                "meta|task-router|path|why|summary",
                "--loaded",
                "core|impact-analysis|path|why|summary",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if rule_summary_proc.returncode != 0:
            invalid.append(
                "scripts/generate_rule_loading_manifest.py rule-summary smoke test failed: "
                + rule_summary_proc.stderr.strip()
            )
        elif "## Rule-Loading Summary" not in rule_summary_proc.stdout:
            invalid.append("rule-summary format no longer emits Rule-Loading Summary")
        else:
            if "- Meta: task-router" not in rule_summary_proc.stdout:
                invalid.append("rule-summary format must include loaded meta rules")

        risk_proc = subprocess.run(
            [
                sys.executable,
                str(generator_script),
                "--format",
                "risk",
                "--task",
                "risk demo",
                "--task-type",
                "bugfix + release",
                "--execution-mode",
                "STRICT",
                "--status",
                "ALLOW_WITH_WARNINGS",
                "--next-step",
                "run focused checks",
                "--loaded",
                "meta|task-router|path|why|summary",
                "--loaded",
                "core|release-check|path|why|summary",
                "--risk-focus",
                "release replay gating",
                "--risk-affected-rules",
                "release-check",
                "--risk-why",
                "rollback-sensitive path",
                "--risk-extra-checks",
                "focused replay validation",
                "--contract-goal",
                "stabilize replay gating",
                "--contract-non-goals",
                "no installer rewrite",
                "--contract-allowed-edits",
                "tests and validation script",
                "--contract-acceptance-criteria",
                "focused replay checks pass",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if risk_proc.returncode != 0:
            invalid.append(
                "scripts/generate_rule_loading_manifest.py risk smoke test failed: "
                + risk_proc.stderr.strip()
            )
        else:
            stdout = risk_proc.stdout
            validate_record_packet(
                stdout,
                ["## Execution Summary", "## Risk Note", "## Task Contract Summary"],
                invalid,
                "risk format",
            )
            for stage_block in DEFAULT_STAGE_SUMMARY_BLOCKS:
                if stage_block in stdout:
                    invalid.append(f"risk format must not emit {stage_block}")
            if "## Rule-Loading Risk Notes" in stdout:
                invalid.append("risk format must not emit standalone Rule-Loading Risk Notes")

        exception_proc = subprocess.run(
            [
                sys.executable,
                str(generator_script),
                "--format",
                "exception",
                "--task",
                "exception demo",
                "--task-type",
                "bugfix + ui",
                "--execution-mode",
                "STANDARD",
                "--status",
                "BLOCKED",
                "--next-step",
                "load missing rule",
                "--exception-reason",
                "required project rule is missing",
                "--exception-missing",
                "example-desktop project rule",
                "--exception-required",
                "load example-desktop project rule before continuing",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if exception_proc.returncode != 0:
            invalid.append(
                "scripts/generate_rule_loading_manifest.py exception smoke test failed: "
                + exception_proc.stderr.strip()
            )
        else:
            stdout = exception_proc.stdout
            validate_record_packet(
                stdout,
                ["## Execution Summary", "## Exception Note"],
                invalid,
                "exception format",
            )
            for stage_block in DEFAULT_STAGE_SUMMARY_BLOCKS:
                if stage_block in stdout:
                    invalid.append(f"exception format must not emit {stage_block}")
            if "## Rule-Loading Exception" in stdout:
                invalid.append("exception format must not emit standalone Rule-Loading Exception")

        empty_summary_proc = subprocess.run(
            [
                sys.executable,
                str(generator_script),
                "--format",
                "summary",
                "--task",
                "empty rules demo",
                "--task-type",
                "bugfix",
                "--execution-mode",
                "STANDARD",
                "--status",
                "ALLOW",
                "--next-step",
                "continue",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if empty_summary_proc.returncode == 0:
            invalid.append("summary format must reject ALLOW without any loaded rules")

        full_proc = subprocess.run(
            [
                sys.executable,
                str(generator_script),
                "--format",
                "full",
                "--task-type",
                "bugfix",
                "--execution-mode",
                "STANDARD",
                "--status",
                "ALLOW",
                "--stage",
                "route",
                "--loaded",
                "meta|task-router|path|why|summary",
                "--decision-reason",
                "detailed evidence requested",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if full_proc.returncode != 0:
            invalid.append(
                "scripts/generate_rule_loading_manifest.py full smoke test failed: "
                + full_proc.stderr.strip()
            )
        elif "Human confirmation points" in full_proc.stdout:
            invalid.append("full manifest output must match the canonical rule-loading schema")

    skillopt_judge = skill_dir / "scripts" / "run_skillopt_judge.py"
    if skillopt_judge.exists():
        skillopt_proc = subprocess.run(
            [sys.executable, str(skillopt_judge), "--skill-dir", str(skill_dir), "--dataset", "all"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if skillopt_proc.returncode != 0:
            invalid.append(
                "scripts/run_skillopt_judge.py dataset validation failed: "
                + skillopt_proc.stderr.strip()
                + skillopt_proc.stdout.strip()
            )

    gitignore = skill_dir / ".gitignore"
    if gitignore.exists():
        gitignore_content = gitignore.read_text(encoding="utf-8")
        for ignored_path in [".codegraph/", "graphify-out/", "skillopt/"]:
            if ignored_path not in gitignore_content:
                invalid.append(f".gitignore missing generated artifact ignore: {ignored_path}")

    for rel_path in P7_REQUIRED_FILES:
        full_path = skill_dir / rel_path
        exists = full_path.exists()
        print(f"{'OK   ' if exists else 'MISS '} {rel_path}")
        if not exists:
            missing.append(rel_path)

    if skill_md.exists():
        skill_lines = len(skill_content.splitlines())
        if skill_lines > P7_MAX_SKILL_LINES:
            invalid.append(f"SKILL.md has {skill_lines} lines; P7 max is {P7_MAX_SKILL_LINES}")
        for phase in P7_SKILL_PHASES:
            if phase not in skill_content:
                invalid.append(f"SKILL.md missing P7 phase: {phase}")
        if "control-plane-core.md" not in skill_content:
            invalid.append("SKILL.md missing control-plane-core.md link")
        if "devguard-lookup.md" not in skill_content:
            invalid.append("SKILL.md missing devguard-lookup.md link")
        if "Default Workflow" in skill_content and "1. Route with" in skill_content:
            invalid.append("SKILL.md still uses legacy 8-step Default Workflow")

    readme_md = skill_dir / "README.md"
    readme_content = readme_md.read_text(encoding="utf-8") if readme_md.exists() else ""
    if readme_content:
        if "## Runtime Flow" in readme_content:
            invalid.append("README.md still contains legacy Runtime Flow section")
        if "control-plane-core.md" not in readme_content:
            invalid.append("README.md missing control-plane-core.md link")

    if report_templates.exists():
        template_lines = len(report_templates_content.splitlines())
        if template_lines > P7_MAX_REPORT_TEMPLATES_LINES:
            invalid.append(
                f"references/report-templates.md has {template_lines} lines; "
                f"P7 max is {P7_MAX_REPORT_TEMPLATES_LINES}"
            )
        for section in P7_REPORT_TEMPLATE_MAIN_SECTIONS:
            if section not in report_templates_content:
                invalid.append(f"references/report-templates.md missing P7 main section: {section}")
        if "report-templates-detailed.md" not in report_templates_content:
            invalid.append("references/report-templates.md missing link to report-templates-detailed.md")
        for section in [
            "## Skill Routing Decision",
            "## Rule-Loading Manifest",
            "## Development Completion Report",
        ]:
            if section in report_templates_content:
                invalid.append(
                    f"references/report-templates.md still contains T3 section in main file: {section}"
                )

    detailed_templates = skill_dir / "references/report-templates-detailed.md"
    detailed_content = (
        detailed_templates.read_text(encoding="utf-8") if detailed_templates.exists() else ""
    )
    for section in P7_REPORT_TEMPLATE_DETAILED_SECTIONS:
        if detailed_content and section not in detailed_content:
            invalid.append(f"references/report-templates-detailed.md missing {section}")

    lookup_md = skill_dir / "references/devguard-lookup.md"
    if lookup_md.exists():
        lookup_lines = len(lookup_md.read_text(encoding="utf-8").splitlines())
        if lookup_lines > P7_MAX_LOOKUP_LINES:
            invalid.append(f"references/devguard-lookup.md has {lookup_lines} lines; max {P7_MAX_LOOKUP_LINES}")

    control_plane = skill_dir / "references/control-plane-core.md"
    if control_plane.exists():
        cp_content = control_plane.read_text(encoding="utf-8")
        for phase in P7_SKILL_PHASES:
            if phase not in cp_content:
                invalid.append(f"references/control-plane-core.md missing phase: {phase}")

    skills_dir = skill_dir / "skills"
    if skills_dir.exists():
        active_wrappers: list[str] = []
        for wrapper_path in sorted(skills_dir.glob("*/SKILL.md")):
            rel = wrapper_path.relative_to(skill_dir).as_posix()
            wrapper_lines = len(wrapper_path.read_text(encoding="utf-8").splitlines())
            if wrapper_lines > P7_MAX_ACTIVE_WRAPPER_LINES and rel not in P7_ACTIVE_WRAPPER_ALLOWLIST:
                active_wrappers.append(rel)
        if len(active_wrappers) > 0:
            invalid.append(
                "P7 requires stub wrappers except allowlist; active wrappers: "
                + ", ".join(active_wrappers)
            )

    if openai_content and "control-plane-core.md" not in openai_content and "Orient" not in openai_content:
        invalid.append("agents/openai.yaml must reference P7 three-phase workflow")

    validate_script = skill_dir / "scripts/validate_outward_packet.py"
    if validate_script.exists():
        validate_proc = subprocess.run(
            [sys.executable, str(validate_script), "--self-test"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if validate_proc.returncode != 0:
            invalid.append(
                "scripts/validate_outward_packet.py self-test failed: "
                + validate_proc.stderr.strip()
                + validate_proc.stdout.strip()
            )

    benchmark_path = skill_dir / "skillopt/benchmark.jsonl"
    if benchmark_path.exists():
        benchmark_ids = []
        for line in benchmark_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                benchmark_ids.append(json.loads(line).get("task_id", ""))
        for required_id in ["socratic-inquiry", "lite-skip-inquiry", "three-phase-normal"]:
            if required_id not in benchmark_ids:
                invalid.append(f"skillopt/benchmark.jsonl missing P7 scenario: {required_id}")
        if len(benchmark_ids) < 16:
            invalid.append(f"skillopt/benchmark.jsonl has {len(benchmark_ids)} entries; P7 needs >= 16")

    if missing:
        print("\nMissing files:")
        for rel_path in missing:
            print(f"- {rel_path}")
        return 1

    if invalid:
        print("\nInvalid files:")
        for item in invalid:
            print(f"- {item}")
        return 1

    print("\nDevGuard bundle looks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
