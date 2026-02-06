#!/usr/bin/env python3
"""
Move files between ai-context subdirectories and update all references.

Usage:
    python move-context-files.py <source> <dest> [<source> <dest> ...]
    python move-context-files.py --execute <source> <dest> [<source> <dest> ...]

Paths are relative to ai-context/. Example:
    python move-context-files.py reference/custom-gradle-plugins external/custom-gradle-plugins

Dry-run by default. Pass --execute to perform changes.
"""

import argparse
import shutil
import sys
from pathlib import Path

AI_CONTEXT_DIR = Path(__file__).resolve().parent.parent
SCAN_EXTENSIONS = {".md", ".yaml", ".yml", ".txt", ".java", ".scala"}
EXCLUDE_DIRS = {"_darcs", "archive"}


def parse_move_specs(args: list[str]) -> list[tuple[str, str]]:
    if len(args) % 2 != 0:
        print("Error: move specs must be pairs of <source> <dest>", file=sys.stderr)
        sys.exit(1)
    return [(args[i], args[i + 1]) for i in range(0, len(args), 2)]


def scannable_files() -> list[Path]:
    files = []
    for path in AI_CONTEXT_DIR.rglob("*"):
        if any(excluded in path.parts for excluded in EXCLUDE_DIRS):
            continue
        if path.is_file() and path.suffix in SCAN_EXTENSIONS:
            files.append(path)
    return sorted(files)


def find_references(
    files: list[Path], source: str
) -> list[tuple[Path, int, str]]:
    """Find lines referencing source path. Returns (file, line_num, line_text)."""
    # Match both "ai-context/reference/foo" and bare "reference/foo"
    patterns = [f"ai-context/{source}", source]
    matches = []
    for path in files:
        try:
            lines = path.read_text().splitlines()
        except (UnicodeDecodeError, PermissionError, FileNotFoundError):
            continue
        for i, line in enumerate(lines, 1):
            if any(p in line for p in patterns):
                matches.append((path, i, line))
    return matches


def update_references(
    files: list[Path], source: str, dest: str
) -> list[tuple[Path, int]]:
    """Replace source references with dest in all files. Returns (file, count)."""
    replacements = [
        (f"ai-context/{source}", f"ai-context/{dest}"),
        (source, dest),
    ]
    updated = []
    for path in files:
        try:
            content = path.read_text()
        except (UnicodeDecodeError, PermissionError, FileNotFoundError):
            continue
        new_content = content
        for old, new in replacements:
            new_content = new_content.replace(old, new)
        if new_content != content:
            path.write_text(new_content)
            count = sum(
                content.count(old) - new_content.count(old)
                for old, _ in replacements
            )
            updated.append((path, content.count(source) - new_content.count(source)))
    return updated


def main():
    parser = argparse.ArgumentParser(
        description="Move ai-context files and update references."
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually perform moves and updates (default is dry-run)",
    )
    parser.add_argument(
        "specs",
        nargs="+",
        help="Pairs of <source> <dest> paths relative to ai-context/",
    )
    args = parser.parse_args()
    specs = parse_move_specs(args.specs)
    files = scannable_files()

    for source, dest in specs:
        source_path = AI_CONTEXT_DIR / source
        dest_path = AI_CONTEXT_DIR / dest

        print(f"\n{'=' * 60}")
        print(f"Move: {source} -> {dest}")
        print(f"{'=' * 60}")

        if not source_path.exists():
            print(f"  ERROR: source does not exist: {source_path}")
            continue

        if dest_path.exists():
            print(f"  ERROR: destination already exists: {dest_path}")
            continue

        # Show what will be moved
        if source_path.is_dir():
            children = sorted(source_path.rglob("*"))
            print(f"  Directory with {len([c for c in children if c.is_file()])} file(s)")
        else:
            print(f"  File: {source_path.name}")

        # Find references
        refs = find_references(files, source)
        if refs:
            print(f"\n  References found ({len(refs)}):")
            for path, line_num, line_text in refs:
                rel = path.relative_to(AI_CONTEXT_DIR)
                print(f"    {rel}:{line_num}: {line_text.strip()}")
        else:
            print("\n  No references found.")

        if args.execute:
            # Move file/directory
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(dest_path))
            print(f"\n  Moved: {source} -> {dest}")

            # Update references
            updated = update_references(files, source, dest)
            if updated:
                print(f"  Updated references in {len(updated)} file(s):")
                for path, count in updated:
                    rel = path.relative_to(AI_CONTEXT_DIR)
                    print(f"    {rel}")
        else:
            print("\n  [DRY RUN] No changes made.")

    if not args.execute:
        print(f"\n{'=' * 60}")
        print("Dry run complete. Pass --execute to perform changes.")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'=' * 60}")
        print("Done. Remember to manually update 0-index.md section listings.")
        print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
