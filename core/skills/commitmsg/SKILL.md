# `/commitmsg` - Smart Commit Message Generation

Generate commit messages that cover the **full scope** of work across related sessions, not just the last edit.

## How It Works

### Default Behavior (Smart Git-Based Scope Detection)

1. **Find uncommitted changes**:
   - Run `git diff --name-only HEAD` to get uncommitted files
   - Run `git log -1 --format=%cd --date=iso` on each file to get last commit timestamp
   - For new files, use current timestamp

2. **Find related session files**:
   - Scan `ai-context/sessions/` for files with dates >= oldest uncommitted file timestamp
   - Read those session files to understand the full context of work
   - If no session files found, use git diff and current conversation context

3. **Generate commit message**:
   - Analyze ALL changes in scope (not just the most recent edit)
   - Follow the commit message format from `CLAUDE.md` § Commit Messages

### Parameter Overrides

Users can override the default scope detection:

- **Time-based**: `args: "since yesterday"`, `args: "since 2026-02-01"`, `args: "last 3 days"`
  - Filters session files by date range
  - Still reads git diff for actual changes

- **Topic-based**: `args: "about authentication"`, `args: "related to API"`
  - Filters session files by keyword in filename or content
  - Still reads git diff for actual changes

- **Combined**: `args: "since yesterday about authentication"`
  - Applies both filters

## Output Format

The commit message must follow these specifications (from `CLAUDE.md` lines 81-92):

1. **Subject line**:
   - Imperative verb (e.g., "Fix", "Add", "Refactor", "Update")
   - 50 characters soft limit
   - No period at the end

2. **Body**:
   - Explain **what** changed and **why** (not how — the diff shows how)
   - Wrapped at 72 characters
   - Leave blank line between subject and body
   - Character limits are soft, not hard

3. **Signature**:
   - End with: `Signed-off-by: <Name> <Email>`
   - Use git config to get user name and email

4. **Format for copy-paste**:
   - Output in a code block so the user can copy directly
   - Example:
   ```
   Subject line here

   Body paragraph explaining what changed and why. This should be
   wrapped at 72 characters for readability in git log and other
   tools.

   Signed-off-by: Name <email@example.com>
   ```

## What to Exclude

- Changes in `ai-context/`, `.vscode/`, `.windsurf/`, and similar directories (unless explicitly requested)
- Generated files, build artifacts, dependencies (unless they're relevant to the change)
- Changes that were reverted or are no longer present in the diff

## Implementation Steps

When invoked:

1. **Parse arguments** (if provided):
   - Extract time filter: "since X", "last X days", date ranges
   - Extract topic filter: "about X", "related to X"

2. **Get uncommitted changes**:
   ```bash
   git diff --name-only HEAD
   git diff --cached --name-only  # staged files
   ```

3. **Find oldest relevant timestamp**:
   - For each uncommitted file, get its last commit date or current time if new
   - Find the oldest timestamp

4. **Scan session files**:
   - List files in `ai-context/sessions/` with `YYYY-MM-DD-XX-topic.md` pattern
   - Filter by date >= oldest timestamp (or user-provided time filter)
   - Filter by topic keyword if provided
   - Read the matching files

5. **Analyze changes**:
   - Run `git diff HEAD` to see actual changes
   - Consider context from session files
   - Consider current conversation context

6. **Generate message**:
   - Write subject line (imperative verb, ~50 chars)
   - Write body paragraphs (wrapped at 72 chars)
   - Add signature with git config user name and email
   - Format in a code block for easy copy-paste

7. **Ask for confirmation** (optional):
   - If the scope seems ambiguous or very large, ask: "This commit covers work from [date] onwards. Is that correct?"

## Examples

### Example 1: Default (git-based)

```
User: /commitmsg

Claude:
- Finds files changed since last commit
- Discovers relevant session files from the past 2 days
- Reads those sessions to understand full context
- Generates commit message covering all work

Output:
```
Add user authentication with JWT tokens

Implement JWT-based authentication to replace the previous
session-based approach. This change improves security and enables
stateless authentication for API endpoints.

Changes include:
- New AuthService with token generation and validation
- Middleware for protected routes
- Updated user login endpoint to return JWT
- Added token refresh mechanism

Signed-off-by: John Doe <john@example.com>
```
```

### Example 2: Time override

```
User: /commitmsg args: "since yesterday"

Claude:
- Filters session files to only those from yesterday onwards
- Reads git diff for actual changes
- Generates commit message

Output:
(commit message covering only yesterday's work)
```

### Example 3: Topic override

```
User: /commitmsg args: "about authentication"

Claude:
- Scans all session files for "authentication" keyword
- Reads matching sessions
- Generates commit message focused on auth changes

Output:
(commit message covering all authentication-related work)
```

## Tips

- The skill automatically handles multi-session work — no need to manually specify session files
- If the generated message is too broad, use parameter overrides to narrow the scope
- If the generated message is too narrow, check that relevant session files exist in `ai-context/sessions/`
- The skill respects git's index — only uncommitted or staged changes are included

## References

- Commit message format: `CLAUDE.md` lines 81-92
- Session file structure: `guidelines/DEVELOPMENT_PROCESS.md` lines 164-207
- Linus Torvalds' commit message advice: https://github.com/torvalds/subsurface-for-dirk/blob/a48494d2fbed58c751e9b7e8fbff88582f9b2d02/README#L88
