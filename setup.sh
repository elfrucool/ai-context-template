#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────────────────────────────
# ai-context-template setup script
#
# Usage: ./setup.sh <target-project-path> [--java] [--tdd]
#
#   --java  Include Java unit testing and test data creation guidelines
#   --tdd   Alias for --java (same effect)
# ──────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Parse arguments ──────────────────────────────────────────────────

JAVA=false
TARGET=""

for arg in "$@"; do
    case "$arg" in
        --java|--tdd)
            JAVA=true
            ;;
        -*)
            echo "Unknown option: $arg" >&2
            echo "Usage: $0 <target-project-path> [--java] [--tdd]" >&2
            exit 1
            ;;
        *)
            if [ -z "$TARGET" ]; then
                TARGET="$arg"
            else
                echo "Error: multiple target paths provided" >&2
                exit 1
            fi
            ;;
    esac
done

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target-project-path> [--java] [--tdd]" >&2
    exit 1
fi

# Resolve to absolute path
TARGET="$(cd "$TARGET" 2>/dev/null && pwd)" || {
    echo "Error: target path does not exist or is not a directory: $TARGET" >&2
    exit 1
}

# ── Validate ─────────────────────────────────────────────────────────

if [ ! -d "$TARGET" ]; then
    echo "Error: target is not a directory: $TARGET" >&2
    exit 1
fi

AI_CONTEXT="$TARGET/ai-context"

if [ -d "$AI_CONTEXT" ]; then
    echo "Error: $AI_CONTEXT already exists. Aborting to avoid overwriting." >&2
    exit 1
fi

# ── Create directory structure ───────────────────────────────────────

echo "Creating ai-context/ in $TARGET ..."

mkdir -p "$AI_CONTEXT"/{guidelines,scripts,sessions,til,reference,external,test-data,archive}

# ── Copy core files ──────────────────────────────────────────────────

cp "$SCRIPT_DIR/core/CLAUDE.md"      "$AI_CONTEXT/CLAUDE.md"
cp "$SCRIPT_DIR/core/0-index.md"     "$AI_CONTEXT/0-index.md"

cp "$SCRIPT_DIR/core/guidelines/DEVELOPMENT_PROCESS.md"       "$AI_CONTEXT/guidelines/"
cp "$SCRIPT_DIR/core/guidelines/PR_DESCRIPTION_GUIDELINES.md"  "$AI_CONTEXT/guidelines/"
cp "$SCRIPT_DIR/core/guidelines/domain-explanation.md"          "$AI_CONTEXT/guidelines/"

cp "$SCRIPT_DIR/core/scripts/move-context-files.py"  "$AI_CONTEXT/scripts/"
cp "$SCRIPT_DIR/core/scripts/migrate-filenames.py"   "$AI_CONTEXT/scripts/"

# ── Optional: Java TDD module ───────────────────────────────────────

if $JAVA; then
    echo "Installing Java TDD module ..."

    cp "$SCRIPT_DIR/modules/java-tdd/JAVA_UNIT_TESTING_GUIDELINES.md"      "$AI_CONTEXT/guidelines/"
    cp "$SCRIPT_DIR/modules/java-tdd/JAVA_TEST_DATA_CREATION_GUIDELINES.md" "$AI_CONTEXT/guidelines/"

    # Patch DEVELOPMENT_PROCESS.md: add Java cross-references
    sed -i 's|^- See language-specific guidelines in `guidelines/` if available$|- `JAVA_UNIT_TESTING_GUIDELINES.md` - TDD approach, test structure, assertions\n- `JAVA_TEST_DATA_CREATION_GUIDELINES.md` - Test data patterns, records, builders|' \
        "$AI_CONTEXT/guidelines/DEVELOPMENT_PROCESS.md"

    # Patch DEVELOPMENT_PROCESS.md: add Java refs in implementation section
    sed -i 's|^Implementation follows guidelines defined in language-specific files in `guidelines/` if available\.$|Implementation follows guidelines defined in:\n- `JAVA_UNIT_TESTING_GUIDELINES.md` - Test-first development, incremental approach\n- `JAVA_TEST_DATA_CREATION_GUIDELINES.md` - Creating reusable test data|' \
        "$AI_CONTEXT/guidelines/DEVELOPMENT_PROCESS.md"

    # Patch 0-index.md: add Java guideline listings
    sed -i 's|^<!-- Add language-specific guidelines here when installed (e.g., JAVA_\*\.md) -->$|- `JAVA_UNIT_TESTING_GUIDELINES.md` - Test structure, incremental TDD, assertions\n- `JAVA_TEST_DATA_CREATION_GUIDELINES.md` - Test data records, builders|' \
        "$AI_CONTEXT/0-index.md"

    # Patch CLAUDE.md: add Java coding patterns reference
    sed -i 's|^3\. Coding patterns → see language-specific guidelines in `ai-context/guidelines/` if available$|3. Coding patterns → `ai-context/guidelines/JAVA_*.md`|' \
        "$AI_CONTEXT/CLAUDE.md"
fi

# ── Root CLAUDE.md stub ──────────────────────────────────────────────

if [ ! -f "$TARGET/CLAUDE.md" ]; then
    cp "$SCRIPT_DIR/core/root-CLAUDE.md" "$TARGET/CLAUDE.md"
    echo "Created $TARGET/CLAUDE.md (stub → ai-context/CLAUDE.md)"
else
    echo "Skipped $TARGET/CLAUDE.md (already exists)"
fi

# ── Windsurf rules stub ──────────────────────────────────────────────

if [ ! -f "$TARGET/.windsurf/rules.md" ]; then
    mkdir -p "$TARGET/.windsurf"
    cp "$SCRIPT_DIR/core/root-windsurf-rules.md" "$TARGET/.windsurf/rules.md"
    echo "Created $TARGET/.windsurf/rules.md (stub → ai-context/CLAUDE.md)"
else
    echo "Skipped $TARGET/.windsurf/rules.md (already exists)"
fi

# ── Darcs initialization ─────────────────────────────────────────────

if command -v darcs &>/dev/null; then
    echo "Initializing darcs in ai-context/ ..."
    (
        cd "$AI_CONTEXT"
        darcs init
        darcs add -r .
        darcs record -a -m "Initial ai-context setup"
    )
    echo "Darcs initialized with initial recording."
else
    echo ""
    echo "Tip: Install darcs for local version control of ai-context/."
    echo "  It keeps history without polluting git. See: https://darcs.net/"
fi

# ── .gitignore prompt ─────────────────────────────────────────────────

GITIGNORE="$TARGET/.gitignore"
ENTRY="ai-context/"

already_ignored=false
if [ -f "$GITIGNORE" ]; then
    if grep -qxF "$ENTRY" "$GITIGNORE" 2>/dev/null; then
        already_ignored=true
    fi
fi

if ! $already_ignored; then
    echo ""
    read -rp "Add ai-context/ to .gitignore? [Y/n] " answer
    answer="${answer:-Y}"
    if [[ "$answer" =~ ^[Yy] ]]; then
        echo "$ENTRY" >> "$GITIGNORE"
        echo "Added '$ENTRY' to .gitignore"
    else
        echo "Skipped .gitignore update."
    fi
else
    echo "ai-context/ is already in .gitignore."
fi

# ── Summary ───────────────────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════════════════════"
echo " ai-context setup complete!"
echo "══════════════════════════════════════════════════════════════"
echo ""
echo " Installed in: $AI_CONTEXT"
echo ""
echo " Directories:"
echo "   guidelines/  - Coding standards and domain knowledge"
echo "   sessions/    - Session notes (YYYY-MM-DD-XX-<topic>.md)"
echo "   til/         - Today I Learned entries"
echo "   reference/   - API specs and schemas"
echo "   external/    - Context from other projects"
echo "   test-data/   - Test data files"
echo "   scripts/     - Utility scripts"
echo "   archive/     - Outdated files"
echo ""
echo " Files:"
echo "   CLAUDE.md                              - Architecture principles"
echo "   0-index.md                             - Directory guide"
echo "   guidelines/DEVELOPMENT_PROCESS.md      - Workflow process"
echo "   guidelines/PR_DESCRIPTION_GUIDELINES.md - PR format"
echo "   guidelines/domain-explanation.md        - Domain concepts (fill in!)"
if $JAVA; then
echo "   guidelines/JAVA_UNIT_TESTING_GUIDELINES.md      - Java TDD"
echo "   guidelines/JAVA_TEST_DATA_CREATION_GUIDELINES.md - Test data patterns"
fi
echo "   scripts/move-context-files.py          - Move files + update refs"
echo "   scripts/migrate-filenames.py           - Rename session files"
echo ""
echo " Next steps:"
echo "   1. Fill in guidelines/domain-explanation.md with your project's concepts"
echo "   2. Review CLAUDE.md and adjust to your preferences"
echo "   3. Start a session and let the AI read 0-index.md first"
echo ""
