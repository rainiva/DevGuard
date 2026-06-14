#!/usr/bin/env python3
"""Check DevGuard bundle structure and key disclosure invariants."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


EXPECTED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/task-routing.md",
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
    "references/batch-roadmap.md",
    "scripts/generate_rule_loading_manifest.py",
    "scripts/check_devguard_bundle.py",
    "shared/evidence-rules.md",
    "shared/blocking-rules.md",
    "shared/severity-levels.md",
    "shared/report-templates.md",
    "skills/00-task-router/SKILL.md",
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
    "## Summary Output Discipline",
    "## Record Block Discipline",
    "## Execution Summary",
    "## Risk Note",
    "## Exception Note",
    "## Official Docs Check Summary",
    "## Official Docs Focused Expansion",
    "## Focused Expansion Discipline",
    "## Routing Summary",
    "## Routing Focused Expansion",
    "## Rule-Loading Summary",
    "## Rule-Loading Exception",
    "## Rule-Loading Risk Notes",
    "## Rule-Loading Manifest",
    "## Project Understanding Summary",
    "## Project Understanding Focused Expansion",
    "## CodeGraph Project Understanding Report",
    "## Official Docs Check Report",
    "## Strict Project Understanding Additions",
    "## Impact Analysis Focused Expansion",
    "## Task Contract Focused Expansion",
    "## Review Verdict Mapping",
]
SEVERITY_LEVELS_SECTIONS = ["## Metadata", "## Summary", "## Review Verdict Mapping", "## Full Rule"]
CODEGRAPH_UNDERSTANDING_SECTIONS = ["## Metadata", "## Summary", "## Full Rule"]
OFFICIAL_DOCS_SECTIONS = ["## Metadata", "## Summary", "## Full Rule"]


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
    if disclosure_index.exists():
        content = disclosure_index.read_text(encoding="utf-8")
        for section in DISCLOSURE_INDEX_SECTIONS:
            if section not in content:
                invalid.append(f"references/rule-disclosure-index.md missing {section}")

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
    if report_templates.exists():
        content = report_templates.read_text(encoding="utf-8")
        for section in REPORT_TEMPLATE_SECTIONS:
            if section not in content:
                invalid.append(f"references/report-templates.md missing {section}")

    codegraph_understanding = skill_dir / "references/codegraph-project-understanding.md"
    if codegraph_understanding.exists():
        content = codegraph_understanding.read_text(encoding="utf-8")
        for section in CODEGRAPH_UNDERSTANDING_SECTIONS:
            if section not in content:
                invalid.append(f"references/codegraph-project-understanding.md missing {section}")

    official_docs = skill_dir / "references/official-docs-check.md"
    if official_docs.exists():
        content = official_docs.read_text(encoding="utf-8")
        for section in OFFICIAL_DOCS_SECTIONS:
            if section not in content:
                invalid.append(f"references/official-docs-check.md missing {section}")

    skill_md = skill_dir / "SKILL.md"
    skill_content = skill_md.read_text(encoding="utf-8") if skill_md.exists() else ""
    report_templates_content = (
        report_templates.read_text(encoding="utf-8") if report_templates.exists() else ""
    )
    rule_loading_content = rule_loading.read_text(encoding="utf-8") if rule_loading.exists() else ""
    task_routing = skill_dir / "references/task-routing.md"
    task_routing_content = task_routing.read_text(encoding="utf-8") if task_routing.exists() else ""
    forward_testing = skill_dir / "references/forward-testing.md"
    forward_testing_content = forward_testing.read_text(encoding="utf-8") if forward_testing.exists() else ""

    if "Execution Summary" not in skill_content or "Task Contract Summary" not in skill_content:
        invalid.append("SKILL.md missing default outward packet contract")
    if "standalone record blocks" not in skill_content:
        invalid.append("SKILL.md missing standalone record-block discipline")

    if "--format rule-summary" not in skill_content:
        invalid.append("SKILL.md missing explicit rule-summary helper guidance")

    if rule_loading_content.count("- Meta rules:") != 1:
        invalid.append("references/rule-loading.md should define Meta rules once")

    if (
        "Execution Summary + Task Contract Summary" not in rule_loading_content
        or "standalone `Rule-Loading Summary` only when rule-loading-specific output is explicitly requested"
        not in rule_loading_content
    ):
        invalid.append("references/rule-loading.md missing canonical default-packet guidance")
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
                "core|task-router|path|why|summary",
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
            if "## Rule-Loading Summary" in stdout:
                invalid.append("summary format still emits standalone Rule-Loading Summary")

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
                "core|task-router|path|why|summary",
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
                "core|task-router|path|why|summary",
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
