# `/prmsg` - PR Description Generation

Generate PR descriptions that include **full context** from multi-session work, following the repository's PR template format.

## How It Works

## Mode Requirements

**For Windsurf Cascade Agent**:
- If you are in Ask mode, stop and ask the user to switch to Code mode
- This skill requires git commands and file operations that are only available in Code mode

**For Claude CLI**:
- No special indication is required, Claude CLI knows how to require the user to authorize commands and modifications

### Step 1: Ask for JIRA Ticket (Required)

Before drafting the PR description, **always ask the user**:

1. Is there a JIRA ticket for this work?
2. If yes, what is the ticket code? (e.g., `OR-809`, `PROJ-123`)
3. Is there any overall context or background information not available in the code?

If there's no JIRA ticket, proceed without the ticket link. The PR description follows the same structure either way.

### Step 2: Smart Git-Based Scope Detection

Uses the same scope detection as `/commitmsg`:

1. **Find uncommitted changes** using `git diff --name-only HEAD`
2. **Find related session files** in `ai-context/sessions/` based on timestamps
3. **Read session files** to understand the full context of work
4. **Generate PR description** covering ALL work in scope

### Parameter Overrides

Same as `/commitmsg`:

- **Time-based**: `args: "since yesterday"`, `args: "since 2026-02-01"`, `args: "last 3 days"`
- **Topic-based**: `args: "about authentication"`, `args: "related to API"`
- **Combined**: `args: "since yesterday about authentication"`

## Output Format

The PR description follows `guidelines/PR_DESCRIPTION_GUIDELINES.md`:

### Title Field (separate)

Short imperative sentence describing the change:
- Example: `Fix user authentication for SSO login`
- Corresponds to the `#` heading in the draft

### Body Field

```markdown
## Summary
[PROJ-xxx](https://your-jira-instance.atlassian.net/browse/PROJ-xxx)

One or two paragraphs explaining **what** changed and **why**. Include context
that cannot be discovered from the code alone — the motivation, the trigger for
the change, or background that only the author knows.

### Detailed list of changes

- **Change A** — brief explanation
- **Change B** — brief explanation
- **Change C** — brief explanation

---

## Test Plan

- ✓ Test or verification step already done
- ✓ Another completed step
- Pending step (no checkmark)
```

**If there's no JIRA ticket**, omit the `[PROJ-xxx](...)` link line entirely.

## What to Include

From `PR_DESCRIPTION_GUIDELINES.md`:

- **Summary paragraph**: Explain the what and why in plain language. Add context the reviewer cannot infer from the diff — motivation, how the problem was discovered, relevant history.
- **Detailed list of changes**: One bullet per logical change. Bold the change, dash, then the explanation.
- **Test plan**: List what was tested and how. Use `✓` for completed items. If testing is pending, list steps without checkmarks.

## What NOT to Include

From `PR_DESCRIPTION_GUIDELINES.md`:

- Session metadata (`Date`, `Branch`, `Status`) — this is a PR description, not a session note
- Architectural deep-dives or design decision rationale — that belongs in session summaries
- Individual commit messages or commit-by-commit breakdowns
- Files-for-review lists or review checklists — the reviewer decides what to look at
- Internal jargon like "Phase 1, Phase 2" from the development process

## Implementation Steps

When invoked:

1. **Ask for JIRA ticket**:
   - "Is there a JIRA ticket for this work?"
   - If yes: "What's the ticket code?" and "Any context not in the code?"
   - If no: proceed without ticket link

2. **Parse arguments** (if provided):
   - Extract time filter: "since X", "last X days"
   - Extract topic filter: "about X", "related to X"

3. **Get uncommitted changes**:
   ```bash
   git diff --name-only HEAD
   git diff --cached --name-only
   ```

4. **Find relevant session files**:
   - List files in `ai-context/sessions/` with `YYYY-MM-DD-XX-topic.md` pattern
   - Filter by date/topic based on git changes or user parameters
   - Read matching session files

5. **Analyze changes**:
   - Run `git diff HEAD` to see actual changes
   - Consider context from session files
   - Consider current conversation context
   - Consider user-provided background context

6. **Generate PR description**:
   - **Title**: Short imperative sentence (~50 chars)
   - **Summary**: 1-2 paragraphs with what/why + context
   - **Detailed changes**: Bullet list with **bold** items
   - **Test Plan**: List with `✓` for completed, no checkmark for pending

7. **Output in copy-paste format**:
   - Show title separately: "**Title**: [title text]"
   - Show body in markdown code block
   - User can paste directly into GitHub PR form

## Draft File Convention

PR descriptions should be saved as session files:

`ai-context/sessions/YYYY-MM-DD-XX-<topic>-PR.md`

The file uses:
- `#` for the title (what goes in the title field)
- `##` for the body sections (Summary, Test Plan)

**Note**: This skill generates the PR description but does NOT automatically save it as a draft file. If the user wants to save it, ask them to confirm and then write the file.

## Examples

### Example 1: With JIRA ticket

```
User: /prmsg

Claude: Is there a JIRA ticket for this work?
User: Yes, OR-809

Claude: What's the ticket code?
(Wait, user already provided it)

Claude: Any additional context not in the code?
User: This was triggered by customer complaints about slow login

Claude:
(Reads session files, analyzes git diff, generates PR description)

**Title**: Fix user authentication for SSO login

**Body**:
```markdown
## Summary
[OR-809](https://your-jira.atlassian.net/browse/OR-809)

This PR fixes slow SSO login times by implementing JWT-based authentication
to replace the previous session-based approach. The change was triggered by
customer complaints about 5-10 second delays during login. The new approach
reduces login time to under 500ms by eliminating database queries during
authentication.

### Detailed list of changes

- **AuthService** — new service with JWT token generation and validation
- **Protected route middleware** — validates JWT tokens for API endpoints
- **Login endpoint** — updated to return JWT instead of creating session
- **Token refresh** — added mechanism to refresh expired tokens without re-login

---

## Test Plan

- ✓ Manual testing with SSO provider (Okta)
- ✓ Unit tests for AuthService (95% coverage)
- ✓ Integration tests for protected endpoints
- ✓ Performance testing shows <500ms login time
- Load testing with 100 concurrent users
```
```

### Example 2: Without JIRA ticket

```
User: /prmsg

Claude: Is there a JIRA ticket for this work?
User: No

Claude:
(Generates PR description without ticket link)

**Title**: Add user authentication with JWT tokens

**Body**:
```markdown
## Summary

This PR implements JWT-based authentication to replace the previous
session-based approach. The change improves security and enables
stateless authentication for API endpoints.

### Detailed list of changes

- **AuthService** — new service with JWT token generation and validation
- **Protected route middleware** — validates JWT tokens for API endpoints
(... rest of description)
```
```

### Example 3: With time override

```
User: /prmsg args: "since yesterday"

Claude: Is there a JIRA ticket for this work?
User: No, this is just a quick fix

Claude:
(Reads only yesterday's session files, generates focused PR description)
```

## Tips

- The skill automatically handles multi-session work — reads relevant session files to understand full context
- If the PR description is too broad, use parameter overrides to narrow scope
- The Test Plan should reflect actual testing done — use `✓` for completed tests, no checkmark for pending
- Write for the reviewer — the summary paragraph is most important

## References

- PR description format: `guidelines/PR_DESCRIPTION_GUIDELINES.md` (full file)
- Session file structure: `guidelines/DEVELOPMENT_PROCESS.md` lines 164-207
- Commit message format (for merge commits): `CLAUDE.md` lines 81-92
