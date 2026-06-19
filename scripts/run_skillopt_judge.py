#!/usr/bin/env python3
"""Validate skillopt datasets and score DevGuard outward transcripts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SUPPORTED_OPS = {
    "section_present",
    "section_absent",
    "contains",
    "not_contains",
    "max_chars",
}


def load_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number} invalid JSON: {exc}") from exc
        rows.append(row)
    return rows


def validate_dataset(path: Path, minimum_rows: int) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing dataset: {path}"]
    try:
        rows = load_jsonl(path)
    except ValueError as exc:
        return [str(exc)]
    if len(rows) < minimum_rows:
        errors.append(f"{path.name} has {len(rows)} rows, expected at least {minimum_rows}")
    for row in rows:
        task_id = row.get("task_id")
        task = row.get("task")
        judge = row.get("judge")
        if not isinstance(task_id, str) or not task_id:
            errors.append(f"{path.name} row missing task_id")
            continue
        if not isinstance(task, str) or "$devguard" not in task:
            errors.append(f"{path.name}:{task_id} task must invoke $devguard")
        if not isinstance(judge, dict) or judge.get("kind") != "rule":
            errors.append(f"{path.name}:{task_id} judge.kind must be rule")
            continue
        checks = judge.get("checks")
        if not isinstance(checks, list) or not checks:
            errors.append(f"{path.name}:{task_id} judge.checks must be non-empty")
            continue
        for check in checks:
            if not isinstance(check, dict):
                errors.append(f"{path.name}:{task_id} check must be an object")
                continue
            op = check.get("op")
            arg = check.get("arg")
            if op not in SUPPORTED_OPS:
                errors.append(f"{path.name}:{task_id} unsupported op: {op}")
            if arg is None:
                errors.append(f"{path.name}:{task_id} check missing arg for op {op}")
    return errors


def evaluate_checks(transcript: str, checks: list[dict[str, object]]) -> list[str]:
    failures: list[str] = []
    for check in checks:
        op = check.get("op")
        arg = check.get("arg")
        if op == "section_present":
            if f"## {arg}" not in transcript:
                failures.append(f"missing section: {arg}")
        elif op == "section_absent":
            if f"## {arg}" in transcript:
                failures.append(f"unexpected section: {arg}")
        elif op == "contains":
            if str(arg).lower() not in transcript.lower():
                failures.append(f"missing text: {arg}")
        elif op == "not_contains":
            if str(arg) in transcript:
                failures.append(f"forbidden text present: {arg}")
        elif op == "max_chars":
            if len(transcript) > int(arg):
                failures.append(f"transcript too long: {len(transcript)} > {arg}")
        else:
            failures.append(f"unsupported op at runtime: {op}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", default=".", help="Path to the DevGuard skill directory.")
    parser.add_argument("--dataset", choices=("benchmark", "held-out", "all"), default="benchmark")
    parser.add_argument("--minimum-rows", type=int, default=12)
    parser.add_argument("--transcript", help="Optional transcript file to score against one task_id.")
    parser.add_argument("--task-id", help="Task id to use with --transcript.")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    datasets: list[tuple[str, Path, int]] = []
    if args.dataset in ("benchmark", "all"):
        datasets.append(("benchmark", skill_dir / "skillopt" / "benchmark.jsonl", args.minimum_rows))
    if args.dataset in ("held-out", "all"):
        datasets.append(("held-out", skill_dir / "skillopt" / "held-out.jsonl", 3))

    errors: list[str] = []
    rows_by_id: dict[str, dict[str, object]] = {}
    for label, path, minimum_rows in datasets:
        dataset_errors = validate_dataset(path, minimum_rows)
        errors.extend(dataset_errors)
        if not dataset_errors:
            for row in load_jsonl(path):
                rows_by_id[str(row["task_id"])] = row
            print(f"OK   {label}: {path.name} ({len(load_jsonl(path))} rows)")

    if args.transcript:
        if not args.task_id:
            print("--task-id is required with --transcript", file=sys.stderr)
            return 2
        transcript = Path(args.transcript).read_text(encoding="utf-8")
        row = rows_by_id.get(args.task_id)
        if not row:
            print(f"unknown task_id: {args.task_id}", file=sys.stderr)
            return 2
        judge = row["judge"]
        checks = judge["checks"] if isinstance(judge, dict) else []
        failures = evaluate_checks(transcript, checks if isinstance(checks, list) else [])
        if failures:
            print(f"FAIL {args.task_id}:")
            for failure in failures:
                print(f"- {failure}")
            return 1
        print(f"PASS {args.task_id}")

    if errors:
        print("\nDataset validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    if not args.transcript:
        print("\nSkillopt datasets look valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
