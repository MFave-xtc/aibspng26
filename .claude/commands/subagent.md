---
name: subagent
description: Use when executing an implementation plan with mostly independent tasks in the current session. Dispatches a fresh subagent per task with two-stage review.
---

# Subagent-Driven Development — Superpowers Skill

Sourced from: github.com/obra/superpowers

## Core principle

**Fresh subagent per task + two-stage review (spec compliance then code quality) = high quality, fast iteration.**

Subagents receive exactly the context they need — nothing more, nothing less. They never inherit your session history.

## When to use

Decision tree:
- Have an implementation plan? ✓
- Tasks mostly independent? ✓
- Staying in this session? ✓

→ Use subagent-driven-development

If tasks are tightly coupled → use executing-plans instead

## The process

For each task:
1. Dispatch implementer subagent with complete task text + context
2. Answer any questions before implementation starts
3. Implementer implements, tests, commits, and self-reviews
4. Dispatch spec compliance reviewer
5. If issues found → implementer fixes → reviewer re-reviews
6. Dispatch code quality reviewer
7. If issues found → implementer fixes → reviewer re-reviews
8. Mark task complete → next task

After all tasks: dispatch final reviewer + use finish-branch workflow.

## Model selection

- Isolated, clear 1–2 file changes → cheapest model
- Multi-file integration → standard model
- Architecture, design, review → most capable model

## Hard rules

- Never start on main/master without explicit user consent
- Never skip spec compliance OR code quality review
- Never proceed with unfixed issues
- Never run implementer subagents in parallel (causes conflicts)
- Never let implementer self-review replace actual review
- Code quality review only starts after spec compliance is ✅
