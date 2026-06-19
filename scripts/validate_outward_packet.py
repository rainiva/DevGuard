#!/usr/bin/env python3
"""Validate DevGuard outward packet shape."""
from __future__ import annotations
import argparse
import sys

BLOCKS = [
    "## Project Understanding Summary",
    "## Impact Analysis Summary",
    "## Rule-Loading Manifest",
]

def validate_text(text: str, mode: str = "FAST", status: str = "ALLOW") -> list[str]:
    errors: list[str] = []
    stripped = text.strip()
    if not stripped:
        return ["empty packet"]
    if stripped.splitlines()[0] != "## Execution Summary":
        errors.append("must start with ## Execution Summary")
    if status == "INQUIRY":
        if "## Inquiry Note" not in stripped:
            errors.append("INQUIRY needs Inquiry Note")
        if "## Task Contract Summary" in stripped:
            errors.append("INQUIRY must not include TCS")
        return errors
    if mode == "LITE" and "## Task Contract Summary" in stripped:
        errors.append("LITE must not emit TCS")
    elif mode in {"FAST", "STANDARD", "STRICT"} and status in {"ALLOW", "ALLOW_WITH_WARNINGS"}:
        if "## Task Contract Summary" not in stripped:
            errors.append("FAST+ needs TCS")
    for block in BLOCKS:
        if block in stripped:
            errors.append("T1 must not emit " + block)
    return errors

def self_test() -> int:
    if validate_text("## Execution Summary\n- Status: ALLOW\n\n## Task Contract Summary\n- Goal: g\n"):
        return 1
    if not validate_text("## Execution Summary\n\n## Task Contract Summary\n", status="INQUIRY"):
        return 1
    return 0

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text")
    parser.add_argument("--mode", default="FAST")
    parser.add_argument("--status", default="ALLOW")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.text:
        return 2
    errors = validate_text(args.text, args.mode, args.status)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    print("OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
