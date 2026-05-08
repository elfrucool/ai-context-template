# AI Context Directory

This directory contains context, guidelines, and session history for AI assistants working on this codebase.

## Directory Structure

```
ai-context
├── 0-index.md
├── CLAUDE.md
├── _darcs
├── archive
├── external
├── guidelines
├── reference
├── scripts
├── sessions
├── til
└── test-data
```

### `CLAUDE.md`

Project-wide instructions for AI agents: architecture principles, coding guidelines, commit message conventions, and quick-reference pointers into this directory.

**Important:** The root `CLAUDE.md`, `AGENTS.md`, and `.windsurf/rules.md` are **symbolic links** pointing to `ai-context/CLAUDE.md`. They are NOT separate files - editing any of them modifies the same file.

### `architecture/`

Stable reference documentation for system design and core concepts. Read when you need to understand how the system works.

- `00-architecture-index.md` - Architecture overview and index
- `01-domain-explanation.md` - Core domain concepts (fill in for your project)

### `briefs/`

High-level summaries of major features and changes. Read a brief first to get oriented, then dive into `sessions/` only if you need implementation-level detail.

- `00-about-briefs.md` - Index of all briefs

### `guidelines/`

Stable coding standards and development processes. Read these before writing code.

- `DEVELOPMENT_PROCESS.md` - End-to-end workflow (planning, implementation, summaries)
- `BRIEF_CREATION_GUIDELINES.md` - When and how to create feature briefs
- `PR_DESCRIPTION_GUIDELINES.md` - PR description structure, JIRA ticket conventions

<!-- Add language-specific guidelines here when installed (e.g., JAVA_*.md) -->

### `sessions/`

Dated session notes documenting implementation history and design decisions.
Files follow `YYYY-MM-DD-XX-<topic>.md` naming convention where `XX` is a sequential number (00, 01, 02...) for ordering multiple files on the same date.
Files with `-plan` suffix share the same `XX` as their implementation counterpart.
Check recent files (last 3-7 days) for current work context.

### `til/`

Today I Learned entries — concise learnings from debugging, investigation, or discovery.
Files follow `YYYY-MM-DD-XX-<title>.md` naming convention (same as sessions).
Title should identify the learning at a glance without needing to read the file.

### `reference/`

API specs, decompiled dependencies, and schemas for external/generated code.
Empty — add content as needed.

### `test-data/`

Data used for tests during development process.
Empty — add content as needed.

### `external/`

Context from separate projects and repos.
Empty — add content as needed.

### `scripts/`

Utility scripts for managing this directory.

- `migrate-filenames.py` - Renames session files to include sequential ordering numbers
- `move-context-files.py` - Moves files between ai-context subdirectories and updates references

### `skills/`

Claude Code skills for workflow automation.

- `/commitmsg` - Generate commit messages covering full session scope
- `/prmsg` - Generate PR descriptions with complete context
- `/session-save` - Save session summaries following standard format

### `archive/`

Outdated files kept for historical reference.
Empty — add content as needed.

## Notes

- This directory (ai-context) has its own darcs repo (if darcs is available) and is **not** tracked by the parent git repo since it is intended to be used locally only.
