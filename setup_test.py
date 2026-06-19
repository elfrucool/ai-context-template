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


# ──────────────────────────────────────────────────────────────────────
    # Test 18: Codex .agents/skills/ directory created
    # ──────────────────────────────────────────────────────────────────────

    def test_18_codex_skills_directory_created(self):
        """Test that .agents/skills/ directory is created with symlinks."""
        exit_code, stdout, stderr = self.run_setup(None, "--auto")

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        # Check that .agents/skills/ directory exists
        codex_skills = Path(self.test_dir) / ".agents" / "skills"
        self.assertTrue(codex_skills.exists(), ".agents/skills/ directory not created")

        # Check that at least one skill symlink exists
        skill_dirs = list(codex_skills.iterdir())
        self.assertGreater(len(skill_dirs), 0, "No skills linked in .agents/skills/")

    # ──────────────────────────────────────────────────────────────────────
    # Test 19: Codex skills are symlinks to ai-context/skills/
    # ──────────────────────────────────────────────────────────────────────

    def test_19_codex_skills_are_symlinks(self):
        """Test that Codex skills are symlinks pointing to ai-context/skills/."""
        exit_code, stdout, stderr = self.run_setup(None, "--auto")

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        codex_skills = Path(self.test_dir) / ".agents" / "skills"
        ai_context_skills = Path(self.test_dir) / "ai-context" / "skills"

        # Check that each skill in .agents/skills/ is a symlink to ai-context/skills/
        for skill_dir in codex_skills.iterdir():
            self.assertTrue(skill_dir.is_symlink(), f"{skill_dir.name} is not a symlink")
            self.assertEqual(
                skill_dir.resolve().parent,
                ai_context_skills.resolve(),
                f"{skill_dir.name} doesn't point to ai-context/skills/"
            )

    # ──────────────────────────────────────────────────────────────────────
    # Test 20: Codex collision handling with --skills-skip
    # ──────────────────────────────────────────────────────────────────────

    def test_20_codex_collision_handling_skip(self):
        """Test Codex collision handling with --skills-skip returns exit code 1."""
        # Pre-create ai-context with skills first
        ai_context = Path(self.test_dir) / "ai-context"
        ai_context.mkdir(parents=True, exist_ok=True)

        src_skills = self.script_dir / "core" / "skills"
        if src_skills.exists():
            dst_skills = ai_context / "skills"
            shutil.copytree(src_skills, dst_skills)

        # Pre-create the .agents/skills collision
        codex_skills = Path(self.test_dir) / ".agents" / "skills"
        codex_skills.mkdir(parents=True, exist_ok=True)

        # Create a collision by pre-creating one of the skill directories
        ai_context_skills = ai_context / "skills"
        if ai_context_skills.exists():
            for skill in ai_context_skills.iterdir():
                if skill.is_dir():
                    collision_target = codex_skills / skill.name
                    collision_target.mkdir(parents=True, exist_ok=True)
                    (collision_target / "dummy.txt").write_text("existing content")
                    break

        # Remove ai-context to let setup.py run fresh
        shutil.rmtree(ai_context)

        # Run setup.py with --skills-skip
        exit_code, stdout, stderr = self.run_setup(None, "--skills-skip")
        self.assertEqual(exit_code, 1, f"Expected exit 1, got {exit_code}")
        self.assertIn("Collision detected", stdout)

    # ──────────────────────────────────────────────────────────────────────
    # Test 21: OpenCode .opencode/skills/ directory created
    # ──────────────────────────────────────────────────────────────────────

    def test_21_opencode_skills_directory_created(self):
        """Test that .opencode/skills/ directory is created with symlinks."""
        exit_code, stdout, stderr = self.run_setup(None, "--auto")

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        # Check that .opencode/skills/ directory exists
        opencode_skills = Path(self.test_dir) / ".opencode" / "skills"
        self.assertTrue(opencode_skills.exists(), ".opencode/skills/ directory not created")

        # Check that at least one skill symlink exists
        skill_dirs = list(opencode_skills.iterdir())
        self.assertGreater(len(skill_dirs), 0, "No skills linked in .opencode/skills/")

    # ──────────────────────────────────────────────────────────────────────
    # Test 22: OpenCode skills are symlinks to ai-context/skills/
    # ──────────────────────────────────────────────────────────────────────

    def test_22_opencode_skills_are_symlinks(self):
        """Test that OpenCode skills are symlinks pointing to ai-context/skills/."""
        exit_code, stdout, stderr = self.run_setup(None, "--auto")

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        opencode_skills = Path(self.test_dir) / ".opencode" / "skills"
        ai_context_skills = Path(self.test_dir) / "ai-context" / "skills"

        # Check that each skill in .opencode/skills/ is a symlink to ai-context/skills/
        for skill_dir in opencode_skills.iterdir():
            self.assertTrue(skill_dir.is_symlink(), f"{skill_dir.name} is not a symlink")
            self.assertEqual(
                skill_dir.resolve().parent,
                ai_context_skills.resolve(),
                f"{skill_dir.name} doesn't point to ai-context/skills/"
            )

    # ──────────────────────────────────────────────────────────────────────
    # Test 23: OpenCode skills have valid frontmatter
    # ──────────────────────────────────────────────────────────────────────

    def test_23_opencode_skills_have_frontmatter(self):
        """Test that OpenCode skills have YAML frontmatter with name and description."""
        exit_code, stdout, stderr = self.run_setup(None, "--auto")

        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        ai_context_skills = Path(self.test_dir) / "ai-context" / "skills"

        # Check that each skill has valid frontmatter
        for skill_dir in ai_context_skills.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(skill_md.exists(), f"{skill_md.name}/SKILL.md not found")

            content = skill_md.read_text()
            self.assertTrue(content.startswith("---"), f"{skill_dir.name}/SKILL.md doesn't start with frontmatter")

            # Check required frontmatter fields
            self.assertIn("name:", content, f"{skill_dir.name}/SKILL.md missing name field")
            self.assertIn("description:", content, f"{skill_dir.name}/SKILL.md missing description field")

    # ──────────────────────────────────────────────────────────────────────
    # Test 24: OpenCode collision handling with --skills-skip
    # ──────────────────────────────────────────────────────────────────────

    def test_24_opencode_collision_handling_skip(self):
        """Test OpenCode collision handling with --skills-skip returns exit code 1."""
        # Pre-create ai-context with skills first
        ai_context = Path(self.test_dir) / "ai-context"
        ai_context.mkdir(parents=True, exist_ok=True)

        src_skills = self.script_dir / "core" / "skills"
        if src_skills.exists():
            dst_skills = ai_context / "skills"
            shutil.copytree(src_skills, dst_skills)

        # Pre-create the .opencode/skills collision
        opencode_skills = Path(self.test_dir) / ".opencode" / "skills"
        opencode_skills.mkdir(parents=True, exist_ok=True)

        # Create a collision by pre-creating one of the skill directories
        ai_context_skills = ai_context / "skills"
        if ai_context_skills.exists():
            for skill in ai_context_skills.iterdir():
                if skill.is_dir():
                    collision_target = opencode_skills / skill.name
                    collision_target.mkdir(parents=True, exist_ok=True)
                    (collision_target / "dummy.txt").write_text("existing content")
                    break

        # Remove ai-context to let setup.py run fresh
        shutil.rmtree(ai_context)

        # Run setup.py with --skills-skip
        exit_code, stdout, stderr = self.run_setup(None, "--skills-skip")
        self.assertEqual(exit_code, 1, f"Expected exit 1, got {exit_code}")
        self.assertIn("Collision detected", stdout)

    # ──────────────────────────────────────────────────────────────────────
    # Test 25: Fresh install creates root stubs pointing to ai-context/CLAUDE.md
    # ──────────────────────────────────────────────────────────────────────

    def test_25_fresh_root_stubs_single_source(self):
        """Test that fresh install creates root stubs resolving to ai-context/CLAUDE.md."""
        exit_code, stdout, stderr = self.run_setup(None, "--auto")
        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

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
    # Test 26: Existing AGENTS.md creates AGENTS.override.md
    # ──────────────────────────────────────────────────────────────────────

    def test_26_existing_agents_creates_override(self):
        """Test that existing AGENTS.md is preserved and AGENTS.override.md is created."""
        root = Path(self.test_dir)
        (root / "AGENTS.md").write_text("existing AGENTS content")

        exit_code, stdout, stderr = self.run_setup(None, "--auto")
        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        ai_context_claude = (root / "ai-context" / "CLAUDE.md").resolve()

        self.assertTrue((root / "AGENTS.md").exists(), "AGENTS.md should be preserved")
        self.assertEqual((root / "AGENTS.md").read_text(), "existing AGENTS content")
        self.assertTrue((root / "AGENTS.override.md").is_symlink(), "AGENTS.override.md not created")
        self.assertEqual((root / "AGENTS.override.md").resolve(), ai_context_claude)

        self.assertTrue((root / "CLAUDE.md").is_symlink(), "CLAUDE.md not created")
        self.assertEqual((root / "CLAUDE.md").resolve(), ai_context_claude)

    # ──────────────────────────────────────────────────────────────────────
    # Test 27: Existing CLAUDE.md creates CLAUDE.local.md
    # ──────────────────────────────────────────────────────────────────────

    def test_27_existing_claude_creates_local(self):
        """Test that existing CLAUDE.md is preserved and CLAUDE.local.md is created."""
        root = Path(self.test_dir)
        (root / "CLAUDE.md").write_text("existing CLAUDE content")

        exit_code, stdout, stderr = self.run_setup(None, "--auto")
        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        ai_context_claude = (root / "ai-context" / "CLAUDE.md").resolve()

        self.assertTrue((root / "CLAUDE.md").exists(), "CLAUDE.md should be preserved")
        self.assertEqual((root / "CLAUDE.md").read_text(), "existing CLAUDE content")
        self.assertTrue((root / "CLAUDE.local.md").is_symlink(), "CLAUDE.local.md not created")
        self.assertEqual((root / "CLAUDE.local.md").resolve(), ai_context_claude)

        self.assertTrue((root / "AGENTS.md").is_symlink(), "AGENTS.md not created")
        self.assertEqual((root / "AGENTS.md").resolve(), ai_context_claude)

    # ──────────────────────────────────────────────────────────────────────
    # Test 28: Both existing AGENTS.md and CLAUDE.md create both overrides
    # ──────────────────────────────────────────────────────────────────────

    def test_28_existing_both_creates_both_overrides(self):
        """Test that existing AGENTS.md and CLAUDE.md are preserved and both override symlinks are created."""
        root = Path(self.test_dir)
        (root / "AGENTS.md").write_text("existing AGENTS content")
        (root / "CLAUDE.md").write_text("existing CLAUDE content")

        exit_code, stdout, stderr = self.run_setup(None, "--auto")
        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        ai_context_claude = (root / "ai-context" / "CLAUDE.md").resolve()

        self.assertEqual((root / "AGENTS.md").read_text(), "existing AGENTS content")
        self.assertTrue((root / "AGENTS.override.md").is_symlink())
        self.assertEqual((root / "AGENTS.override.md").resolve(), ai_context_claude)

        self.assertEqual((root / "CLAUDE.md").read_text(), "existing CLAUDE content")
        self.assertTrue((root / "CLAUDE.local.md").is_symlink())
        self.assertEqual((root / "CLAUDE.local.md").resolve(), ai_context_claude)

    # ──────────────────────────────────────────────────────────────────────
    # Test 29: --root-stubs-skip leaves root files untouched
    # ──────────────────────────────────────────────────────────────────────

    def test_29_root_stubs_skip(self):
        """Test that --root-stubs-skip does not create or modify root stubs."""
        root = Path(self.test_dir)
        (root / "AGENTS.md").write_text("existing AGENTS content")
        (root / "CLAUDE.md").write_text("existing CLAUDE content")

        exit_code, stdout, stderr = self.run_setup(None, "--root-stubs-skip", "--auto")
        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        self.assertEqual((root / "AGENTS.md").read_text(), "existing AGENTS content")
        self.assertEqual((root / "CLAUDE.md").read_text(), "existing CLAUDE content")
        self.assertFalse((root / "AGENTS.override.md").exists())
        self.assertFalse((root / "CLAUDE.local.md").exists())
        self.assertFalse((root / "CLAUDE.md").is_symlink())

    # ──────────────────────────────────────────────────────────────────────
    # Test 30: --root-stubs-overwrite replaces existing files
    # ──────────────────────────────────────────────────────────────────────

    def test_30_root_stubs_overwrite(self):
        """Test that --root-stubs-overwrite replaces existing files with symlinks."""
        root = Path(self.test_dir)
        (root / "AGENTS.md").write_text("existing AGENTS content")
        (root / "CLAUDE.md").write_text("existing CLAUDE content")

        exit_code, stdout, stderr = self.run_setup(None, "--root-stubs-overwrite", "--auto")
        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        ai_context_claude = (root / "ai-context" / "CLAUDE.md").resolve()

        self.assertTrue((root / "AGENTS.md").is_symlink())
        self.assertEqual((root / "AGENTS.md").resolve(), ai_context_claude)
        self.assertTrue((root / "CLAUDE.md").is_symlink())
        self.assertEqual((root / "CLAUDE.md").resolve(), ai_context_claude)
        self.assertFalse((root / "AGENTS.override.md").exists())
        self.assertFalse((root / "CLAUDE.local.md").exists())

    # ──────────────────────────────────────────────────────────────────────
    # Test 31: --root-stubs-backup backs up existing files and creates overrides
    # ──────────────────────────────────────────────────────────────────────

    def test_31_root_stubs_backup(self):
        """Test that --root-stubs-backup backs up existing files and creates override symlinks."""
        root = Path(self.test_dir)
        (root / "AGENTS.md").write_text("existing AGENTS content")
        (root / "CLAUDE.md").write_text("existing CLAUDE content")

        exit_code, stdout, stderr = self.run_setup(None, "--root-stubs-backup", "--auto")
        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        ai_context_claude = (root / "ai-context" / "CLAUDE.md").resolve()

        # Original files should be backed up, not present as regular files
        self.assertFalse((root / "AGENTS.md").is_symlink() and (root / "CLAUDE.md").is_symlink())

        self.assertTrue((root / "AGENTS.override.md").is_symlink())
        self.assertEqual((root / "AGENTS.override.md").resolve(), ai_context_claude)
        self.assertTrue((root / "CLAUDE.local.md").is_symlink())
        self.assertEqual((root / "CLAUDE.local.md").resolve(), ai_context_claude)

        # Backups should exist
        backup_files = set(p.name for p in root.glob("*.20*"))
        self.assertTrue(any("AGENTS.md" in name for name in backup_files), "AGENTS.md backup not found")
        self.assertTrue(any("CLAUDE.md" in name for name in backup_files), "CLAUDE.md backup not found")

    # ──────────────────────────────────────────────────────────────────────
    # Test 32: Conflicting --root-stubs-* flags
    # ──────────────────────────────────────────────────────────────────────

    def test_32_root_stubs_conflict_overwrite_skip(self):
        """Test conflicting --root-stubs-overwrite and --root-stubs-skip returns exit code 2."""
        exit_code, stdout, stderr = self.run_setup(
            None,
            "--root-stubs-overwrite",
            "--root-stubs-skip",
        )
        self.assertEqual(exit_code, 2, f"Expected exit 2, got {exit_code}")
        self.assertIn("not allowed with argument", stderr)

    # ──────────────────────────────────────────────────────────────────────
    # Test 33: --skills-skip does not affect --root-stubs-overwrite
    # ──────────────────────────────────────────────────────────────────────

    def test_33_skills_skip_root_stubs_overwrite(self):
        """Test that --skills-skip does not prevent --root-stubs-overwrite from working."""
        root = Path(self.test_dir)
        (root / "AGENTS.md").write_text("existing AGENTS content")
        (root / "CLAUDE.md").write_text("existing CLAUDE content")

        exit_code, stdout, stderr = self.run_setup(
            None,
            "--skills-skip",
            "--root-stubs-overwrite",
            "--auto",
        )
        self.assertEqual(exit_code, 0, f"Expected exit 0, got {exit_code}")

        ai_context_claude = (root / "ai-context" / "CLAUDE.md").resolve()

        self.assertTrue((root / "AGENTS.md").is_symlink())
        self.assertEqual((root / "AGENTS.md").resolve(), ai_context_claude)
        self.assertTrue((root / "CLAUDE.md").is_symlink())
        self.assertEqual((root / "CLAUDE.md").resolve(), ai_context_claude)


if __name__ == "__main__":
    unittest.main(verbosity=2)
