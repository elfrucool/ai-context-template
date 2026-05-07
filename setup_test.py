#!/usr/bin/env python3
"""
Test suite for setup.py

Tests the setup.py script with 9 test cases covering:
1. Help option
2. Conflicting skills flags
3. Conflicting gitignore flags
4. Conflicting mode flags
5. Additional conflicting skills flags
6. Additional conflicting gitignore flags
7. Fresh install with --auto mode
8. Fresh install with explicit flags
9. Collision handling with --skills-skip
"""

import unittest
import subprocess
import tempfile
import shutil
import sys
from pathlib import Path


class SetupScriptTests(unittest.TestCase):
    """Test cases for setup.py"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.script_dir = Path(__file__).resolve().parent
        cls.setup_script = cls.script_dir / "setup.py"
        cls.tmp_base = cls.script_dir / "tmp"
        cls.tmp_base.mkdir(exist_ok=True)

    def setUp(self):
        """Create a temporary directory for each test."""
        self.test_dir = tempfile.mkdtemp(dir=self.tmp_base)

    def tearDown(self):
        """Clean up temporary directory after each test."""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def run_setup(self, target: str = None, *args) -> tuple:
        """Run setup.py and return (exit_code, stdout, stderr).

        Args:
            target: Target path (uses self.test_dir if None)
            *args: Additional arguments to pass to setup.py

        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        if target is None:
            target = self.test_dir

        cmd = [sys.executable, str(self.setup_script), target] + list(args)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )

        return result.returncode, result.stdout, result.stderr

    # ──────────────────────────────────────────────────────────────────────
    # Test 1: --help option
    # ──────────────────────────────────────────────────────────────────────

    def test_01_help(self):
        """Test --help option returns exit code 0."""
        exit_code, stdout, stderr = self.run_setup(None, "--help")

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")
        self.assertIn("ai-context-template setup script", stdout)
        self.assertIn("options:", stdout)

    # ──────────────────────────────────────────────────────────────────────
    # Test 2: Conflicting --skills-* flags
    # ──────────────────────────────────────────────────────────────────────

    def test_02_skills_conflict_overwrite_skip(self):
        """Test --skills-overwrite and --skills-skip conflict returns exit code 2."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--skills-overwrite",
            "--skills-skip",
        )

        self.assertEqual(exit_code, 2, f"Expected exit 2, got {exit_code}")
        self.assertIn("not allowed with argument", stderr)

    # ──────────────────────────────────────────────────────────────────────
    # Test 3: Conflicting --gitignore-* flags
    # ──────────────────────────────────────────────────────────────────────

    def test_03_gitignore_conflict_auto_skip(self):
        """Test --gitignore-auto and --gitignore-skip conflict returns exit code 2."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--gitignore-auto",
            "--gitignore-skip",
        )

        self.assertEqual(exit_code, 2, f"Expected exit 2, got {exit_code}")
        self.assertIn("not allowed with argument", stderr)

    # ──────────────────────────────────────────────────────────────────────
    # Test 4: Conflicting --auto and --interactive mode flags
    # ──────────────────────────────────────────────────────────────────────

    def test_04_mode_conflict_auto_interactive(self):
        """Test --auto and --interactive conflict returns exit code 2."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--auto",
            "--interactive",
        )

        self.assertEqual(exit_code, 2, f"Expected exit 2, got {exit_code}")
        self.assertIn("not allowed with argument", stderr)

    # ──────────────────────────────────────────────────────────────────────
    # Test 5: Conflicting --skills-overwrite and --skills-backup
    # ──────────────────────────────────────────────────────────────────────

    def test_05_skills_conflict_overwrite_backup(self):
        """Test --skills-overwrite and --skills-backup conflict returns exit code 2."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--skills-overwrite",
            "--skills-backup",
        )

        self.assertEqual(exit_code, 2, f"Expected exit 2, got {exit_code}")
        self.assertIn("not allowed with argument", stderr)

    # ──────────────────────────────────────────────────────────────────────
    # Test 6: Conflicting --gitignore-auto and --gitignore-prompt
    # ──────────────────────────────────────────────────────────────────────

    def test_06_gitignore_conflict_auto_prompt(self):
        """Test --gitignore-auto and --gitignore-prompt conflict returns exit code 2."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--gitignore-auto",
            "--gitignore-prompt",
        )

        self.assertEqual(exit_code, 2, f"Expected exit 2, got {exit_code}")
        self.assertIn("not allowed with argument", stderr)

    # ──────────────────────────────────────────────────────────────────────
    # Test 7: Fresh install with --auto mode
    # ──────────────────────────────────────────────────────────────────────

    def test_07_fresh_install_auto(self):
        """Test fresh install with --auto returns exit code 0."""
        exit_code, stdout, stderr = self.run_setup(None, "--auto")

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        # Check that ai-context directory structure was created
        ai_context = Path(self.test_dir) / "ai-context"
        self.assertTrue(ai_context.exists(), "ai-context/ directory not created")
        self.assertTrue((ai_context / "guidelines").exists(), "guidelines/ not created")
        self.assertTrue((ai_context / "architecture").exists(), "architecture/ not created")
        self.assertTrue((ai_context / "briefs").exists(), "briefs/ not created")
        self.assertTrue((ai_context / "scripts").exists(), "scripts/ not created")
        self.assertTrue((ai_context / "sessions").exists(), "sessions/ not created")

        # Check that core files exist
        self.assertTrue((ai_context / "CLAUDE.md").exists(), "CLAUDE.md not found")
        self.assertTrue((ai_context / "0-index.md").exists(), "0-index.md not found")

        # Check that new architecture and briefs files exist
        self.assertTrue((ai_context / "architecture" / "00-architecture-index.md").exists(), "architecture/00-architecture-index.md not found")
        self.assertTrue((ai_context / "architecture" / "01-domain-explanation.md").exists(), "architecture/01-domain-explanation.md not found")
        self.assertTrue((ai_context / "briefs" / "00-about-briefs.md").exists(), "briefs/00-about-briefs.md not found")
        self.assertTrue((ai_context / "guidelines" / "BRIEF_CREATION_GUIDELINES.md").exists(), "guidelines/BRIEF_CREATION_GUIDELINES.md not found")

        # Check that .windsurf/workflows/ directory exists
        windsurf_workflows = Path(self.test_dir) / ".windsurf" / "workflows"
        self.assertTrue(windsurf_workflows.exists(), ".windsurf/workflows/ directory not created")

        # Check that at least one .md symlink exists in .windsurf/workflows/
        md_files = list(windsurf_workflows.glob("*.md"))
        self.assertGreater(len(md_files), 0, "No .md files found in .windsurf/workflows/")

        # Check that at least one symlink points to SKILL.md
        for md_file in md_files:
            if md_file.is_symlink():
                target = md_file.resolve()
                self.assertTrue(str(target).endswith("SKILL.md"), f"{md_file.name} symlink doesn't target SKILL.md")
                break
        else:
            self.fail("No symlinks found in .windsurf/workflows/")

        # Check that root-level symlinks point to ai-context/CLAUDE.md
        root = Path(self.test_dir)
        ai_context_claude = (root / "ai-context" / "CLAUDE.md").resolve()

        claude_md = root / "CLAUDE.md"
        self.assertTrue(claude_md.is_symlink(), "CLAUDE.md is not a symlink")
        self.assertEqual(claude_md.resolve(), ai_context_claude)

        agents_md = root / "AGENTS.md"
        self.assertTrue(agents_md.is_symlink(), "AGENTS.md is not a symlink")
        self.assertEqual(agents_md.resolve(), ai_context_claude)

        windsurf_rules = root / ".windsurf" / "rules.md"
        self.assertTrue(windsurf_rules.is_symlink(), ".windsurf/rules.md is not a symlink")
        self.assertEqual(windsurf_rules.resolve(), ai_context_claude)

    # ──────────────────────────────────────────────────────────────────────
    # Test 8: Fresh install with explicit flags
    # ──────────────────────────────────────────────────────────────────────

    def test_08_fresh_install_explicit_flags(self):
        """Test fresh install with --skills-skip and --gitignore-skip returns exit code 0."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--skills-skip",
            "--gitignore-skip",
        )

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        # Check that ai-context directory structure was created
        ai_context = Path(self.test_dir) / "ai-context"
        self.assertTrue(ai_context.exists(), "ai-context/ directory not created")

        # Check that new directories exist
        self.assertTrue((ai_context / "architecture").exists(), "architecture/ not created")
        self.assertTrue((ai_context / "briefs").exists(), "briefs/ not created")

        # Check that .windsurf/workflows/ directory exists
        windsurf_workflows = Path(self.test_dir) / ".windsurf" / "workflows"
        self.assertTrue(windsurf_workflows.exists(), ".windsurf/workflows/ directory not created")

        # Check that at least one .md symlink exists
        md_files = list(windsurf_workflows.glob("*.md"))
        self.assertGreater(len(md_files), 0, "No .md files found in .windsurf/workflows/")

    # ──────────────────────────────────────────────────────────────────────
    # Test 9: Collision handling with --skills-skip
    # ──────────────────────────────────────────────────────────────────────

    def test_09_collision_handling_skip(self):
        """Test collision handling with --skills-skip returns exit code 1.

        This test pre-creates a skill collision before running setup.py,
        then runs with --skills-skip and expects exit code 1 (partial success).
        """
        # Pre-create the directory structure that setup.py expects
        ai_context = Path(self.test_dir) / "ai-context"
        ai_context.mkdir(parents=True, exist_ok=True)

        # Copy the skills directory from the source to ai-context
        src_skills = self.script_dir / "core" / "skills"
        if src_skills.exists():
            shutil.copytree(src_skills, ai_context / "skills")

        # Pre-create a collision: manually create a skill in .claude/skills/
        claude_skills = Path(self.test_dir) / ".claude" / "skills"
        claude_skills.mkdir(parents=True, exist_ok=True)

        # Create a collision by pre-creating one of the skills in .claude/skills/
        ai_context_skills = ai_context / "skills"
        if ai_context_skills.exists():
            for skill in ai_context_skills.iterdir():
                if skill.is_dir():
                    # Create a collision by pre-creating this skill in .claude/skills/
                    collision_target = claude_skills / skill.name
                    collision_target.mkdir(parents=True, exist_ok=True)
                    (collision_target / "dummy.txt").write_text("existing content")
                    break

        # Now remove the ai-context we created so setup.py can run
        shutil.rmtree(ai_context)

        # Run setup.py with --skills-skip
        # This should create the structure, detect the collision, skip it, and exit with 1
        exit_code, stdout, stderr = self.run_setup(None, "--skills-skip")
        self.assertEqual(exit_code, 1, f"Expected exit 1, got {exit_code}")
        self.assertIn("Collision detected", stdout)
        self.assertIn("Skipped", stdout)

    # ──────────────────────────────────────────────────────────────────────
# Test 10: Windsurf collision handling with --skills-skip

    def test_10_windsurf_collision_handling_skip(self):
        """Test windsurf collision handling with --skills-skip returns exit code 1.

        This test pre-creates a windsurf workflows collision before running setup.py,
        then runs with --skills-skip and expects exit code 1 (partial success).
        """
        # Pre-create the .windsurf/workflows collision
        windsurf_workflows = Path(self.test_dir) / ".windsurf" / "workflows"
        windsurf_workflows.mkdir(parents=True, exist_ok=True)

        # Create a collision by pre-creating one of the workflow files
        collision_file = windsurf_workflows / "commitmsg.md"
        collision_file.write_text("existing workflow content")

        # Run setup.py with --skills-skip
        # This should create the structure, detect the collision, skip it, and exit with 1
        exit_code, stdout, stderr = self.run_setup(None, "--skills-skip")
        self.assertEqual(exit_code, 1, f"Expected exit 1, got {exit_code}")
        self.assertIn("Collision detected", stdout)
        self.assertIn("Skipped", stdout)

    # ──────────────────────────────────────────────────────────────────────
    # Test 11: Conflicting darcs flags
    # ──────────────────────────────────────────────────────────────────────

    def test_11_darcs_conflict_skip_auto(self):
        """Test --darcs-skip and --darcs-auto conflict returns exit code 2."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--darcs-skip",
            "--darcs-auto",
        )

        self.assertEqual(exit_code, 2, f"Expected exit 2, got {exit_code}")
        self.assertIn("not allowed with argument", stderr)

    # ──────────────────────────────────────────────────────────────────────
    # Test 12: Conflicting tracking flags
    # ──────────────────────────────────────────────────────────────────────

    def test_12_tracking_conflict_ignore_track(self):
        """Test --tracking-ignore and --tracking-track conflict returns exit code 2."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--tracking-ignore",
            "--tracking-track",
        )

        self.assertEqual(exit_code, 2, f"Expected exit 2, got {exit_code}")
        self.assertIn("not allowed with argument", stderr)

# ──────────────────────────────────────────────────────────────────────
    # Test 13: --shared conflicts with --darcs-*
    # ──────────────────────────────────────────────────────────────────────

    def test_13_shared_darcs_conflict(self):
        """Test --shared and --darcs-auto conflict returns exit code 2."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--shared",
            "--darcs-auto",
        )

        self.assertEqual(exit_code, 2, f"Expected exit 2, got {exit_code}")
        self.assertIn("--shared not allowed with", stderr)

    # ──────────────────────────────────────────────────────────────────────
    # Test 14: Shared mode flag (ai-context in parent git, no darcs)
    # ──────────────────────────────────────────────────────────────────────

    def test_14_shared_mode(self):
        """Test --shared flag returns exit code 0.

        --shared means: no darcs (--darcs-skip implied) + track in git (--tracking-track implied)
        """
        exit_code, stdout, stderr = self.run_setup(None, "--shared")

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        # ai-context should be created
        ai_context = Path(self.test_dir) / "ai-context"
        self.assertTrue(ai_context.exists(), "ai-context/ directory not created")

        # Darcs should NOT be initialized (no _darcs directory)
        self.assertFalse((ai_context / "_darcs").exists(), "_darcs should not exist in shared mode")

        # .gitignore should NOT have ai-context/ (it's tracked, not ignored)
        gitignore = Path(self.test_dir) / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text()
            self.assertNotIn("ai-context/", content)

    # ──────────────────────────────────────────────────────────────────────
    # Test 15: Standalone mode flag (darcs if avail, ignore in git)
    # ──────────────────────────────────────────────────────────────────────

    def test_15_standalone_mode(self):
        """Test --standalone flag returns exit code 0.

        --standalone means: darcs if available (--darcs-auto implied) + ignore in git (--tracking-ignore implied)
        """
        exit_code, stdout, stderr = self.run_setup(None, "--standalone")

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        # ai-context should be created
        ai_context = Path(self.test_dir) / "ai-context"
        self.assertTrue(ai_context.exists(), "ai-context/ directory not created")

        # .gitignore SHOULD have ai-context/ (it's ignored, not tracked)
        gitignore = Path(self.test_dir) / ".gitignore"
        self.assertTrue(gitignore.exists(), ".gitignore should exist in standalone mode")
        content = gitignore.read_text()
        self.assertIn("ai-context/", content)

    # ──────────────────────────────────────────────────────────────────────
    # Test 16: Explicit --darcs-skip with --tracking-track
    # ──────────────────────────────────────────────────────────────────────

    def test_16_darcs_skip_tracking_track(self):
        """Test --darcs-skip with --tracking-track returns exit code 0."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--darcs-skip",
            "--tracking-track",
        )

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        ai_context = Path(self.test_dir) / "ai-context"
        self.assertTrue(ai_context.exists(), "ai-context/ directory not created")

        # No _darcs directory
        self.assertFalse((ai_context / "_darcs").exists(), "_darcs should not exist")

        # No ai-context/ in .gitignore
        gitignore = Path(self.test_dir) / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text()
            self.assertNotIn("ai-context/", content)

    # ──────────────────────────────────────────────────────────────────────
    # Test 17: Explicit --darcs-skip with --tracking-ignore
    # ──────────────────────────────────────────────────────────────────────

    def test_17_darcs_skip_tracking_ignore(self):
        """Test --darcs-skip with --tracking-ignore returns exit code 0."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--darcs-skip",
            "--tracking-ignore",
        )

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        ai_context = Path(self.test_dir) / "ai-context"
        self.assertTrue(ai_context.exists(), "ai-context/ directory not created")

        # No _darcs directory
        self.assertFalse((ai_context / "_darcs").exists(), "_darcs should not exist")

        # .gitignore SHOULD have ai-context/
        gitignore = Path(self.test_dir) / ".gitignore"
        self.assertTrue(gitignore.exists(), ".gitignore should exist")
        content = gitignore.read_text()
        self.assertIn("ai-context/", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
