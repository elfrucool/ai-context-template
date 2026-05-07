# Brief Creation Guidelines

Briefs are high-level, orientation-first summaries of major features and architectural changes.
They serve as entry points before diving into implementation-level session notes.

## Philosophy

- **Orientation-first**: Designed to be read first by new team members or agents
- **Link-driven**: References session files, architecture docs, and code locations rather than duplicating details
- **Chronological**: Captures feature evolution across multiple sessions
- **Stable**: Updated when significant changes occur, not per-session

## When to Create a Brief

| Situation                            | Create Brief? | Scope                   |
| ------------------------------------ | ------------- | ----------------------- |
| Single session, small fix            | No            | —                       |
| Feature spanning 3+ session files    | Yes           | Multi-session work      |
| Significant architectural change     | Yes           | System-wide impact      |
| Before handing off work              | Yes           | Any substantial feature |
| Major decision affecting future work | Yes           | Design impact           |

**Note**: Small (1-2 session) features don't need briefs; large features do.

## Directory Structure

```
ai-context/
├── briefs/
│   ├── 00-about-briefs.md              (this index)
│   └── 2026-02-15-auth-system.md       (brief example)
├── sessions/
│   ├── 2026-02-15-00-auth-planning.md
│   ├── 2026-02-15-00-auth-planning-plan.md
│   ├── 2026-02-16-00-auth-implementation.md
│   ├── 2026-02-17-00-auth-implementation.md
│   └── 2026-02-18-00-auth-tests.md
└── architecture/
    ├── 00-architecture-index.md
    └── 01-domain-explanation.md
```

## Brief File Naming

```
YYYY-MM-DD-<feature-name>.md
```

- `YYYY-MM-DD`: Date when brief was written (not when work started)
- `<feature-name>`: Kebab-case feature or component name
- Examples: `2026-02-15-auth-system.md`, `2026-03-01-api-v2-migration.md`

## Standard Brief Template

```markdown
# <Feature Name> Brief

**Period**: YYYY-MM-DD to YYYY-MM-DD (or TBD if ongoing)
**Status**: Completed / In Progress / Paused
**JIRA**: ABC-123, ABC-456 (optional)
**Branch**: feature/auth-system (optional)

## What is this?

1-2 sentences: What does this feature do? Who uses it?

## Key Decisions

- **Decision 1**: What was decided and why?
- **Decision 2**: Trade-offs and alternatives considered

## Components

(Optional, include if helpful)

- **Component A**: What it does
- **Component B**: What it does
- See also: `architecture/01-domain-explanation.md`

## Session Files

Key session files in chronological order:

1. [Planning](../sessions/2026-02-15-00-auth-planning-plan.md) - Initial design and approach
2. [Implementation Part 1](../sessions/2026-02-16-00-auth-implementation.md) - Core logic
3. [Implementation Part 2](../sessions/2026-02-17-00-auth-implementation.md) - Edge cases and hardening
4. [Testing](../sessions/2026-02-18-00-auth-tests.md) - Test coverage

See [sessions/](../sessions/) for the complete history.

## Related Documentation

- Architecture: [Domain Explanation](../architecture/01-domain-explanation.md)
- Testing: [guidelines/JAVA_UNIT_TESTING_GUIDELINES.md](../guidelines/JAVA_UNIT_TESTING_GUIDELINES.md) (if applicable)
- Code: `src/main/java/com/example/auth/` (or relevant directory)

## Timeline

- **Feb 15**: Planning session, API design finalized
- **Feb 16-17**: Implementation across multiple sessions
- **Feb 18**: Test coverage and verification
- **Status**: Ready for production

## Follow-up / Next Steps

(If applicable)

- [ ] Performance testing in staging
- [ ] Documentation update
```

## Quality Checklist

Before creating a brief, verify:

- [ ] **Brief answers "what is this?"** in 2 sentences without reading session files
- [ ] **Key decisions are documented** with reasoning
- [ ] **Links to session files are accurate** and chronologically ordered
- [ ] **Related architecture docs are referenced** (if applicable)
- [ ] **Status is clear** (Completed / In Progress / Paused)
- [ ] **Timeline is accurate** (dates and phase descriptions match session files)
- [ ] **Next steps are identified** if work is incomplete

## How to Update `00-about-briefs.md`

After creating a brief, add an entry to the index:

```markdown
| [Auth System](2026-02-15-auth-system.md) | Feb 15 - Feb 18 | User authentication, JWT tokens, session management |
```

Entries should be in reverse chronological order (newest first).

## Brief vs. Session File

| Aspect             | Brief                                 | Session                      |
| ------------------ | ------------------------------------- | ---------------------------- |
| **Purpose**        | Orientation for new readers           | Daily progress record        |
| **Audience**       | New team members, architects          | Current session participants |
| **Scope**          | Multi-session feature or architecture | Single session's work        |
| **Links**          | Links to sessions                     | Inline details               |
| **Frequency**      | Written once per major feature        | Written daily during work    |
| **Update Pattern** | Stable; updated with major changes    | Not updated after creation   |

## Brief vs. Architecture Doc

| Aspect        | Brief                         | Architecture                     |
| ------------- | ----------------------------- | -------------------------------- |
| **Purpose**   | Feature overview and history  | Reference design                 |
| **Content**   | What was built, why, timeline | How it works, design patterns    |
| **Links**     | Links to code and sessions    | Links to implementations         |
| **Frequency** | Rare (per major feature)      | Infrequent (per system redesign) |

## Examples

### Small Feature (No Brief Needed)

```
Session file: 2026-02-20-00-fix-login-button.md

Status: Completed
Changes: Fixed button alignment in LoginComponent
Tests: 2 new tests added, all passing
No brief needed — small, self-contained fix.
```

### Large Feature (Brief Recommended)

```
Brief: 2026-02-15-auth-system.md
Sessions:
  - 2026-02-15-00-auth-planning-plan.md
  - 2026-02-15-00-auth-planning.md
  - 2026-02-16-00-auth-implementation.md
  - 2026-02-17-00-auth-implementation.md
  - 2026-02-18-00-auth-tests.md

Creates brief because:
- Spans 5 session files
- Significant architectural impact
- Touches authentication across multiple components
```

## Tips

- **Reference, don't duplicate**: Briefs should reference session files, not rewrite them
- **Use links liberally**: Make it easy to jump to relevant docs
- **Chronological sessions**: List session files in the order they were created
- **Decision focus**: Explain the "why", not just the "what"
- **Update sparingly**: A brief should be stable once written; minor improvements don't need updates
- **Timeline section**: Helps future readers understand the work progression
