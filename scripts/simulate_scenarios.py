#!/usr/bin/env python3
"""Simulate DevGuard outward transcripts for skillopt scenarios and smoke cases."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def load_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


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
            failures.append(f"unsupported op: {op}")
    return failures


def run_manifest_smokes(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    gen = skill_dir / "scripts/generate_rule_loading_manifest.py"
    loaded = ["--loaded", "meta|task-router|references/task-routing.md|why|summary"]
    cases = [
        (
            "lite-summary",
            [
                "--format", "summary", "--task", "README typo", "--task-type", "change",
                "--execution-mode", "LITE", "--status", "ALLOW", "--next-step", "apply edit",
            ] + loaded,
            ["## Execution Summary", "LITE"],
            ["## Task Contract Summary"],
        ),
        (
            "fast-summary",
            [
                "--format", "summary", "--task", "tiny fix", "--task-type", "change",
                "--execution-mode", "FAST", "--status", "ALLOW", "--next-step", "code",
                "--contract-goal", "fix", "--contract-scope", "one file",
                "--contract-tests", "check", "--contract-acceptance-criteria", "done",
            ] + loaded,
            ["## Execution Summary", "## Task Contract Summary", "FAST"],
            [],
        ),
        (
            "strict-risk",
            [
                "--format", "risk", "--task", "installer", "--task-type", "release",
                "--execution-mode", "STRICT", "--status", "ALLOW_WITH_WARNINGS",
                "--next-step", "validate", "--risk-focus", "rollback",
                "--risk-why", "release surface", "--risk-extra-checks", "release-check",
                "--contract-goal", "hotfix", "--contract-scope", "installer",
                "--contract-tests", "failing test", "--contract-acceptance-criteria", "rollback ok",
            ] + loaded,
            ["## Execution Summary", "## Risk Note", "## Task Contract Summary"],
            [],
        ),
        (
            "exception-blocked",
            [
                "--format", "exception", "--task", "missing rule", "--task-type", "bugfix",
                "--execution-mode", "STANDARD", "--status", "BLOCKED",
                "--next-step", "load missing rule",
                "--exception-reason", "required project rule is missing",
                "--exception-missing", "example-desktop project rule",
                "--exception-required", "load example-desktop project rule before continuing",
            ],
            ["## Execution Summary", "## Exception Note"],
            [],
        ),
    ]
    for name, args, must_have, must_not in cases:
        proc = subprocess.run(
            [sys.executable, str(gen), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
            cwd=str(skill_dir),
        )
        if proc.returncode != 0:
            errors.append(f"{name}: manifest failed: {proc.stderr.strip()}")
            continue
        for phrase in must_have:
            if phrase not in proc.stdout:
                errors.append(f"{name}: missing {phrase!r}")
        for phrase in must_not:
            if phrase in proc.stdout:
                errors.append(f"{name}: forbidden {phrase!r} present")
    return errors


def main() -> int:
    skill_dir = SKILL_DIR
    fixtures_path = skill_dir / "skillopt/simulate_fixtures.json"
    if not fixtures_path.exists():
        print(f"Missing {fixtures_path}. Run scripts/gen_skillopt.py after adding fixtures.")
        return 2
    fixtures = json.loads(fixtures_path.read_text(encoding="utf-8"))
    golden: dict[str, str] = fixtures["golden"]
    negative: list[dict[str, object]] = fixtures["negative"]

    benchmark = load_jsonl(skill_dir / "skillopt/benchmark.jsonl")
    held_out = load_jsonl(skill_dir / "skillopt/held-out.jsonl")
    all_rows = benchmark + held_out

    print("=== DevGuard Scenario Simulation ===\n")
    passed = 0
    failed = 0

    print("-- Golden transcripts vs skillopt judges --")
    for row in all_rows:
        task_id = str(row["task_id"])
        checks = row["judge"]["checks"]  # type: ignore[index]
        transcript = golden.get(task_id)
        if transcript is None:
            print(f"SKIP {task_id}: no golden transcript")
            continue
        failures = evaluate_checks(transcript, checks)
        if failures:
            failed += 1
            print(f"FAIL {task_id}")
            for item in failures:
                print(f"  - {item}")
        else:
            passed += 1
            print(f"PASS {task_id} ({len(transcript)} chars)")

    print("\n-- Negative cases (expect judge failure) --")
    for case in negative:
        label = str(case["label"])
        task_id = str(case["task_id"])
        if "transcript" in case:
            bad = str(case["transcript"])
        elif "suffix" in case:
            bad = golden[task_id] + str(case["suffix"])
        else:
            old, new = case["replace"]
            bad = golden[task_id].replace(str(old), str(new))
        row = next(r for r in all_rows if r["task_id"] == task_id)
        checks = row["judge"]["checks"]  # type: ignore[index]
        failures = evaluate_checks(bad, checks)
        if failures:
            passed += 1
            print(f"PASS {label}: rejected ({failures[0]})")
        else:
            failed += 1
            print(f"FAIL {label}: bad transcript accepted")

    print("\n-- Manifest generator smokes --")
    manifest_errors = run_manifest_smokes(skill_dir)
    if manifest_errors:
        failed += len(manifest_errors)
        for err in manifest_errors:
            print(f"FAIL {err}")
    else:
        passed += 4
        print("PASS lite, fast, strict-risk, exception manifest smokes")

    print("\n-- Skillopt dataset validation --")
    judge = subprocess.run(
        [
            sys.executable,
            str(skill_dir / "scripts/run_skillopt_judge.py"),
            "--skill-dir",
            str(skill_dir),
            "--dataset",
            "all",
            "--minimum-rows",
            "14",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if judge.returncode == 0:
        passed += 1
        print(judge.stdout.strip())
    else:
        failed += 1
        print(judge.stdout)
        print(judge.stderr)

    print("\n-- Bundle check --")
    bundle = subprocess.run(
        [sys.executable, str(skill_dir / "scripts/check_devguard_bundle.py"), "--skill-dir", str(skill_dir)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if bundle.returncode == 0:
        passed += 1
        print("PASS check_devguard_bundle.py")
    else:
        failed += 1
        print("FAIL check_devguard_bundle.py")
        print((bundle.stdout + bundle.stderr)[-2500:])

    print(f"\n=== Summary: {passed} passed, {failed} failed ===")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
