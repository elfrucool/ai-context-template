# ai-context-template

A template for bootstrapping an `ai-context/` directory in any project. Provides a structured folder layout, coding guidelines, and workflow conventions that make AI-assisted development more effective.

## Quick Start

```bash
# Basic setup (all projects)
./setup.sh /path/to/your-project

# With Java TDD guidelines
./setup.sh /path/to/your-project --java
```

The script will:
1. Create `ai-context/` with all core files and empty subdirectories
2. Copy a `CLAUDE.md` stub to your project root (if none exists)
3. Copy a `.windsurf/rules.md` stub (if none exists)
4. If `--java` is passed, install Java unit testing and test data guidelines
5. Initialize darcs for local version control (if darcs is available)
6. Offer to add `ai-context/` to `.gitignore`

## What's Included

### Core (always installed)

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Architecture principles, coding guidelines, commit conventions |
| `0-index.md` | Directory guide — AI agents read this first |
| `guidelines/DEVELOPMENT_PROCESS.md` | Planning, implementation, and session summary workflow |
| `guidelines/PR_DESCRIPTION_GUIDELINES.md` | PR description format with JIRA support |
| `guidelines/domain-explanation.md` | Template — fill in your project's domain concepts |
| `scripts/move-context-files.py` | Move files between ai-context subdirectories and update references |
| `scripts/migrate-filenames.py` | Rename session files to include sequential ordering numbers |
| `skills/` | Workflow skills: `/commitmsg` (commit messages), `/prmsg` (PR descriptions), `/session-save` (session summaries) |

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
│   └── rules.md                      # Stub → ai-context/CLAUDE.md
└── ai-context/
    ├── 0-index.md
    ├── CLAUDE.md
    ├── guidelines/
    │   ├── DEVELOPMENT_PROCESS.md
    │   ├── PR_DESCRIPTION_GUIDELINES.md
    │   └── domain-explanation.md
    ├── scripts/
    │   ├── move-context-files.py
    │   └── migrate-filenames.py
    ├── sessions/                      # Session notes go here
    ├── til/                           # Today I Learned entries
    ├── reference/                     # API specs, schemas
    ├── external/                      # Context from other projects
    ├── test-data/                     # Test data files
    └── archive/                       # Outdated files
```

## After Setup

1. **Fill in `guidelines/domain-explanation.md`** with your project's core concepts
2. **Review `CLAUDE.md`** and adjust architecture principles to your preferences
3. **Start a session** — tell the AI to read `ai-context/0-index.md` first

## Adding New Modules

To create a new module:

1. Create a directory under `modules/` (e.g., `modules/python-pytest/`)
2. Add your guideline files there
3. Update `setup.sh` to:
   - Accept a new flag (e.g., `--python`)
   - Copy the module files into `ai-context/guidelines/`
   - Patch cross-references in `DEVELOPMENT_PROCESS.md`, `0-index.md`, and `CLAUDE.md`

## Why darcs?

The `ai-context/` directory is excluded from git (it's local-only). Darcs provides lightweight local version control without interfering with git. It lets you track changes to your AI context files independently.

If darcs isn't installed, everything still works — you just won't have version history for the context directory.

Install darcs: https://darcs.net/
