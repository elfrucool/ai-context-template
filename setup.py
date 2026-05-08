#!/usr/bin/env python3
"""
ai-context-template setup script

Usage: python3 setup.py <target-project-path> [OPTIONS]

Initializes ai-context directory structure with core files, skills linking, and
optional Java TDD module support. Handles collisions in skills directory with
configurable behavior (overwrite, skip, backup, prompt).
"""

import argparse
import pathlib
import shutil
import os
import sys
import subprocess
import datetime
from typing import Optional, List, Tuple


# ──────────────────────────────────────────────────────────────────────
# Configuration and Constants
# ──────────────────────────────────────────────────────────────────────

# Detect interactivity: running in terminal with stdin/stdout as TTY
INTERACTIVE = sys.stdin.isatty() and sys.stdout.isatty()

# Script directory (location of this file)
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent

# Subdirectories to create in ai-context/
SUBDIRS = [
    "guidelines",
    "architecture",
    "briefs",
    "scripts",
    "sessions",
    "til",
    "reference",
    "external",
    "test-data",
    "archive",
    "skills",
]

# Core files to copy
CORE_FILES = [
    ("core/CLAUDE.md", "ai-context/CLAUDE.md"),
    ("core/0-index.md", "ai-context/0-index.md"),
    ("core/guidelines/DEVELOPMENT_PROCESS.md", "ai-context/guidelines/"),
    ("core/guidelines/PR_DESCRIPTION_GUIDELINES.md", "ai-context/guidelines/"),
    ("core/guidelines/BRIEF_CREATION_GUIDELINES.md", "ai-context/guidelines/"),
    ("core/architecture/00-architecture-index.md", "ai-context/architecture/"),
    ("core/architecture/01-domain-explanation.md", "ai-context/architecture/"),
    ("core/briefs/00-about-briefs.md", "ai-context/briefs/"),
    ("core/scripts/move-context-files.py", "ai-context/scripts/"),
    ("core/scripts/migrate-filenames.py", "ai-context/scripts/"),
]

# Java TDD module files
JAVA_FILES = [
    ("modules/java-tdd/JAVA_UNIT_TESTING_GUIDELINES.md", "ai-context/guidelines/"),
    (
        "modules/java-tdd/JAVA_TEST_DATA_CREATION_GUIDELINES.md",
        "ai-context/guidelines/",
    ),
]

# Java TDD patches: (filename, old_text, new_text)
JAVA_PATCHES = [
    (
        "ai-context/guidelines/DEVELOPMENT_PROCESS.md",
        "- See language-specific guidelines in `guidelines/` if available",
        """- `JAVA_UNIT_TESTING_GUIDELINES.md` - TDD approach, test structure, assertions
- `JAVA_TEST_DATA_CREATION_GUIDELINES.md` - Test data patterns, records, builders""",
    ),
    (
        "ai-context/guidelines/DEVELOPMENT_PROCESS.md",
        "Implementation follows guidelines defined in language-specific files in `guidelines/` if available.",
        """Implementation follows guidelines defined in:
- `JAVA_UNIT_TESTING_GUIDELINES.md` - Test-first development, incremental approach
- `JAVA_TEST_DATA_CREATION_GUIDELINES.md` - Creating reusable test data""",
    ),
    (
        "ai-context/0-index.md",
        "<!-- Add language-specific guidelines here when installed (e.g., JAVA_*.md) -->",
        """- `JAVA_UNIT_TESTING_GUIDELINES.md` - Test structure, incremental TDD, assertions
- `JAVA_TEST_DATA_CREATION_GUIDELINES.md` - Test data records, builders""",
    ),
    (
        "ai-context/CLAUDE.md",
        "3. Coding patterns → see language-specific guidelines in `ai-context/guidelines/` if available",
        "3. Coding patterns → `ai-context/guidelines/JAVA_*.md`",
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Argument Parsing
# ──────────────────────────────────────────────────────────────────────


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="setup.py",
        description="ai-context-template setup script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
DEFAULT BEHAVIOR:
  Running in terminal (interactive):
    → Prompts for skill collisions
    → Prompts for .gitignore changes

  Running piped/in automation (non-interactive):
    → Skips skill collisions (defensive)
    → Skips .gitignore changes (defensive)

SPECIAL ACTIONS:
  --print-prompt: Print AI agent guidance prompt and exit
    Useful for copying the setup assistance prompt separately

FLAG PRECEDENCE:
  Explicit flags (--skills-*, --gitignore-*) take highest priority
  Mode flags (--auto, --interactive) override auto-detection
  Auto-detection (environment) is used as fallback

EXIT CODES:
  0: Success
  1: Partial success (some operations skipped due to collisions)
  2: Error (invalid flags, missing path, permissions, etc.)
""",
    )

    # Positional argument
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Target project path",
    )

    # Optional flags
    parser.add_argument(
        "--java",
        "--tdd",
        action="store_true",
        dest="java",
        help="Include Java unit testing guidelines",
    )

    # Skills behavior group (mutually exclusive)
    skills_group = parser.add_mutually_exclusive_group()
    skills_group.add_argument(
        "--skills-overwrite",
        action="store_true",
        help="Force overwrite existing skills",
    )
    skills_group.add_argument(
        "--skills-skip",
        action="store_true",
        help="Force skip existing skills",
    )
    skills_group.add_argument(
        "--skills-backup",
        action="store_true",
        help="Backup existing skills, then overwrite",
    )
    skills_group.add_argument(
        "--skills-prompt",
        action="store_true",
        help="Force prompt for collisions",
    )

    # Gitignore behavior group (mutually exclusive)
    gitignore_group = parser.add_mutually_exclusive_group()
    gitignore_group.add_argument(
        "--gitignore-auto",
        action="store_true",
        help="Automatically add ai-context/ to .gitignore",
    )
    gitignore_group.add_argument(
        "--gitignore-skip",
        action="store_true",
        help="Skip .gitignore modification",
    )
    gitignore_group.add_argument(
        "--gitignore-prompt",
        action="store_true",
        help="Force prompt for .gitignore",
    )

    # Mode control group (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--auto",
        action="store_true",
        help="Defensive automation (skip collisions, skip darcs, prompt gitignore)",
    )
    mode_group.add_argument(
        "--interactive",
        action="store_true",
        help="Force interactive mode (prompt for everything)",
    )

    # VCS behavior group (mutually exclusive with mode)
    vcs_group = parser.add_mutually_exclusive_group()
    vcs_group.add_argument(
        "--darcs-auto",
        action="store_true",
        help="Initialize darcs if available (default)",
    )
    vcs_group.add_argument(
        "--darcs-skip",
        action="store_true",
        help="Skip darcs initialization",
    )

    # Tracking behavior group (mutually exclusive with mode)
    tracking_group = parser.add_mutually_exclusive_group()
    tracking_group.add_argument(
        "--tracking-ignore",
        action="store_true",
        help="Add ai-context/ to .gitignore",
    )
    tracking_group.add_argument(
        "--tracking-track",
        action="store_true",
        help="Track ai-context/ in parent git (no .gitignore)",
    )
    tracking_group.add_argument(
        "--tracking-prompt",
        action="store_true",
        help="Prompt for .gitignore modification",
    )

    # Convenience flags (mutually exclusive with each other and above groups)
    convenience_group = parser.add_mutually_exclusive_group()
    convenience_group.add_argument(
        "--shared",
        action="store_true",
        help="Track in parent git, no darcs (for team workflows)",
    )
    convenience_group.add_argument(
        "--standalone",
        action="store_true",
        help="Use darcs if avail, ignore in git (local-only)",
    )

    # Special actions group (mutually exclusive with mode)
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print AI agent guidance prompt and exit",
    )

    return parser


# ──────────────────────────────────────────────────────────────────────
# Behavior Resolution
# ──────────────────────────────────────────────────────────────────────


def resolve_skills_behavior(args) -> str:
    """Resolve skills collision behavior based on flags and environment."""
    if args.skills_overwrite:
        return "overwrite"
    elif args.skills_skip:
        return "skip"
    elif args.skills_backup:
        return "backup"
    elif args.skills_prompt:
        return "prompt"
    elif args.auto:
        return "skip"
    elif args.interactive:
        return "prompt"
    else:
        # Default based on interactivity
        return "prompt" if INTERACTIVE else "skip"


def resolve_gitignore_behavior(args) -> str:
    """Resolve gitignore behavior based on flags and environment."""
    if args.gitignore_auto:
        return "auto"
    elif args.gitignore_skip:
        return "skip"
    elif args.gitignore_prompt:
        return "prompt"
    elif args.auto:
        return "skip"
    elif args.interactive:
        return "prompt"
    else:
        # Default based on interactivity
        return "prompt" if INTERACTIVE else "skip"


def resolve_darcs_behavior(args) -> str:
    """Resolve darcs behavior based on flags."""
    if args.darcs_skip:
        return "skip"
    elif args.darcs_auto:
        return "auto"
    elif args.shared:
        return "skip"
    elif args.standalone:
        return "auto"
    elif args.auto:
        return "auto"
    else:
        # Default: try darcs if available
        return "auto"


def resolve_tracking_behavior(args) -> str:
    """Resolve tracking behavior based on flags."""
    if args.tracking_ignore:
        return "ignore"
    elif args.tracking_track:
        return "track"
    elif args.tracking_prompt:
        return "prompt"
    elif args.shared:
        return "track"
    elif args.standalone:
        return "ignore"
    elif args.auto:
        return "prompt"
    elif args.interactive:
        return "prompt"
    else:
        # Default based on interactivity
        return "prompt" if INTERACTIVE else "skip"


# ──────────────────────────────────────────────────────────────────────
# Validation
# ──────────────────────────────────────────────────────────────────────


def validate_target(target: Optional[str]) -> pathlib.Path:
    """Validate and resolve target path to absolute path.

    Returns:
        Absolute path to target directory.

    Raises:
        SystemExit: With code 2 if target is invalid.
    """
    if target is None:
        print("Error: target path is required", file=sys.stderr)
        sys.exit(2)

    try:
        target_path = pathlib.Path(target).resolve()
    except (OSError, ValueError) as e:
        print(f"Error: cannot resolve target path: {e}", file=sys.stderr)
        sys.exit(2)

    if not target_path.is_dir():
        print(
            f"Error: target path does not exist or is not a directory: {target}",
            file=sys.stderr,
        )
        sys.exit(2)

    return target_path


# ──────────────────────────────────────────────────────────────────────
# File Operations
# ──────────────────────────────────────────────────────────────────────


def create_directory_structure(target: pathlib.Path) -> pathlib.Path:
    """Create ai-context directory and subdirectories.

    Returns:
        Path to created ai-context directory.

    Raises:
        SystemExit: With code 2 if ai-context already exists.
    """
    ai_context = target / "ai-context"

    if ai_context.exists():
        print(
            f"Error: {ai_context} already exists. Aborting to avoid overwriting.",
            file=sys.stderr,
        )
        sys.exit(2)

    print(f"Creating ai-context/ in {target} ...")

    for subdir in SUBDIRS:
        (ai_context / subdir).mkdir(parents=True, exist_ok=True)

    return ai_context


def copy_core_files(ai_context: pathlib.Path) -> None:
    """Copy core files from SCRIPT_DIR/core to ai_context."""
    for src_rel, dst_rel in CORE_FILES:
        src = SCRIPT_DIR / src_rel
        dst = ai_context.parent / dst_rel

        if not src.exists():
            print(f"Warning: source file not found: {src}", file=sys.stderr)
            continue

        # If destination is a directory, copy file into it
        if dst_rel.endswith("/"):
            dst = ai_context.parent / dst_rel / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src, dst)


def copy_skills(ai_context: pathlib.Path) -> None:
    """Copy skills directory from core/skills to ai-context/skills."""
    src_skills = SCRIPT_DIR / "core" / "skills"
    dst_skills = ai_context / "skills"

    if src_skills.exists():
        for skill in src_skills.iterdir():
            if skill.is_dir():
                dst_skill = dst_skills / skill.name
                if dst_skill.exists():
                    shutil.rmtree(dst_skill)
                shutil.copytree(skill, dst_skill)


def install_java_tdd_module(ai_context: pathlib.Path) -> None:
    """Install Java TDD module files and apply patches."""
    print("Installing Java TDD module ...")

    # Copy Java TDD files
    for src_rel, dst_rel in JAVA_FILES:
        src = SCRIPT_DIR / src_rel
        dst = ai_context.parent / dst_rel

        if not src.exists():
            print(f"Warning: Java TDD file not found: {src}", file=sys.stderr)
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    # Apply patches
    for filename, old_text, new_text in JAVA_PATCHES:
        filepath = ai_context.parent / filename
        if filepath.exists():
            content = filepath.read_text()
            if old_text in content:
                new_content = content.replace(old_text, new_text)
                filepath.write_text(new_content)


def _create_symlink_stub(path: pathlib.Path, rel_target: str, label: str) -> None:
    """Create a symlink at path pointing to rel_target, skip if already present."""
    if path.is_symlink():
        print(f"Skipped {label} (symlink already exists)")
    elif path.exists():
        print(f"Skipped {label} (regular file already exists)")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(rel_target)
        print(f"Created {label} (symlink → {rel_target})")


def copy_root_stubs(target: pathlib.Path) -> None:
    """Create symlinks at root level pointing to ai-context/CLAUDE.md."""
    _create_symlink_stub(target / "CLAUDE.md", "ai-context/CLAUDE.md", "CLAUDE.md")
    _create_symlink_stub(target / "AGENTS.md", "ai-context/CLAUDE.md", "AGENTS.md")
    _create_symlink_stub(
        target / ".windsurf" / "rules.md",
        "../ai-context/CLAUDE.md",
        ".windsurf/rules.md",
    )


# ──────────────────────────────────────────────────────────────────────
# Skills Linking
# ──────────────────────────────────────────────────────────────────────


def create_backup(source_dir: pathlib.Path, target_base: pathlib.Path) -> pathlib.Path:
    """Create timestamped backup of source directory.

    Returns:
        Path to created backup directory.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = target_base.parent / f"{target_base.name}.{timestamp}"

    counter = 1
    while backup_dir.exists():
        backup_dir = target_base.parent / f"{target_base.name}.{timestamp}-{counter}"
        counter += 1

    if source_dir.is_symlink():
        # Copy what the symlink points to
        shutil.copytree(source_dir.resolve(), backup_dir)
    else:
        # Copy directory recursively
        shutil.copytree(source_dir, backup_dir)

    return backup_dir


def link_skills_to_claude(
    target: pathlib.Path,
    ai_context: pathlib.Path,
    skills_behavior: str,
) -> Tuple[int, int, List[str], bool]:
    """Link skills from ai-context/skills to .claude/skills.

    Returns:
        Tuple of (linked_count, skipped_count, collision_names, partial_success)
    """
    print("Linking skills to .claude directory...")

    claude_dir = target / ".claude"
    claude_skills = claude_dir / "skills"
    source_skills = ai_context / "skills"

    linked_count = 0
    skipped_count = 0
    collisions = []
    partial_success = False

    # Create directories
    if not claude_dir.exists():
        claude_dir.mkdir(parents=True, exist_ok=True)
        print("  Created .claude directory")

    if not claude_skills.exists():
        claude_skills.mkdir(parents=True, exist_ok=True)
        print("  Created .claude/skills directory")

    # Link each skill
    if source_skills.exists():
        for skill_dir in sorted(source_skills.iterdir()):
            if not skill_dir.is_dir():
                continue

            skill_name = skill_dir.name
            target_link = claude_skills / skill_name

            # Check for collision
            if target_link.exists() or target_link.is_symlink():
                print(
                    f"  Collision detected: {skill_name} already exists in .claude/skills/"
                )

                if skills_behavior == "overwrite":
                    if target_link.is_symlink():
                        target_link.unlink()
                    else:
                        shutil.rmtree(target_link)
                    target_link.symlink_to(skill_dir)
                    print(f"    Overwrote {skill_name}")
                    linked_count += 1

                elif skills_behavior == "skip":
                    print(f"    Skipped {skill_name}")
                    skipped_count += 1
                    collisions.append(skill_name)
                    partial_success = True

                elif skills_behavior == "backup":
                    backup_dir = create_backup(target_link, target_link)
                    print(f"    Backed up {skill_name} to {backup_dir.name}")
                    if target_link.is_symlink():
                        target_link.unlink()
                    else:
                        shutil.rmtree(target_link)
                    target_link.symlink_to(skill_dir)
                    print(f"    Overwrote {skill_name} (backup created)")
                    linked_count += 1

                elif skills_behavior == "prompt":
                    if INTERACTIVE:
                        answer = (
                            input(f"  Overwrite {skill_name}? [y/N] ").strip().lower()
                        )
                        if answer in ("y", "yes"):
                            if target_link.is_symlink():
                                target_link.unlink()
                            else:
                                shutil.rmtree(target_link)
                            target_link.symlink_to(skill_dir)
                            print(f"    Overwrote {skill_name}")
                            linked_count += 1
                        else:
                            print(f"    Skipped {skill_name}")
                            skipped_count += 1
                            collisions.append(skill_name)
                            partial_success = True
                    else:
                        print(f"    Skipping {skill_name} (non-interactive mode)")
                        skipped_count += 1
                        collisions.append(skill_name)
                        partial_success = True
            else:
                # No collision, create symlink
                target_link.symlink_to(skill_dir)
                print(f"  Linked {skill_name}")
                linked_count += 1

    print(f"  Skills linking complete: {linked_count} linked, {skipped_count} skipped")

    return linked_count, skipped_count, collisions, partial_success


def link_skills_to_windsurf(
    target: pathlib.Path,
    ai_context: pathlib.Path,
    skills_behavior: str,
) -> Tuple[int, int, List[str], bool]:
    """Link skills as .md files into .windsurf/workflows/.

    Returns:
        Tuple of (linked_count, skipped_count, collision_names, partial_success)
    """
    print("Linking skills to .windsurf/workflows directory...")

    windsurf_dir = target / ".windsurf"
    windsurf_workflows = windsurf_dir / "workflows"
    source_skills = ai_context / "skills"

    linked_count = 0
    skipped_count = 0
    collisions = []
    partial_success = False

    # Create .windsurf/workflows directory if missing
    if not windsurf_workflows.exists():
        windsurf_workflows.mkdir(parents=True, exist_ok=True)
        print("  Created .windsurf/workflows directory")

    # Link each skill as a .md file
    if source_skills.exists():
        for skill_dir in sorted(source_skills.iterdir()):
            if not skill_dir.is_dir():
                continue

            skill_name = skill_dir.name
            skill_md = skill_dir / "SKILL.md"

            # Check if SKILL.md exists
            if not skill_md.exists():
                print(f"  Warning: {skill_name}/SKILL.md not found, skipping")
                continue

            # Target: .windsurf/workflows/{skill_name}.md
            target_link = windsurf_workflows / f"{skill_name}.md"

            # Check for collision
            if target_link.exists() or target_link.is_symlink():
                print(
                    f"  Collision detected: {skill_name}.md already exists in .windsurf/workflows/"
                )

                if skills_behavior == "overwrite":
                    if target_link.is_symlink():
                        target_link.unlink()
                    else:
                        target_link.unlink()
                    target_link.symlink_to(skill_md.resolve())
                    print(f"    Overwrote {skill_name}.md")
                    linked_count += 1

                elif skills_behavior == "skip":
                    print(f"    Skipped {skill_name}.md")
                    skipped_count += 1
                    collisions.append(f"{skill_name}.md")
                    partial_success = True

                elif skills_behavior == "backup":
                    backup_file = target_link.parent / f"{target_link.name}.backup"
                    counter = 1
                    while backup_file.exists():
                        backup_file = (
                            target_link.parent
                            / f"{target_link.stem}.{counter}.md.backup"
                        )
                        counter += 1
                    target_link.rename(backup_file)
                    print(f"    Backed up {skill_name}.md to {backup_file.name}")
                    target_link.symlink_to(skill_md.resolve())
                    print(f"    Overwrote {skill_name}.md (backup created)")
                    linked_count += 1

                elif skills_behavior == "prompt":
                    if INTERACTIVE:
                        answer = (
                            input(f"  Overwrite {skill_name}.md? [y/N] ")
                            .strip()
                            .lower()
                        )
                        if answer in ("y", "yes"):
                            if target_link.is_symlink():
                                target_link.unlink()
                            else:
                                target_link.unlink()
                            target_link.symlink_to(skill_md.resolve())
                            print(f"    Overwrote {skill_name}.md")
                            linked_count += 1
                        else:
                            print(f"    Skipped {skill_name}.md")
                            skipped_count += 1
                            collisions.append(f"{skill_name}.md")
                            partial_success = True
                    else:
                        print(f"    Skipping {skill_name}.md (non-interactive mode)")
                        skipped_count += 1
                        collisions.append(f"{skill_name}.md")
                        partial_success = True
            else:
                # No collision, create symlink
                target_link.symlink_to(skill_md.resolve())
                print(f"  Linked {skill_name}.md")
                linked_count += 1

    print(
        f"  Workflows linking complete: {linked_count} linked, {skipped_count} skipped"
    )

    return linked_count, skipped_count, collisions, partial_success


def link_skills_to_codex(
    target: pathlib.Path,
    ai_context: pathlib.Path,
    skills_behavior: str,
) -> Tuple[int, int, List[str], bool]:
    """Link skills from ai-context/skills to .agents/skills.

    Returns:
        Tuple of (linked_count, skipped_count, collision_names, partial_success)
    """
    print("Linking skills to .agents directory...")

    codex_dir = target / ".agents"
    codex_skills = codex_dir / "skills"
    source_skills = ai_context / "skills"

    linked_count = 0
    skipped_count = 0
    collisions = []
    partial_success = False

    if not codex_dir.exists():
        codex_dir.mkdir(parents=True, exist_ok=True)
        print("  Created .agents directory")

    if not codex_skills.exists():
        codex_skills.mkdir(parents=True, exist_ok=True)
        print("  Created .agents/skills directory")

    if source_skills.exists():
        for skill_dir in sorted(source_skills.iterdir()):
            if not skill_dir.is_dir():
                continue

            skill_name = skill_dir.name
            target_link = codex_skills / skill_name

            if target_link.exists() or target_link.is_symlink():
                print(f"  Collision detected: {skill_name} already exists in .agents/skills/")

                if skills_behavior == "overwrite":
                    if target_link.is_symlink():
                        target_link.unlink()
                    else:
                        shutil.rmtree(target_link)
                    target_link.symlink_to(skill_dir)
                    print(f"    Overwrote {skill_name}")
                    linked_count += 1

                elif skills_behavior == "skip":
                    print(f"    Skipped {skill_name}")
                    skipped_count += 1
                    collisions.append(skill_name)
                    partial_success = True

                elif skills_behavior == "backup":
                    backup_dir = create_backup(target_link, target_link)
                    print(f"    Backed up {skill_name} to {backup_dir.name}")
                    if target_link.is_symlink():
                        target_link.unlink()
                    else:
                        shutil.rmtree(target_link)
                    target_link.symlink_to(skill_dir)
                    print(f"    Overwrote {skill_name} (backup created)")
                    linked_count += 1

                elif skills_behavior == "prompt":
                    if INTERACTIVE:
                        answer = (
                            input(f"  Overwrite {skill_name}? [y/N] ").strip().lower()
                        )
                        if answer in ("y", "yes"):
                            if target_link.is_symlink():
                                target_link.unlink()
                            else:
                                shutil.rmtree(target_link)
                            target_link.symlink_to(skill_dir)
                            print(f"    Overwrote {skill_name}")
                            linked_count += 1
                        else:
                            print(f"    Skipped {skill_name}")
                            skipped_count += 1
                            collisions.append(skill_name)
                            partial_success = True
                    else:
                        print(f"    Skipping {skill_name} (non-interactive mode)")
                        skipped_count += 1
                        collisions.append(skill_name)
                        partial_success = True
            else:
                target_link.symlink_to(skill_dir)
                print(f"  Linked {skill_name}")
                linked_count += 1

    print(
        f"  Codex linking complete: {linked_count} linked, {skipped_count} skipped"
    )

    return linked_count, skipped_count, collisions, partial_success


def link_skills_to_opencode(
    target: pathlib.Path,
    ai_context: pathlib.Path,
    skills_behavior: str,
) -> Tuple[int, int, List[str], bool]:
    """Link skills from ai-context/skills to .opencode/skills.

    Returns:
        Tuple of (linked_count, skipped_count, collision_names, partial_success)
    """
    print("Linking skills to .opencode directory...")

    opencode_dir = target / ".opencode"
    opencode_skills = opencode_dir / "skills"
    source_skills = ai_context / "skills"

    linked_count = 0
    skipped_count = 0
    collisions = []
    partial_success = False

    if not opencode_dir.exists():
        opencode_dir.mkdir(parents=True, exist_ok=True)
        print("  Created .opencode directory")

    if not opencode_skills.exists():
        opencode_skills.mkdir(parents=True, exist_ok=True)
        print("  Created .opencode/skills directory")

    if source_skills.exists():
        for skill_dir in sorted(source_skills.iterdir()):
            if not skill_dir.is_dir():
                continue

            skill_name = skill_dir.name
            skill_md = skill_dir / "SKILL.md"
            target_link = opencode_skills / skill_name

            if not skill_md.exists():
                print(f"  Warning: {skill_name}/SKILL.md not found, skipping")
                continue

            if target_link.exists() or target_link.is_symlink():
                print(f"  Collision detected: {skill_name} already exists in .opencode/skills/")

                if skills_behavior == "overwrite":
                    if target_link.is_symlink():
                        target_link.unlink()
                    else:
                        shutil.rmtree(target_link)
                    target_link.symlink_to(skill_dir)
                    print(f"    Overwrote {skill_name}")
                    linked_count += 1

                elif skills_behavior == "skip":
                    print(f"    Skipped {skill_name}")
                    skipped_count += 1
                    collisions.append(skill_name)
                    partial_success = True

                elif skills_behavior == "backup":
                    backup_dir = create_backup(target_link, target_link)
                    print(f"    Backed up {skill_name} to {backup_dir.name}")
                    if target_link.is_symlink():
                        target_link.unlink()
                    else:
                        shutil.rmtree(target_link)
                    target_link.symlink_to(skill_dir)
                    print(f"    Overwrote {skill_name} (backup created)")
                    linked_count += 1

                elif skills_behavior == "prompt":
                    if INTERACTIVE:
                        answer = (
                            input(f"  Overwrite {skill_name}? [y/N] ").strip().lower()
                        )
                        if answer in ("y", "yes"):
                            if target_link.is_symlink():
                                target_link.unlink()
                            else:
                                shutil.rmtree(target_link)
                            target_link.symlink_to(skill_dir)
                            print(f"    Overwrote {skill_name}")
                            linked_count += 1
                        else:
                            print(f"    Skipped {skill_name}")
                            skipped_count += 1
                            collisions.append(skill_name)
                            partial_success = True
                    else:
                        print(f"    Skipping {skill_name} (non-interactive mode)")
                        skipped_count += 1
                        collisions.append(skill_name)
                        partial_success = True
            else:
                target_link.symlink_to(skill_dir)
                print(f"  Linked {skill_name}")
                linked_count += 1

    print(f"  OpenCode linking complete: {linked_count} linked, {skipped_count} skipped")

    return linked_count, skipped_count, collisions, partial_success


# ──────────────────────────────────────────────────────────────────────
# Darcs and Git Integration
# ──────────────────────────────────────────────────────────────────────


def init_darcs(ai_context: pathlib.Path) -> None:
    """Initialize darcs in ai-context directory if available."""
    try:
        subprocess.run(
            ["darcs", "--version"], capture_output=True, check=True, timeout=5
        )
    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ):
        print("")
        print("Tip: Install darcs for local version control of ai-context/.")
        print("  It keeps history without polluting git. See: https://darcs.net/")
        return

    print("Initializing darcs in ai-context/ ...")
    try:
        subprocess.run(
            ["darcs", "init"],
            cwd=ai_context,
            check=True,
            capture_output=True,
            timeout=10,
        )
        subprocess.run(
            ["darcs", "add", "-r", "."],
            cwd=ai_context,
            check=True,
            capture_output=True,
            timeout=10,
        )
        subprocess.run(
            ["darcs", "record", "-a", "-m", "Initial ai-context setup"],
            cwd=ai_context,
            check=True,
            capture_output=True,
            timeout=10,
        )
        print("Darcs initialized with initial recording.")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"Warning: darcs initialization failed: {e}", file=sys.stderr)


# ──────────────────────────────────────────────────────────────────────
# Gitignore Management
# ──────────────────────────────────────────────────────────────────────


def handle_tracking(
    target: pathlib.Path,
    tracking_behavior: str,
) -> None:
    """Handle tracking behavior: ignore in .gitignore or track in parent git."""
    gitignore_path = target / ".gitignore"
    entry = "ai-context/"

    if tracking_behavior == "track":
        print("ai-context/ will be tracked in parent git (not ignored).")
        return

    if tracking_behavior == "ignore":
        already_ignored = False
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if entry in content.splitlines():
                already_ignored = True

        if already_ignored:
            print("ai-context/ is already in .gitignore.")
            return

        if not gitignore_path.exists():
            gitignore_path.write_text(entry + "\n")
        else:
            with gitignore_path.open("a") as f:
                f.write(entry + "\n")
        print("Added 'ai-context/' to .gitignore")

    elif tracking_behavior == "prompt":
        if INTERACTIVE:
            answer = input("Add ai-context/ to .gitignore? [Y/n] ").strip().lower()
            if answer in ("", "y", "yes"):
                already_ignored = False
                if gitignore_path.exists():
                    content = gitignore_path.read_text()
                    if entry in content.splitlines():
                        already_ignored = True

                if not already_ignored:
                    if not gitignore_path.exists():
                        gitignore_path.write_text(entry + "\n")
                    else:
                        with gitignore_path.open("a") as f:
                            f.write(entry + "\n")
                print("Added 'ai-context/' to .gitignore")
            else:
                print("Skipped .gitignore update.")
        else:
            print("Skipped .gitignore update (non-interactive mode).")

    elif tracking_behavior == "skip":
        print("Skipped .gitignore update.")


# ──────────────────────────────────────────────────────────────────────
# Summary and Guidance Prompt
# ──────────────────────────────────────────────────────────────────────


def print_ai_agent_guidance_prompt() -> None:
    """Print the AI agent setup assistance prompt."""
    print("=" * 62)
    print(" AI AGENT SETUP ASSISTANCE PROMPT")
    print("=" * 62)
    print("")
    print("Copy this prompt into your AI agent to help fill the templates:")
    print("")
    print("---")
    print("")
    print("## Introduction")
    print("")
    print(
        "This project now has an `ai-context/` directory. Its purpose is to provide persistent"
    )
    print(
        "context, guidelines, and session history for AI assistants working on this codebase."
    )
    print(
        "Think of it as a memory or handbook for AI agents - it ensures that when you"
    )
    print(
        "(or a different AI) resume work, you have the necessary background to be effective."
    )
    print("")
    print("The directory contains:")
    print("- Architecture principles and domain knowledge")
    print("- Session notes documenting implementation history")
    print("- Coding guidelines and development workflows")
    print("- Today I Learned entries (TIL)")
    print("")
    print("## Project Analysis and Template Setup")
    print("")
    print(
        "I need to analyze this project and fill in the ai-context templates. Please help me document:"
    )
    print("")
    print("### 1. First, analyze the project structure:")
    print("")
    print("**Key files to examine (prioritized):**")
    print("- `README.md` - Project overview and purpose")
    print(
        "- `package.json`, `pom.xml`, `build.gradle`, `Cargo.toml`, etc. - Dependencies and tech stack"
    )
    print(
        "- Main source directories (`src/`, `lib/`, `app/`, etc.) - Architecture patterns"
    )
    print("- Configuration files - Environment and setup requirements")
    print("- `docs/` directory - Additional documentation")
    print("")
    print("**Analysis questions:**")
    print(
        "- What is the primary purpose of this project? (web app, CLI tool, library, etc.)"
    )
    print("- Who are the users? (developers, end users, internal team)")
    print("- What programming language(s) and frameworks are used?")
    print("- Are there any unusual architectural patterns or design decisions?")
    print("")
    print("### 2. Fill in `architecture/01-domain-explanation.md`:")
    print("")
    print("Based on your analysis, complete these sections:")
    print("")
    print("**What does this project do?**")
    print("- 1-2 paragraphs explaining the purpose and value proposition")
    print("- Include target users and main use cases")
    print("")
    print("**Key Concepts**")
    print("- List 5-10 domain-specific terms with brief explanations")
    print("- Include technical concepts that would confuse outsiders")
    print('- Example: "JWT Token - Authentication token containing user claims"')
    print("")
    print("**Data Flow**")
    print("- How data enters, transforms, and exits the system")
    print("- Key integration points (APIs, databases, external services)")
    print("- Important business logic flows")
    print("")
    print("### 3. Review and customize `CLAUDE.md`:")
    print("")
    print("**Important - Symlink structure:** The root `CLAUDE.md`, `AGENTS.md`, and")
    print("`.windsurf/rules.md` are symbolic links pointing to `ai-context/CLAUDE.md`.")
    print("They are NOT separate files. Editing any of them modifies the same file.")
    print("Do NOT delete or erase these symlinks - they redirect agents to the")
    print("centralized context in `ai-context/CLAUDE.md`.")
    print("")
    print("Check if these need adjustment:")
    print("- Architecture section - does it match the actual stack?")
    print("- Coding patterns - are there specific conventions used?")
    print("- Testing approach - does it align with existing practices?")
    print("")
    print("### 4. Identify any missing guidelines:")
    print("")
    print("Are there language-specific or framework-specific guidelines needed?")
    print("- Java Spring Boot patterns")
    print("- React component conventions")
    print("- Database schema rules")
    print("- API design principles")
    print("")
    print("---")
    print("")
    print(
        "**Token-efficient approach:** Start with README.md and 2-3 key source files, then expand based on findings. Focus on what makes this project unique rather than documenting obvious patterns."
    )
    print("")


def print_summary(
    ai_context: pathlib.Path,
    java_enabled: bool,
    linked_count: int,
    skipped_count: int,
    collisions: List[str],
) -> None:
    """Print setup summary and guidance prompt."""
    print("")
    print("=" * 62)
    print(" ai-context setup complete!")
    print("=" * 62)
    print("")
    print(f" Installed in: {ai_context}")
    print("")
    print(" Directories:")
    print("   guidelines/  - Coding standards and domain knowledge")
    print("   sessions/    - Session notes (YYYY-MM-DD-XX-<topic>.md)")
    print("   til/         - Today I Learned entries")
    print("   reference/   - API specs and schemas")
    print("   external/    - Context from other projects")
    print("   test-data/   - Test data files")
    print("   scripts/     - Utility scripts")
    print("   skills/      - Workflow automation skills")
    print("   archive/     - Outdated files")
    print("   .claude/     - Windsurf Cascade integration (skills linked here)")
    print("")
    print(" Files:")
    print("   CLAUDE.md  → ai-context/CLAUDE.md      - Architecture principles (symlink)")
    print("   AGENTS.md  → ai-context/CLAUDE.md      - Architecture principles (symlink)")
    print("   0-index.md                             - Directory guide")
    print("   architecture/00-architecture-index.md  - Architecture overview")
    print("   architecture/01-domain-explanation.md  - Domain concepts (fill in!)")
    print("   briefs/00-about-briefs.md              - Feature briefs index")
    print("   guidelines/DEVELOPMENT_PROCESS.md      - Workflow process")
    print("   guidelines/BRIEF_CREATION_GUIDELINES.md - Brief creation process")
    print("   guidelines/PR_DESCRIPTION_GUIDELINES.md - PR format")
    if java_enabled:
        print("   guidelines/JAVA_UNIT_TESTING_GUIDELINES.md      - Java TDD")
        print(
            "   guidelines/JAVA_TEST_DATA_CREATION_GUIDELINES.md - Test data patterns"
        )
    print("   scripts/move-context-files.py          - Move files + update refs")
    print("   scripts/migrate-filenames.py           - Rename session files")
    print("   skills/commitmsg/      - /commitmsg - Smart commit message generation")
    print("   skills/prmsg/          - /prmsg - PR description generation")
    print("   skills/session-save/   - /session-save - Automated session summaries")
    print("")
    print(" .windsurf/:")
    print("   rules.md → ../ai-context/CLAUDE.md     - AI rules (symlink)")
    print("   workflows/ - Linked as .md files pointing to ai-context/skills/*/SKILL.md")
    print("   Windsurf Cascade integration")
    print("")
    print(" .claude/skills:")
    print("   Linked as directories to ai-context/skills/")
    print("   Claude Code integration")
    print("")
    print(" .agents/skills:")
    print("   Linked as directories to ai-context/skills/")
    print("   Codex integration")
    print("")
    print(" .opencode/skills:")
    print("   Linked as directories to ai-context/skills/")
    print("   OpenCode integration")
    if linked_count > 0:
        print(f"   Total: {linked_count} skill(s) linked successfully")
    if skipped_count > 0:
        print(f"   Total: {skipped_count} skill(s) skipped (collisions)")
        if collisions:
            print(f"   Collisions: {', '.join(collisions)}")
    print("")
    print(" Next steps:")
    print(
        "   1. Fill in architecture/01-domain-explanation.md with your project's concepts"
    )
    print("   2. Review CLAUDE.md and adjust to your preferences")
    print("   3. Start a session and let the AI read 0-index.md first")
    print("")

    # AI Agent Guidance Prompt
    print_ai_agent_guidance_prompt()
    print("")


# ──────────────────────────────────────────────────────────────────────
def validate_flag_combinations(args) -> None:
    """Validate incompatible flag combinations across groups.

    Raises:
        SystemExit: With code 2 if incompatible flags are used together.
    """
    # --shared conflicts with --darcs-* and --tracking-*
    if args.shared and (args.darcs_auto or args.darcs_skip):
        parser.error("--shared not allowed with --darcs-* arguments")
    if args.shared and (args.tracking_ignore or args.tracking_track or args.tracking_prompt):
        parser.error("--shared not allowed with --tracking-* arguments")

    # --standalone conflicts with --darcs-* and --tracking-*
    if args.standalone and (args.darcs_auto or args.darcs_skip):
        parser.error("--standalone not allowed with --darcs-* arguments")
    if args.standalone and (args.tracking_ignore or args.tracking_track or args.tracking_prompt):
        parser.error("--standalone not allowed with --tracking-* arguments")

    # --auto conflicts with --interactive
    if args.auto and args.interactive:
        parser.error("--auto not allowed with --interactive")


# Main
# ──────────────────────────────────────────────────────────────────────

def main() -> None:
    """Main entry point."""
    global parser
    parser = create_parser()
    args = parser.parse_args()

    # Validate flag combinations
    validate_flag_combinations(args)

    # Handle special actions
    if args.print_prompt:
        print_ai_agent_guidance_prompt()
        sys.exit(0)

    # Validate target
    target = validate_target(args.target)

    # Resolve behaviors
    skills_behavior = resolve_skills_behavior(args)
    darcs_behavior = resolve_darcs_behavior(args)
    tracking_behavior = resolve_tracking_behavior(args)

    # Create directory structure
    ai_context = create_directory_structure(target)

    # Copy files
    copy_core_files(ai_context)
    copy_skills(ai_context)

    # Install Java TDD module if requested
    if args.java:
        install_java_tdd_module(ai_context)

    # Copy root stubs
    copy_root_stubs(target)

    # Link skills to .claude directory
    linked_count, skipped_count, collisions, partial_success = link_skills_to_claude(
        target,
        ai_context,
        skills_behavior,
    )

    # Link skills to .windsurf/workflows directory
    wf_linked, wf_skipped, wf_collisions, wf_partial = link_skills_to_windsurf(
        target,
        ai_context,
        skills_behavior,
    )
    linked_count += wf_linked
    skipped_count += wf_skipped
    collisions.extend(wf_collisions)
    partial_success = partial_success or wf_partial

    # Link skills to .agents directory (Codex)
    codex_linked, codex_skipped, codex_collisions, codex_partial = link_skills_to_codex(
        target,
        ai_context,
        skills_behavior,
    )
    linked_count += codex_linked
    skipped_count += codex_skipped
    collisions.extend(codex_collisions)
    partial_success = partial_success or codex_partial

    # Link skills to .opencode directory (OpenCode)
    opencode_linked, opencode_skipped, opencode_collisions, opencode_partial = link_skills_to_opencode(
        target,
        ai_context,
        skills_behavior,
    )
    linked_count += opencode_linked
    skipped_count += opencode_skipped
    collisions.extend(opencode_collisions)
    partial_success = partial_success or opencode_partial

    # Initialize darcs based on behavior
    if darcs_behavior == "auto":
        init_darcs(ai_context)
    elif darcs_behavior == "skip":
        pass  # Skip darcs as requested

    # Handle tracking (gitignore or track in parent git)
    handle_tracking(target, tracking_behavior)

    # Print summary
    print_summary(ai_context, args.java, linked_count, skipped_count, collisions)

    # Exit with appropriate code
    if partial_success:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
