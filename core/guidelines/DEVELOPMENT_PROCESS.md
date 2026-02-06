# Development Process Guidelines

## Overview

This document defines the end-to-end workflow for AI-assisted development sessions, from planning through implementation to session documentation.

### Philosophy

- **Collaboration-first**: Ask questions, validate assumptions, get approval before significant changes
- **Incremental**: Build and verify in small steps, one test at a time
- **Well-documented**: Capture decisions and progress for future reference

### Related Guidelines

- See language-specific guidelines in `guidelines/` if available

---

## 1. Planning Phase

### Phase 1: Context Gathering

Before starting any task, understand the current state:

1. **Read recent session files** (last 3-7 days in `sessions/`)
   - Understand what was recently worked on
   - Identify ongoing work or decisions made

2. **Read domain guidelines** (`guidelines/domain-explanation.md`)
   - Refresh understanding of core concepts

3. **Explore relevant codebase areas**
   - Read files that will be affected
   - Understand existing patterns and conventions

### Phase 2: Requirements Clarification

Before planning, ensure requirements are clear:

- **Ask clarifying questions** when intent is ambiguous
- **Identify assumptions** and validate them explicitly
- **Don't proceed** with unclear requirements - ask first

**Questions to consider:**
- What is the expected behavior?
- What inputs/outputs are involved?
- Are there edge cases to handle?
- How does this fit with existing code?

### Phase 3: Scope Definition

Define clear boundaries:

| Aspect | Include |
|--------|---------|
| **In scope** | What this task will accomplish |
| **Out of scope** | What this task will NOT do |
| **Assumptions** | What we're taking as given |
| **Complexity** | Simple / Medium / Complex |

### Phase 4: Plan Creation

For **complex tasks**, create a plan file before implementation.

**File location**: `ai-context/sessions/YYYY-MM-DD-XX-<topic>-plan.md`

**Plan structure**:
```markdown
# <Task Title> - Plan

**Date**: YYYY-MM-DD
**Status**: Draft / Approved / In Progress

## Goal
What we're trying to achieve

## Findings
What we learned during exploration

## Phases
1. Phase 1: ...
2. Phase 2: ...
3. Phase 3: ...

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Open Questions (if any)
- Question 1
- Question 2
```

**Important**: Include a reference to this file (`ai-context/guidelines/DEVELOPMENT_PROCESS.md`) at the top of the plan, so AI agents follow the TDD process correctly.

**Get user approval** before starting implementation.

### Checkpoint Guidance

**Stop and ask when:**
- Requirements are ambiguous
- Multiple valid approaches exist
- Changes would affect public APIs
- Accessibility changes are needed (making methods less private)
- You're unsure about design decisions

**Proceed when:**
- Requirements are clear
- Following established patterns
- Changes are localized and low-risk
- User has already approved the approach

---

## 2. Implementation Phase

Implementation follows guidelines defined in language-specific files in `guidelines/` if available.

### Key Principles

1. **Incremental development**
   - Write one test at a time
   - Get it passing before writing the next
   - Build complexity gradually

2. **Test-first workflow**
   - Write the test first (AI agent)
   - Create minimal stubs/scaffolding to make the test compile (empty methods, placeholder classes)
   - User implements the production code to make the test pass
   - AI agent assists only if the user cannot make it pass

3. **User runs tests**
   - By default, let the user execute tests
   - Only run tests yourself when explicitly asked
   - TODO: add your test/build commands here

4. **Ask when uncertain**
   - Accessibility decisions (making private methods accessible)
   - Design choices with multiple valid options
   - Anything that feels like a judgment call

5. **Keep changes focused**
   - Only make changes directly requested
   - Avoid opportunistic refactoring
   - Don't add features beyond scope

---

## 3. Session Summaries

### When to Create

Create a session summary when:
- Significant work completed (refactoring, feature, architecture)
- Major decisions made that affect future work
- Work paused mid-task and context needs preservation

**Always ask the user** before creating a session summary.

Partial summaries are acceptable if the user needs to leave mid-session.

### File Naming

`ai-context/sessions/YYYY-MM-DD-XX-<topic>.md`

- `YYYY-MM-DD` - Date
- `XX` - Sequential number (00, 01, 02...) for ordering within the day
- `<topic>` - Brief descriptive topic

If a plan file exists, use the **same XX number** for the implementation summary.

**Examples:**
- `2026-01-28-00-compiler-refactoring-plan.md` (plan)
- `2026-01-28-00-compiler-refactoring.md` (implementation summary)
- `2026-01-28-01-test-data-cleanup.md` (separate task)

### Template

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

---

## 4. Quick Reference

### When to Create a Plan File

| Situation | Create Plan? |
|-----------|--------------|
| Simple bug fix, clear requirements | No |
| Multi-file refactoring | Yes |
| New feature with design choices | Yes |
| Following established pattern exactly | No |
| Architectural changes | Yes |
| User explicitly requests a plan | Yes |

### When to Ask vs. Proceed

| Situation | Action |
|-----------|--------|
| Multiple valid implementation approaches | Ask |
| Unclear requirements | Ask |
| Need to change method visibility | Ask |
| Following exact pattern from guidelines | Proceed |
| Simple, localized change | Proceed |
| User already approved approach | Proceed |

### When to Suggest Session Summary

| Situation | Suggest Summary? |
|-----------|------------------|
| Completed significant feature | Yes |
| Made important architectural decisions | Yes |
| Multiple files changed | Yes |
| Quick one-file fix | No |
| Work interrupted mid-task | Yes (partial) |
| Research/exploration only | No |

---

## Summary Checklist

**Before starting:**
- [ ] Read recent session files for context
- [ ] Understand the codebase area being modified
- [ ] Clarify any ambiguous requirements
- [ ] Define scope (in/out) and assumptions
- [ ] Create plan file if task is complex
- [ ] Get user approval for approach

**During implementation:**
- [ ] Work incrementally (one test at a time)
- [ ] Let user run tests unless asked otherwise
- [ ] Ask before making accessibility changes
- [ ] Stay within defined scope

**After completing:**
- [ ] Ask user if they want a session summary
- [ ] Document key decisions and reasoning
- [ ] Note any follow-up tasks identified
