#!/usr/bin/env python3
"""Generate skillopt benchmark.jsonl and held-out.jsonl in UTF-8."""

from __future__ import annotations

import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
DEVGUARD_PATH = str(SKILL_DIR)
INVOCATION = f"Use $devguard at {DEVGUARD_PATH} to "


def entry(task_id: str, body: str, checks: list[dict[str, object]]) -> dict[str, object]:
    return {
        "task_id": task_id,
        "task": INVOCATION + body,
        "judge": {"kind": "rule", "checks": checks},
    }


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    benchmark = [
        entry(
            "feature-normal",
            "route a medium-risk feature request in this repo. Load only the minimum required rules, "
            "keep the default outward output to Execution Summary plus Task Contract Summary, and "
            "freeze the Task Contract before coding. Do not write code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "max_chars", "arg": 12000},
                {"op": "not_contains", "arg": "Project Understanding Summary"},
                {"op": "not_contains", "arg": "Rule-Loading Manifest"},
            ],
        ),
        entry(
            "refactor-compact",
            "route a medium-risk multi-file refactor in this repo. Prefer CodeGraph first for project "
            "understanding, keep outward output compact, and do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "contains", "arg": "CodeGraph"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
        entry(
            "bugfix-evidence",
            "handle a bug report about flaky tests. Reproduce first, load only the needed rules, and "
            "stop if the evidence chain is weak. Do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "contains", "arg": "evidence"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
        entry(
            "review-only",
            "review a medium-risk change set. Mirror implementation-side rules into review, list "
            "findings first, and do not modify code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "contains", "arg": "finding"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
        entry(
            "high-risk-installer",
            "route a hotfix for installer recovery replay gating. Treat rollback, recoverability, "
            "release validation, and focused failing tests as first-class concerns, but keep outward "
            "output compact unless full detail is explicitly required. Do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Risk Note"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
        entry(
            "anomaly-missing-rule",
            "route this desktop WPF scrollbar bugfix. Keep the outward output compact, but stop if "
            "required rules, playbooks, or rule paths are missing. Do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Exception Note"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
        entry(
            "platform-wpf",
            "route this WPF control-template fix. Confirm official WPF control-template, "
            "ResourceDictionary, Dispatcher, and DPI guidance before impact analysis, keep outward "
            "output compact, and stop if the implementation would violate official constraints. Do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
        entry(
            "ui-change",
            "route a UI implementation task for a settings screen change. Require real user operation "
            "path verification in the Task Contract, keep outward output compact, and do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "contains", "arg": "user"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
        entry(
            "ai-tool-calling",
            "route this AI feature task. Treat tool calls, memory boundaries, observability, and cost "
            "controls as first-class routing factors, keep outward output compact, and freeze the Task "
            "Contract before coding. Do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "contains", "arg": "cost"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
        entry(
            "repair-failure-reroute",
            "handle a bug that already failed repair twice without new evidence. Enter failure "
            "retrospective, reroute, and do not attempt a third fix without a new validation plan. "
            "Do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "contains", "arg": "retrospective"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
        entry(
            "codegraph-stale",
            "route a multi-file change. Verify CodeGraph index freshness before structural queries, "
            "refresh or rebuild the index if needed, and only then continue into impact analysis. "
            "Do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "contains", "arg": "CodeGraph"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
        entry(
            "fast-s1-tiny",
            "route a tiny single-file typo fix in one local file with no contract, auth, or data risk. "
            "Use FAST mode, keep outward output to Execution Summary plus Task Contract Summary only, "
            "and do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "contains", "arg": "FAST"},
                {"op": "max_chars", "arg": 8000},
            ],
        ),
        entry(
            "lite-typo-execute",
            "route a single-file typo fix in one local README with no auth, data, or platform risk. "
            "Use LITE mode, freeze Slice inside Execution Summary, do not emit Task Contract Summary, "
            "and do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "contains", "arg": "LITE"},
                {"op": "contains", "arg": "Slice"},
                {"op": "not_contains", "arg": "Task Contract Summary"},
                {"op": "max_chars", "arg": 6000},
            ],
        ),
        entry(
            "lite-upgrade-fast",
            "route this auth login bugfix with failing reproduction evidence. Keep outward output compact, "
            "upgrade off LITE if needed, and do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "contains", "arg": "FAST"},
                {"op": "max_chars", "arg": 12000},
            ],
        ),
    ]

    held_out = [
        entry(
            "regression-normal",
            "route this medium-risk feature task. Keep the default outward output compact, and freeze "
            "the Task Contract before coding. Do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "max_chars", "arg": 8000},
            ],
        ),
        entry(
            "regression-high-risk",
            "route a hotfix for installer recovery replay gating. Treat rollback and release validation "
            "as first-class concerns, keep outward output compact, and do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Risk Note"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "max_chars", "arg": 10000},
            ],
        ),
        entry(
            "regression-platform",
            "route a WPF control-template fix. Confirm official WPF guidance before impact analysis, "
            "keep outward output compact, and do not code.",
            [
                {"op": "section_present", "arg": "Execution Summary"},
                {"op": "section_present", "arg": "Task Contract Summary"},
                {"op": "max_chars", "arg": 10000},
            ],
        ),
    ]

    skillopt = SKILL_DIR / "skillopt"
    skillopt.mkdir(exist_ok=True)
    write_jsonl(skillopt / "benchmark.jsonl", benchmark)
    write_jsonl(skillopt / "held-out.jsonl", held_out)
    print(f"Wrote {len(benchmark)} benchmark rows and {len(held_out)} held-out rows to {skillopt}")
    write_judge_script(SKILL_DIR / "scripts" / "run_skillopt_judge.py")
    print("Wrote scripts/run_skillopt_judge.py")
    write_simulate_scenarios(SKILL_DIR / "scripts" / "simulate_scenarios.py")
    print("Wrote scripts/simulate_scenarios.py")


def write_judge_script(path: Path) -> None:
    path.write_text(
        '''#!/usr/bin/env python3
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
        print("\\nDataset validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    if not args.transcript:
        print("\\nSkillopt datasets look valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
        encoding="utf-8",
        newline="\n",
    )


def write_simulate_scenarios(path: Path) -> None:
    path.write_text(
        '''#!/usr/bin/env python3
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

    print("=== DevGuard Scenario Simulation ===\\n")
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

    print("\\n-- Negative cases (expect judge failure) --")
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

    print("\\n-- Manifest generator smokes --")
    manifest_errors = run_manifest_smokes(skill_dir)
    if manifest_errors:
        failed += len(manifest_errors)
        for err in manifest_errors:
            print(f"FAIL {err}")
    else:
        passed += 4
        print("PASS lite, fast, strict-risk, exception manifest smokes")

    print("\\n-- Skillopt dataset validation --")
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

    print("\\n-- Bundle check --")
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

    print(f"\\n=== Summary: {passed} passed, {failed} failed ===")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
