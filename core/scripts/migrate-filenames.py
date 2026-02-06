#!/usr/bin/env python3
"""
Migrate session filenames to include sequential ordering numbers.

Pattern: yyyy-MM-dd-XX-<title>.md
Where XX is 00, 01, 02... based on file creation time within the same date.

Files that are identical except for "-plan" suffix share the same XX number.
For ordering paired files, use the earliest creation time between them.
"""

import os
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass


@dataclass
class FileInfo:
    path: Path
    date: str
    base_title: str  # title without -plan suffix
    has_plan_suffix: bool
    ctime: float

    @property
    def title(self) -> str:
        return f"{self.base_title}-plan" if self.has_plan_suffix else self.base_title


def parse_filename(path: Path) -> FileInfo | None:
    """Parse a session filename and extract components."""
    name = path.stem  # filename without .md

    # Match: yyyy-MM-dd-<title> or yyyy-MM-dd-XX-<title>
    # We want to handle both old format and potentially already-migrated files
    match = re.match(r'^(\d{4}-\d{2}-\d{2})(?:-(\d{2}))?-(.+)$', name)
    if not match:
        return None

    date = match.group(1)
    # group(2) would be existing XX number, we ignore it for re-migration
    title = match.group(3) if match.group(2) is None else match.group(3)

    # If there was an XX number, reconstruct the title
    if match.group(2) is not None:
        title = match.group(3)
    else:
        title = match.group(3)

    # Check for -plan suffix
    has_plan_suffix = title.endswith('-plan')
    base_title = title[:-5] if has_plan_suffix else title

    # Get file creation time (or modification time as fallback)
    stat = path.stat()
    # On Linux, st_ctime is metadata change time, st_mtime is modification time
    # We'll use st_mtime as it's more reliable for "when content was created"
    ctime = stat.st_mtime

    return FileInfo(
        path=path,
        date=date,
        base_title=base_title,
        has_plan_suffix=has_plan_suffix,
        ctime=ctime
    )


def group_by_date_and_base(files: list[FileInfo]) -> dict[str, dict[str, list[FileInfo]]]:
    """Group files by date, then by base_title."""
    result: dict[str, dict[str, list[FileInfo]]] = {}

    for f in files:
        if f.date not in result:
            result[f.date] = {}
        if f.base_title not in result[f.date]:
            result[f.date][f.base_title] = []
        result[f.date][f.base_title].append(f)

    return result


def get_earliest_time(files: list[FileInfo]) -> float:
    """Get the earliest creation time from a group of files."""
    return min(f.ctime for f in files)


def generate_new_name(date: str, seq: int, title: str) -> str:
    """Generate new filename with sequence number."""
    return f"{date}-{seq:02d}-{title}.md"


def main():
    sessions_dir = Path(__file__).parent

    # Find all .md files (excluding this script and any non-session files)
    md_files = [f for f in sessions_dir.glob("*.md") if f.name != "migrate-filenames.py"]

    # Parse all files
    parsed = []
    for f in md_files:
        info = parse_filename(f)
        if info:
            parsed.append(info)
        else:
            print(f"WARNING: Could not parse filename: {f.name}")

    # Group by date and base_title
    grouped = group_by_date_and_base(parsed)

    # Generate rename operations
    renames: list[tuple[Path, str]] = []

    for date in sorted(grouped.keys()):
        base_titles = grouped[date]

        # Sort base_titles by earliest creation time of their file group
        sorted_bases = sorted(
            base_titles.keys(),
            key=lambda bt: get_earliest_time(base_titles[bt])
        )

        # Assign sequence numbers
        for seq, base_title in enumerate(sorted_bases):
            files_in_group = base_titles[base_title]

            for f in files_in_group:
                new_name = generate_new_name(date, seq, f.title)
                if f.path.name != new_name:
                    renames.append((f.path, new_name))

    # Print planned renames
    if not renames:
        print("No renames needed.")
        return

    print("Planned renames:")
    print("-" * 80)
    for old_path, new_name in sorted(renames, key=lambda x: x[0].name):
        print(f"  {old_path.name}")
        print(f"    -> {new_name}")
        print()

    # Ask for confirmation
    response = input("Proceed with renames? [y/N]: ")
    if response.lower() != 'y':
        print("Aborted.")
        return

    # Execute renames
    for old_path, new_name in renames:
        new_path = old_path.parent / new_name
        old_path.rename(new_path)
        print(f"Renamed: {old_path.name} -> {new_name}")

    print(f"\nDone. Renamed {len(renames)} files.")


if __name__ == "__main__":
    main()
