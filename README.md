# ai-context-template

A template for bootstrapping an `ai-context/` directory in any project. Provides a structured folder layout, coding guidelines, and workflow conventions that make AI-assisted development more effective.

## Quick Start

```bash
# Basic setup (all projects)
python3 setup.py /path/to/your-project

# With Java TDD guidelines
python3 setup.py /path/to/your-project --java
```

The script will:
1. Create `ai-context/` with all core files and empty subdirectories
2. Copy a `CLAUDE.md` stub to your project root (if none exists)
3. Copy a `.windsurf/rules.md` stub (if none exists)
4. Link skills as .md files under `.windsurf/workflows/` (Windsurf Cascade integration)
5. Link skills as directories under `.claude/skills/` (Claude Code integration)
6. If `--java` is passed, install Java unit testing and test data guidelines
7. Initialize darcs for local version control (if darcs is available)
8. Offer to add `ai-context/` to `.gitignore`

## What's Included

### Core (always installed)

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Architecture principles, coding guidelines, commit conventions |
| `0-index.md` | Directory guide — AI agents read this first |
| `architecture/domain-explanation.md` | Template — fill in your project's domain concepts |
| `guidelines/DEVELOPMENT_PROCESS.md` | Planning, implementation, and session summary workflow |
| `guidelines/PR_DESCRIPTION_GUIDELINES.md` | PR description format with JIRA support |
| `guidelines/SCRIPT_SECURITY_GUIDELINES.md` | Security review checklist — required before modifying/executing scripts |
| `guidelines/BRIEF_CREATION_GUIDELINES.md` | Guidance on creating project briefs: timing, templates, quality checklist |
| `scripts/move-context-files.py` | Move files between ai-context subdirectories and update references |
| `scripts/migrate-filenames.py` | Rename session files to include sequential ordering numbers |
| `skills/` | Workflow skills: `/commitmsg` (commit messages), `/prmsg` (PR descriptions), `/session-save` (session summaries); linked to `.claude/skills/` and `.windsurf/workflows/` |
| `til/` | "Today I Learned" entries — project-specific discoveries, patterns, and design decisions |

### Modules (optional)

#### `--java` / `--tdd`

Installs Java-specific TDD guidelines:

| File | Purpose |
|------|---------|
| `JAVA_UNIT_TESTING_GUIDELINES.md` | JUnit 5 test structure, incremental TDD, AssertJ, Mockito |
| `JAVA_TEST_DATA_CREATION_GUIDELINES.md` | Records + builders pattern for test data |

When installed, cross-references are automatically patched into `DEVELOPMENT_PROCESS.md`, `0-index.md`, and `CLAUDE.md`.

## Directory Structure After Setup

```
your-project/
├── CLAUDE.md                         # Stub → ai-context/CLAUDE.md
├── .windsurf/
│   ├── rules.md                      # Stub → ai-context/CLAUDE.md
│   └── workflows/
│       ├── commitmsg.md              # → ai-context/skills/commitmsg/SKILL.md
│       ├── prmsg.md                  # → ai-context/skills/prmsg/SKILL.md
│       └── session-save.md           # → ai-context/skills/session-save/SKILL.md
├── .claude/
│   └── skills/
│       ├── commitmsg/                # → ai-context/skills/commitmsg/
│       ├── prmsg/                    # → ai-context/skills/prmsg/
│       └── session-save/             # → ai-context/skills/session-save/
└── ai-context/
    ├── 0-index.md
    ├── CLAUDE.md
    ├── architecture/
    │   ├── 00-architecture-index.md
    │   └── 01-domain-explanation.md
    ├── briefs/
    │   └── 00-about-briefs.md
    ├── guidelines/
    │   ├── DEVELOPMENT_PROCESS.md
    │   ├── PR_DESCRIPTION_GUIDELINES.md
    │   ├── SCRIPT_SECURITY_GUIDELINES.md
    │   └── BRIEF_CREATION_GUIDELINES.md
    ├── scripts/
    │   ├── move-context-files.py
    │   └── migrate-filenames.py
    ├── skills/
    │   ├── commitmsg/
    │   │   └── SKILL.md
    │   ├── prmsg/
    │   │   └── SKILL.md
    │   └── session-save/
    │       └── SKILL.md
    ├── sessions/                      # Session notes go here
    ├── til/                           # Today I Learned entries
    ├── reference/                     # API specs, schemas
    ├── external/                      # Context from other projects
    ├── test-data/                     # Test data files
    └── archive/                       # Outdated files
```

## Documentation Hierarchy

The template uses a three-level hierarchy for project context:

1. **Architecture** (`architecture/`) — Stable, foundational documentation
   - Domain concepts and problem space
   - System design principles and constraints
   - Read at project start to understand "what problem are we solving"

2. **Briefs** (`briefs/`) — Project orientation documents
   - High-level summaries of work in progress
   - Context for multi-session efforts
   - Read when resuming work or joining the project
   - See `BRIEF_CREATION_GUIDELINES.md` for when and how to write briefs

3. **Sessions** (`sessions/`) — Detailed conversation history
   - Day-by-day development notes
   - Specific implementations, decisions, and learnings
   - Read for technical details on completed work

## After Setup

1. **Fill in `architecture/domain-explanation.md`** with your project's core concepts
2. **Review `CLAUDE.md`** and adjust architecture principles to your preferences
3. **Start a session** — tell the AI to read `ai-context/0-index.md` first

## About Loading Project Rules in New Sessions

**The challenge:** Each new AI session starts with blank context. Without explicit configuration, agents must decide when to load `CLAUDE.md` and `0-index.md`. This creates a choice between:

- **Efficiency**: Load rules only when they seem relevant (saves tokens for quick questions)
- **Consistency**: Always load rules first (ensures every session operates under the same constraints)

**How you can ensure rules are loaded:**

1. **Per prompt** — Manually ask agents to read `ai-context/0-index.md` at the start of your first message each session
2. **Per project** — Some tools support configuration files that agents read automatically; you could create `.claude/project-config.json` to specify auto-load files
3. **Team process** — Document in your team's onboarding that all AI-assisted work starts with reading the rules

The best approach depends on your team's preference and tooling. For critical projects with multiple team members, explicit configuration or process is recommended.

## Adding New Modules

To create a new module:

1. Create a directory under `modules/` (e.g., `modules/python-pytest/`)
2. Add your guideline files there
3. Update `setup.py` to:
   - Accept a new flag (e.g., `--python`)
   - Copy the module files into `ai-context/guidelines/`
   - Patch cross-references in `DEVELOPMENT_PROCESS.md`, `0-index.md`, and `CLAUDE.md`

## Why darcs?

The `ai-context/` directory is excluded from git (it's local-only). Darcs provides lightweight local version control without interfering with git. It lets you track changes to your AI context files independently.

If darcs isn't installed, everything still works — you just won't have version history for the context directory.

Install darcs: https://darcs.net/
