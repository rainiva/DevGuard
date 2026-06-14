#!/usr/bin/env python3
"""Generate DevGuard disclosure blocks from structured CLI inputs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_pipe_rows(raw_rows: list[str], expected_parts: int, label: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw in raw_rows:
        parts = [part.strip() for part in raw.split("|")]
        if len(parts) != expected_parts or any(part == "" for part in parts):
            raise ValueError(
                f"Invalid {label} row '{raw}'. Expected {expected_parts} non-empty '|' separated fields."
            )
        rows.append(parts)
    return rows


def render_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "---|" * len(headers),
    ]
    for row in rows:
        safe = [cell.replace("\n", " ").strip() for cell in row]
        lines.append("| " + " | ".join(safe) + " |")
    return lines


def join_rule_names(loaded_rows: list[list[str]], rule_type: str) -> str:
    names = [row[1] for row in loaded_rows if row[0].lower() == rule_type.lower()]
    return " / ".join(names) if names else ""


def build_rules_line(loaded_rows: list[list[str]]) -> str:
    parts: list[str] = []
    core = join_rule_names(loaded_rows, "core") or join_rule_names(loaded_rows, "meta")
    extensions = join_rule_names(loaded_rows, "extension")
    playbooks = join_rule_names(loaded_rows, "playbook")
    project_rules = join_rule_names(loaded_rows, "project rule")
    review = join_rule_names(loaded_rows, "review extension")
    if core:
        parts.append(f"Core: {core}")
    if extensions:
        parts.append(f"Extensions: {extensions}")
    if playbooks:
        parts.append(f"Playbooks: {playbooks}")
    if project_rules:
        parts.append(f"Project Rules: {project_rules}")
    if review:
        parts.append(f"Review: {review}")
    return "; ".join(parts) if parts else "none confirmed"


def build_execution_summary(args: argparse.Namespace, loaded_rows: list[list[str]], status: str) -> str:
    lines = [
        "## Execution Summary",
        f"- Task: {args.task or args.task_type}",
        f"- Mode: {args.execution_mode}",
        f"- Rules: {build_rules_line(loaded_rows)}",
        f"- Status: {status}",
        f"- Next: {args.next_step}",
    ]
    return "\n".join(lines)


def build_task_contract_summary(args: argparse.Namespace) -> str:
    return "\n".join(
        [
            "## Task Contract Summary",
            f"- Goal: {args.contract_goal}",
            f"- Non-goals: {args.contract_non_goals}",
            f"- Allowed edits: {args.contract_allowed_edits}",
            f"- Acceptance criteria: {args.contract_acceptance_criteria}",
        ]
    )


def build_rule_summary(args: argparse.Namespace, loaded_rows: list[list[str]], status: str) -> str:
    lines = [
        "## Rule-Loading Summary",
        f"- Task type: {args.task_type}",
        f"- Execution mode: {args.execution_mode}",
        f"- Core: {join_rule_names(loaded_rows, 'core') or join_rule_names(loaded_rows, 'meta')}",
        f"- Extensions: {join_rule_names(loaded_rows, 'extension')}",
        f"- Playbooks: {join_rule_names(loaded_rows, 'playbook')}",
        f"- Project Rules: {join_rule_names(loaded_rows, 'project rule')}",
        f"- Review: {join_rule_names(loaded_rows, 'review extension')}",
        f"- Status: {status}",
        "",
    ]
    if args.decision_reason:
        lines.insert(-1, f"- Reason: {args.decision_reason}")
    return "\n".join(lines)


def build_exception(args: argparse.Namespace, status: str) -> str:
    reason = "; ".join(args.exception_reasons)
    missing = "; ".join(args.exception_missing) if args.exception_missing else ""
    required = "; ".join(args.exception_required) if args.exception_required else ""
    lines = [
        "## Exception Note",
        f"- Reason: {reason}",
        f"- Missing / wrong: {missing}",
        f"- Required fix: {required}",
        f"- Status: {status}",
    ]
    lines.append("")
    return "\n".join(lines)


def build_risk_notes(args: argparse.Namespace) -> str:
    focus = args.risk_focus
    if args.risk_affected_rules:
        focus = f"{focus}; Affected rules: {args.risk_affected_rules}"
    lines = [
        "## Risk Note",
        f"- Focus: {focus}",
        f"- Why it matters: {args.risk_why}",
        f"- Extra gate: {args.risk_extra_checks}",
        "",
    ]
    return "\n".join(lines)


def build_full_manifest(
    args: argparse.Namespace,
    loaded_rows: list[list[str]],
    deferred_rows: list[list[str]],
    missing_rows: list[list[str]],
    status: str,
) -> str:
    risk_tags = ", ".join(args.risk_tags) if args.risk_tags else ""
    lines = [
        "# Initial Rule-Loading Manifest",
        "",
        "## 1. Task Identification",
        f"- Project: {args.project}",
        f"- Stack: {args.stack}",
        f"- Task type: {args.task_type}",
        f"- Risk tags: {risk_tags}",
        f"- Complexity: {args.complexity}",
        f"- Risk score: {args.risk_score}",
        f"- Execution mode: {args.execution_mode}",
        f"- Human confirmation points: {args.human_confirmation_points}",
        "",
        "## 2. Current Stage",
        f"- Stage: {args.stage}",
        "",
        "## 3. Loaded Rules",
    ]

    if loaded_rows:
        lines.extend(
            render_table(
                ["Type", "Rule", "Path", "Why loaded", "Detail level"],
                loaded_rows,
            )
        )
    else:
        lines.append("| Type | Rule | Path | Why loaded | Detail level |")
        lines.append("|---|---|---|---|---|")

    lines.extend(["", "## 4. Deferred Rules"])
    if deferred_rows:
        lines.extend(render_table(["Rule", "Why deferred", "Trigger to load later"], deferred_rows))
    else:
        lines.append("| Rule | Why deferred | Trigger to load later |")
        lines.append("|---|---|---|")

    lines.extend(["", "## 5. Possibly Missing Rules"])
    if missing_rows:
        lines.extend(render_table(["Rule type", "Why it may be needed"], missing_rows))
    else:
        lines.append("| Rule type | Why it may be needed |")
        lines.append("|---|---|")

    lines.extend(
        [
            "",
            "## 6. Execution Decision",
            f"- Status: {status}",
            f"- Reason: {args.decision_reason}",
            "",
        ]
    )
    return "\n".join(lines)


def build_disclosure(args: argparse.Namespace) -> str:
    loaded_rows = parse_pipe_rows(args.loaded, 5, "loaded")
    deferred_rows = parse_pipe_rows(args.deferred, 3, "deferred")
    missing_rows = parse_pipe_rows(args.missing, 2, "missing")
    status = args.status or {"yes": "ALLOW", "no": "BLOCKED"}[args.may_proceed]
    if (
        args.format in {"summary", "rule-summary", "risk", "exception"}
        and status != "BLOCKED"
        and not loaded_rows
    ):
        raise ValueError(
            f"{args.format} format requires at least one --loaded row unless status is BLOCKED."
        )

    if args.format == "summary":
        disclosure = build_execution_summary(args, loaded_rows, status)
        if args.contract_goal:
            disclosure = disclosure + "\n\n" + build_task_contract_summary(args)
        return disclosure
    if args.format == "rule-summary":
        return build_rule_summary(args, loaded_rows, status)
    if args.format == "risk":
        if not args.risk_focus:
            raise ValueError("risk format requires --risk-focus")
        disclosure = build_execution_summary(args, loaded_rows, status)
        disclosure = disclosure + "\n\n" + build_risk_notes(args).rstrip()
        if args.contract_goal:
            disclosure = disclosure + "\n\n" + build_task_contract_summary(args)
        return disclosure
    if args.format == "exception":
        if not args.exception_reasons:
            raise ValueError("exception format requires at least one --exception-reason")
        disclosure = build_execution_summary(args, loaded_rows, status)
        disclosure = disclosure + "\n\n" + build_exception(args, status).rstrip()
        if args.contract_goal:
            disclosure = disclosure + "\n\n" + build_task_contract_summary(args)
        return disclosure
    return build_full_manifest(args, loaded_rows, deferred_rows, missing_rows, status)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=["summary", "rule-summary", "risk", "full", "exception"],
        default="summary",
        help="Output format. summary, risk, and exception emit the minimal outward packet plus any focused expansion.",
    )
    parser.add_argument("--task", default="", help="User-facing task line for Execution Summary")
    parser.add_argument("--project", default="", help="Project name or blank if none")
    parser.add_argument("--stack", default="", help="Primary stack or blank if none")
    parser.add_argument("--task-type", required=True, help="Task type label")
    parser.add_argument("--risk-tags", nargs="*", default=[], help="Risk tags")
    parser.add_argument("--complexity", default="", help="Complexity level such as S1 or S3")
    parser.add_argument("--risk-score", default="", help="Optional risk score or rationale")
    parser.add_argument("--execution-mode", required=True, help="FAST, STANDARD, or STRICT")
    parser.add_argument(
        "--human-confirmation-points",
        default="",
        help="Optional human confirmation points for risky decisions",
    )
    parser.add_argument("--stage", default="", help="Current stage")
    parser.add_argument(
        "--next-step",
        default="",
        help="Next-step line for the default Execution Summary packet",
    )
    parser.add_argument(
        "--loaded",
        action="append",
        default=[],
        help="Loaded row: Type|Rule|Path|Why loaded|Detail level",
    )
    parser.add_argument(
        "--deferred",
        action="append",
        default=[],
        help="Deferred row: Rule|Why deferred|Trigger to load later",
    )
    parser.add_argument(
        "--missing",
        action="append",
        default=[],
        help="Missing row: Rule type|Why it may be needed",
    )
    parser.add_argument(
        "--risk-focus",
        default="",
        help="Primary risk focus for focused expansion output",
    )
    parser.add_argument(
        "--risk-affected-rules",
        default="",
        help="Affected rules for focused expansion output",
    )
    parser.add_argument(
        "--risk-why",
        default="",
        help="Why the affected rules matter now",
    )
    parser.add_argument(
        "--risk-extra-checks",
        default="",
        help="Extra checks or blockers for focused expansion output",
    )
    parser.add_argument(
        "--exception-reason",
        action="append",
        default=[],
        dest="exception_reasons",
        help="Exception reason bullet",
    )
    parser.add_argument(
        "--exception-missing",
        action="append",
        default=[],
        help="Missing or incorrect rule bullet for exception output",
    )
    parser.add_argument(
        "--exception-required",
        action="append",
        default=[],
        help="Required remediation bullet for exception output",
    )
    parser.add_argument(
        "--may-proceed",
        choices=["yes", "no"],
        help="Deprecated. Use --status. yes maps to ALLOW and no maps to BLOCKED.",
    )
    parser.add_argument(
        "--status",
        choices=["ALLOW", "ALLOW_WITH_WARNINGS", "BLOCKED"],
        help="Canonical execution decision status.",
    )
    parser.add_argument("--decision-reason", default="", help="Reason for the execution decision")
    parser.add_argument("--contract-goal", default="", help="Task Contract Summary goal line")
    parser.add_argument("--contract-non-goals", default="", help="Task Contract Summary non-goals line")
    parser.add_argument(
        "--contract-allowed-edits",
        default="",
        help="Task Contract Summary allowed-edits line",
    )
    parser.add_argument(
        "--contract-acceptance-criteria",
        default="",
        help="Task Contract Summary acceptance-criteria line",
    )
    parser.add_argument("--output", help="Optional output file path")
    args = parser.parse_args()

    if not args.status and not args.may_proceed:
        parser.error("one of --status or --may-proceed is required")

    if args.format in {"summary", "risk", "exception"} and not args.next_step:
        parser.error("--next-step is required for summary, risk, and exception formats")

    if args.format == "full" and not args.stage:
        parser.error("--stage is required for full format")

    contract_values = [
        args.contract_goal,
        args.contract_non_goals,
        args.contract_allowed_edits,
        args.contract_acceptance_criteria,
    ]
    if any(contract_values) and not all(contract_values):
        parser.error(
            "Task Contract Summary requires --contract-goal, --contract-non-goals, "
            "--contract-allowed-edits, and --contract-acceptance-criteria together"
        )

    try:
        disclosure = build_disclosure(args)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(disclosure + "\n", encoding="utf-8")
    else:
        print(disclosure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
