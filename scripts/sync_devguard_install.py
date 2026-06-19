#!/usr/bin/env python3
"""Sync DevGuard canonical bundle to install targets."""
from __future__ import annotations
import argparse
import shutil
from pathlib import Path

CANONICAL = Path(__file__).resolve().parents[1]
TARGETS = {"cursor": Path.home() / ".cursor" / "skills" / "devguard"}

def sync_tree(src: Path, dst: Path, dry_run: bool) -> None:
    if not dst.exists() and not dry_run:
        dst.mkdir(parents=True, exist_ok=True)
    for path in src.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue
        rel = path.relative_to(src)
        target = dst / rel
        print(f"{'DRY ' if dry_run else ''}copy {rel}")
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--targets", default="cursor")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    for name in [x.strip() for x in a.targets.split(",") if x.strip()]:
        if name not in TARGETS:
            print(f"unknown target: {name}")
            return 1
        print(f"sync {CANONICAL} -> {TARGETS[name]}")
        sync_tree(CANONICAL, TARGETS[name], a.dry_run)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
