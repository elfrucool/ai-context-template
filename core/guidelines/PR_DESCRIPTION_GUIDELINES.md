# PR Description Guidelines

## First Step: Ask for the JIRA Ticket

Before drafting a PR description, **always ask the user**:

1. Is there a JIRA ticket for this work?
2. What is the ticket code? (e.g., `OR-809`, `OR-192` or `FOO-9833`, i.e. `PROJECTCODE-number`)
3. Is there any overall context or background information not available in the code? (optional — there may be nothing to add)

If there is no ticket, omit the JIRA link. The PR description still follows the same structure.

## Structure

PR descriptions follow the repository's GitHub template (`.github/pull_request_template.md`) with two sections: **Summary** and **Test Plan**.

The description is split across two fields in the GitHub web form:

### Title field (separate input)

- Short imperative sentence describing the change
- Corresponds to the `#` heading in the draft file
- Example: `Fix user authentication for SSO login`

### Body field

```markdown
## Summary

[PROJ-xxx](https://TODO-YOUR-JIRA-INSTANCE.atlassian.net/browse/PROJ-xxx)

One or two paragraphs explaining **what** changed and **why**. Include context
that cannot be discovered from the code alone — the motivation, the trigger for
the change, or background that only the author knows.

### Detailed list of changes

- **Change A** — brief explanation
- **Change B** — brief explanation

---

## Test Plan

- ✓ Test or verification step already done
- ✓ Another completed step
- Pending step (no checkmark)
```

If there is no JIRA ticket, omit the `[PROJ-xxx](...)` link line entirely.

## Draft File Convention

PR description drafts are saved as session files:

`ai-context/sessions/YYYY-MM-DD-XX-<topic>-PR.md` (note the upper PR)

The file uses `#` for the title (what goes in the title field) and `##` for the body sections.

## What to Include

- **Summary paragraph**: Explain the what and why in plain language. Add context the reviewer cannot infer from the diff — motivation, how the problem was discovered, relevant history.
- **Detailed list of changes**: One bullet per logical change. Bold the change, dash, then the explanation.
- **Test plan**: List what was tested and how. Use `✓` for completed items.

## What NOT to Include

- Session metadata (`Date`, `Branch`, `Status`) — this is a PR description, not a session note
- Architectural deep-dives or design decision rationale — that belongs in session summaries
- Individual commit messages or commit-by-commit breakdowns
- Files-for-review lists or review checklists — the reviewer decides what to look at
- Internal jargon like "Phase 1, Phase 2" from the development process

## Merge Commit Message

After the PR is approved, produce a merge commit message from the same content. The commit message reuses the PR's summary and change list but adapted to commit message conventions (see `CLAUDE.md` § Commit Messages):

- **Subject line**: Same as the PR title — short imperative sentence (soft limit ~50 chars)
- **Body**: The summary paragraph(s) and detailed list of changes, but as plain text — no markdown formatting (no `**bold**`, no `[links](...)`, no `###` headings)
- **Wrap** the body at 72 characters
- **Omit**: Test Plan section, JIRA link, `✓` checkmarks
- **End with**: `Signed-off-by: <Name> <Email>`

### Draft file convention

`ai-context/sessions/YYYY-MM-DD-XX-<topic>-PR-MERGE-commit.md`

Uses the same `XX` number as the corresponding `-PR.md` file.

## Tone

Write for the reviewer. Be concise. The summary paragraph is the most important part — it should make the reviewer understand the PR before looking at the diff.
