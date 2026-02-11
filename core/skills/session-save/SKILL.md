# `/session-save` - Automated Session Summaries

Automate end-of-session documentation following the standard template, eliminating repeated format explanations.

## How It Works

### Step 1: Auto-detect Date and Sequential Number

1. **Current date**: Use today's date in `YYYY-MM-DD` format
2. **Determine XX number**:
   - Scan `ai-context/sessions/` for files matching today's date
   - Find the highest XX number (00, 01, 02...)
   - Increment by 1 for the new file
   - **Special case**: If a related plan file exists with the same base topic, use its XX number instead

**Example**:
- Existing: `2026-02-11-00-auth-refactoring-plan.md`
- New implementation summary should be: `2026-02-11-00-auth-refactoring.md` (same XX)
- Separate task: `2026-02-11-01-test-cleanup.md` (incremented XX)

### Step 2: Suggest Topic

Analyze git diff and conversation context to suggest a topic:

1. **From git diff**:
   - Look at changed file paths (e.g., `src/auth/` → "authentication")
   - Look at change types (new files, refactoring, fixes)
   - Extract key terms from file names

2. **From conversation context**:
   - Look at issue numbers, feature names mentioned
   - Look at plan files if they exist
   - Look at previous session topics

3. **Suggest to user**:
   - "Suggested topic: 'authentication-refactoring'. Use this or provide your own?"
   - Wait for user confirmation or override
   - Use kebab-case (lowercase with hyphens)

### Step 3: Generate Summary

Generate a summary following the template from `guidelines/DEVELOPMENT_PROCESS.md` lines 177-207:

```markdown
# <Title>

**Date**: YYYY-MM-DD
**Status**: Completed / In Progress / Paused

## Overview
Brief description of what was done (2-3 sentences)

## Key Decisions
- **Decision 1**: Reasoning behind it
- **Decision 2**: Reasoning behind it

## Technical Details
(Optional - include when helpful for future reference)
- Code patterns introduced
- Architecture notes
- Important file locations

## Current State
- What's working
- What's been tested
- What's pending (if any)

## Follow-up / TODO
(If work is incomplete or follow-up tasks identified)
- [ ] Task 1
- [ ] Task 2
```

### Step 4: Save File

Save to: `ai-context/sessions/YYYY-MM-DD-XX-<topic>.md`

**Ask the user before saving**: "Should I save this to `ai-context/sessions/2026-02-11-01-authentication.md`?"

## What to Include

From `DEVELOPMENT_PROCESS.md`:

- **Overview**: 2-3 sentences summarizing what was done
- **Key Decisions**: Major choices made and why
- **Technical Details**: Patterns, architecture notes, file locations (optional)
- **Current State**: What works, what's tested, what's pending
- **Follow-up/TODO**: Next steps or incomplete work

## What NOT to Include

- Implementation details that are obvious from the code
- Commit-by-commit breakdown
- Excessive code snippets (reference file:line instead)
- PR description content (that belongs in PR-specific files)

## Status Guidelines

- **Completed**: Work is done and tested
- **In Progress**: Work is ongoing, this is a checkpoint
- **Paused**: Work stopped mid-task, needs context preservation

## Implementation Steps

When invoked:

1. **Get current date**:
   ```bash
   date +%Y-%m-%d
   ```

2. **Scan existing session files**:
   ```bash
   ls ai-context/sessions/ | grep "^$(date +%Y-%m-%d)-"
   ```
   - Parse filenames to extract XX numbers
   - Find highest XX, increment by 1
   - Check if a related -plan file exists with same base topic

3. **Analyze changes for topic suggestion**:
   ```bash
   git diff --name-only HEAD
   git status --short
   ```
   - Extract directory names and file names
   - Look for patterns: "auth", "api", "test", etc.
   - Consider conversation context (mentioned features, issues)

4. **Suggest topic**:
   - Present: "Suggested topic: 'authentication-refactoring'. Use this or provide your own?"
   - Wait for user response
   - Validate: lowercase, kebab-case, no special chars except hyphens

5. **Read context**:
   - Read related session files (if this is session 02, read session 01)
   - Read current conversation context
   - Run `git diff HEAD` to see changes
   - Consider plan file if it exists

6. **Generate summary**:
   - Title: Derived from topic (e.g., "Authentication Refactoring")
   - Date: Today's date
   - Status: Ask user or infer from context (Completed if tests pass, In Progress otherwise)
   - Overview: 2-3 sentences from conversation + git diff
   - Key Decisions: Extract from conversation (what choices were made and why)
   - Technical Details: Patterns, file locations, architecture
   - Current State: What works, what's tested, what's pending
   - Follow-up: Extract TODO items from conversation or incomplete work

7. **Show preview**:
   - Display the generated summary
   - Ask: "Should I save this to `ai-context/sessions/YYYY-MM-DD-XX-<topic>.md`?"

8. **Save file**:
   - Write to the file path
   - Confirm: "Session saved to `ai-context/sessions/YYYY-MM-DD-XX-<topic>.md`"

## Special Cases

### Implementation Following a Plan

If a plan file exists (e.g., `2026-02-11-00-auth-refactoring-plan.md`):
- Use the **same XX number** for the implementation summary
- File name: `2026-02-11-00-auth-refactoring.md` (no -plan suffix)
- Reference the plan file in the Overview or Technical Details section

### Multi-Session Work

If this is session 02 or later for the same topic:
- Increment the XX number (e.g., 00 → 01 → 02)
- Read previous session files for continuity
- In Overview, reference what was done in previous sessions
- Example: "This session continues the authentication refactoring from session 01..."

### Partial/Paused Sessions

If the user needs to leave mid-session:
- Set Status to "Paused"
- In Current State, clearly mark what's pending
- In Follow-up/TODO, list next steps
- Partial summaries are acceptable and encouraged

## Examples

### Example 1: Implementation Following a Plan

```
Existing file: ai-context/sessions/2026-02-11-00-auth-refactoring-plan.md

User: /session-save

Claude: I found a plan file with XX number 00. I'll use the same number for the implementation summary.

Analyzing changes...

Suggested topic: 'auth-refactoring' (matches the plan file). Use this or provide your own?

User: Use that

Claude: (generates summary)

Should I save this to `ai-context/sessions/2026-02-11-00-auth-refactoring.md`?

User: Yes

Claude: Session saved to `ai-context/sessions/2026-02-11-00-auth-refactoring.md`
```

### Example 2: New Session, No Plan

```
User: /session-save

Claude: Analyzing changes...

I see changes in:
- src/test/data/
- scripts/cleanup.sh

Suggested topic: 'test-data-cleanup'. Use this or provide your own?

User: Use that

Claude: This will be session 01 for today (session 00 was auth-refactoring).

(generates summary)

Should I save this to `ai-context/sessions/2026-02-11-01-test-data-cleanup.md`?

User: Yes

Claude: Session saved to `ai-context/sessions/2026-02-11-01-test-data-cleanup.md`
```

### Example 3: Continue Previous Session

```
Existing file: ai-context/sessions/2026-02-10-00-api-migration.md (Status: Paused)

User: /session-save

Claude: Analyzing changes...

I found a related session from yesterday: '2026-02-10-00-api-migration.md' (Status: Paused).

Is this a continuation of that work?

User: Yes

Claude: Suggested topic: 'api-migration-part2' or 'api-migration-continued'. Which do you prefer?

User: Use 'api-migration-continued'

Claude: This will be session 00 for today.

(generates summary, references yesterday's session in Overview)

Should I save this to `ai-context/sessions/2026-02-11-00-api-migration-continued.md`?

User: Yes

Claude: Session saved to `ai-context/sessions/2026-02-11-00-api-migration-continued.md`
```

### Example 4: User Provides Custom Topic

```
User: /session-save

Claude: Analyzing changes...

Suggested topic: 'database-refactoring'. Use this or provide your own?

User: Use 'postgres-migration-preparation' instead

Claude: (generates summary with user's topic)

Should I save this to `ai-context/sessions/2026-02-11-00-postgres-migration-preparation.md`?

User: Yes

Claude: Session saved.
```

## Topic Naming Guidelines

- Use kebab-case (lowercase with hyphens)
- Be specific but concise (2-4 words)
- Avoid generic terms like "work" or "changes"
- Match existing conventions in the repository
- Examples:
  - Good: `auth-refactoring`, `test-cleanup`, `api-v2-migration`
  - Bad: `work`, `changes`, `stuff`, `MyFeature`

## When to Use This Skill

From `DEVELOPMENT_PROCESS.md` lines 151-158:

Create a session summary when:
- Significant work completed (refactoring, feature, architecture)
- Major decisions made that affect future work
- Work paused mid-task and context needs preservation

**Always ask the user** before creating a session summary.

Partial summaries are acceptable if the user needs to leave mid-session.

## Tips

- The skill automatically determines the correct XX number — you don't need to specify it
- If the suggested topic is wrong, just provide your own
- The skill reads previous session files for continuity automatically
- If you're implementing a plan, the skill detects the plan file and uses the same XX number
- You can invoke this skill multiple times per day for different tasks (XX numbers will increment)

## References

- Session file structure and naming: `guidelines/DEVELOPMENT_PROCESS.md` lines 164-207
- Sequential numbering logic: `scripts/migrate-filenames.py` lines 1-162
- When to create summaries: `core/DEVELOPMENT_PROCESS.md` lines 151-158
