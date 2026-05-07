# ai-context-template

A template for bootstrapping an `ai-context/` directory in any project. Provides a structured folder layout, coding guidelines, and workflow conventions that make AI-assisted development more effective.

## Disclaimer

This template represents my best effort to systematize AI-assisted development practices. I'm not an expert in this rapidly evolving field. I'm learning and iterating as the industry evolves. The approaches here are validated by recent industry trends (see **Comparison** section), but your team should adapt and customize these patterns to fit your own needs.

## Quick Start

```bash
# Basic setup (all projects)
python3 setup.py /path/to/your-project

# With Java TDD guidelines
python3 setup.py /path/to/your-project --java --tdd
```

The script will:

1. Create `ai-context/` with all core files and empty subdirectories
2. Copy a `CLAUDE.md` stub to your project root (if none exists)
3. Copy a `.windsurf/rules.md` stub (if none exists)
4. Link skills as .md files under `.windsurf/workflows/` (Windsurf Cascade integration)
5. Link skills as directories under `.claude/skills/` (Claude Code integration)
6. Link skills as directories under `.opencode/skills/` (OpenCode integration)
7. Link skills as directories under `.agents/skills/` (Codex integration)
8. If `--java` is passed, install Java unit testing and test data guidelines
9. Initialize darcs for local version control (if darcs is available)
10. Offer to add `ai-context/` to `.gitignore`

## What's Included

### Core (always installed)

| File                                       | Purpose                                                                                                                                                                                                           |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE.md`                                | Architecture principles, coding guidelines, commit conventions                                                                                                                                                    |
| `0-index.md`                               | Directory guide — AI agents read this first                                                                                                                                                                       |
| `architecture/domain-explanation.md`       | Template — fill in your project's domain concepts                                                                                                                                                                 |
| `guidelines/DEVELOPMENT_PROCESS.md`        | Planning, implementation, and session summary workflow                                                                                                                                                            |
| `guidelines/PR_DESCRIPTION_GUIDELINES.md`  | PR description format with JIRA support                                                                                                                                                                           |
| `guidelines/SCRIPT_SECURITY_GUIDELINES.md` | Security review checklist — required before modifying/executing scripts                                                                                                                                           |
| `guidelines/BRIEF_CREATION_GUIDELINES.md`  | Guidance on creating project briefs: timing, templates, quality checklist                                                                                                                                         |
| `scripts/move-context-files.py`            | Move files between ai-context subdirectories and update references                                                                                                                                                |
| `scripts/migrate-filenames.py`             | Rename session files to include sequential ordering numbers                                                                                                                                                       |
| `skills/`                                  | Workflow skills: `/commitmsg` (commit messages), `/prmsg` (PR descriptions), `/session-save` (session summaries); linked to `.claude/skills/`, `.opencode/skills/`, `.agents/skills/`, and `.windsurf/workflows/` |
| `til/`                                     | "Today I Learned" entries — project-specific discoveries, patterns, and design decisions                                                                                                                          |

### Modules (optional)

#### `--java` / `--tdd`

Installs Java-specific TDD guidelines:

| File                                    | Purpose                                                   |
| --------------------------------------- | --------------------------------------------------------- |
| `JAVA_UNIT_TESTING_GUIDELINES.md`       | JUnit 5 test structure, incremental TDD, AssertJ, Mockito |
| `JAVA_TEST_DATA_CREATION_GUIDELINES.md` | Records + builders pattern for test data                  |

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
├── .opencode/
│   └── skills/
│       ├── commitmsg/                # → ai-context/skills/commitmsg/
│       ├── prmsg/                    # → ai-context/skills/prmsg/
│       └── session-save/             # → ai-context/skills/session-save/
├── .agents/
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

your-project/
├── CLAUDE.md # Stub → ai-context/CLAUDE.md
├── .windsurf/
│ ├── rules.md # Stub → ai-context/CLAUDE.md
│ └── workflows/
│ ├── commitmsg.md # → ai-context/skills/commitmsg/SKILL.md
│ ├── prmsg.md # → ai-context/skills/prmsg/SKILL.md
│ └── session-save.md # → ai-context/skills/session-save/SKILL.md
├── .claude/
│ └── skills/
│ ├── commitmsg/ # → ai-context/skills/commitmsg/
│ ├── prmsg/ # → ai-context/skills/prmsg/
│ └── session-save/ # → ai-context/skills/session-save/
└── ai-context/
├── 0-index.md
├── CLAUDE.md
├── architecture/
│ ├── 00-architecture-index.md
│ └── 01-domain-explanation.md
├── briefs/
│ └── 00-about-briefs.md
├── guidelines/
│ ├── DEVELOPMENT_PROCESS.md
│ ├── PR_DESCRIPTION_GUIDELINES.md
│ ├── SCRIPT_SECURITY_GUIDELINES.md
│ └── BRIEF_CREATION_GUIDELINES.md
├── scripts/
│ ├── move-context-files.py
│ └── migrate-filenames.py
├── skills/
│ ├── commitmsg/
│ │ └── SKILL.md
│ ├── prmsg/
│ │ └── SKILL.md
│ └── session-save/
│ └── SKILL.md
├── sessions/ # Session notes go here
├── til/ # Today I Learned entries
├── reference/ # API specs, schemas
├── external/ # Context from other projects
├── test-data/ # Test data files
└── archive/ # Outdated files

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

## About Darcs and Version Control

**Why darcs?**

The primary reason: Claude CLI's autocomplete breaks when it encounters nested `.git` folders. By using darcs for the `ai-context/` directory instead of git, we avoid nested VCS conflicts. This preserves autocomplete functionality while keeping the context directory version-controlled separately.

(Note: The agent still recognizes and can work with files even when autocomplete is broken, so this is a UX improvement, not a hard blocker.)

**If darcs isn't installed:**
Everything still works—you just won't have version history for the context directory. This is fine for many workflows.

**Install darcs:** https://darcs.net/

**TODO:** Future versions of this template will let you choose your VCS strategy during setup: use git, use darcs, or skip version control for ai-context/ entirely. This will accommodate different team preferences and CLI tooling.

## How This Compares to Other Approaches

### Core Inspiration

This template's architecture philosophy is built on work by [Alexander Dunlop](https://github.com/Alexanderdunlop/ai-architecture-prompts), who adapted principles from Eskil Steenberg's lecture on "Architecting LARGE Software Projects." The black-box modularity approach (treating modules as replaceable units with clean interfaces) comes directly from that foundation. Credit to Alexander for systematizing these ideas.

### Industry Context

Recent industry research (2025-2026) validates the approach:

- **Context Engineering**: Tools like Google's Conductor now solve the same problem this template addresses—persistent, structured project context for AI agents
- **Spec-Driven Development**: The emphasis on briefs and architecture before implementation aligns with emerging best practices that reduce AI-generated technical debt
- **Documentation Hierarchy**: The three-level structure (architecture → briefs → sessions) reflects how teams are organizing AI-assisted development context

See [Context Engineering: A Complete Guide 2026](https://codeconductor.ai/blog/context-engineering/) and [Spec-Driven Development alignment](https://www.webuild-ai.com/insights/aligning-spec-driven-development-and-context-engineering-for-2026) for more.

### What Makes This Template Different

- **Setup automation**: Bootstraps the full structure with one command, not manual file creation
- **IDE integration**: Links skills to Claude Code, OpenCode, Codex, and Windsurf out of the box
- **Opinionated but customizable**: Ships with architecture principles you can modify, rather than being blank

### When to Use This vs. Roll Your Own

Use this template if you want:

- A structured starting point for multiple projects
- Opinions on AI-assisted development workflow
- Integration with Claude Code, OpenCode, Codex, or Windsurf
- Automated skill linking and setup

Roll your own if you:

- Prefer minimal structure
- Have deeply different IDE/tooling requirements
- Want to build your own philosophy from scratch
```
