---
name: verify
description: Use before claiming any task is complete. Runs fresh verification and confirms output before reporting done.
---

# Verification Before Completion — Superpowers Skill

Sourced from: github.com/obra/superpowers

## Absolute Rule

**NEVER claim work is complete without running fresh verification commands and confirming the output.**

"Claiming work is complete without verification is dishonesty, not efficiency."

## Before any completion claim

1. **Identify** the command that proves your claim
2. **Execute** it completely — no skipping, no partial runs
3. **Read** the full output and exit codes
4. **Verify** the output actually confirms your claim
5. **Only then** make the claim, with evidence

## What does NOT count as verification

- Previous test runs from earlier in the session
- Code changes alone (compiling is not the same as working)
- Linter passes
- Subagent success reports
- "I believe this should work"

## Red flags — stop if you're about to

- Use conditional language: "should," "probably," "seems to"
- Express satisfaction before running any check
- Commit or push without fresh verification
- Trust a self-report without independent confirmation

## Applies to

Tests, builds, regression checks, requirement fulfilment, and any message implying the task is done.

No exceptions for confidence level, fatigue, or "this is obviously right."
