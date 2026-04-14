---
name: write-plan
description: Use after brainstorming is complete and design is approved. Creates a structured implementation plan document before any code is written.
---

# Write Plan — Superpowers Skill

Sourced from: github.com/obra/superpowers

## Purpose

Convert an approved design into a sequenced, actionable implementation plan that subagents can execute independently.

## Plan structure

```
# Implementation Plan: <feature name>
Date: YYYY-MM-DD
Spec: docs/specs/YYYY-MM-DD-<topic>-design.md

## Overview
[2–3 sentence summary of what is being built]

## Tasks

### Task 1: <name>
**Goal:** [What this task achieves]
**Files:** [Specific files to create or modify]
**Inputs:** [What context the implementer needs]
**Acceptance criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
**Dependencies:** [None | Task X]

### Task 2: ...
```

## Rules

- Each task must be independently executable (no implicit shared state)
- Acceptance criteria must be verifiable, not vague
- Provide full file paths, not relative references
- If tasks have dependencies, mark them explicitly — don't assume execution order
- Tasks should be small enough that a single subagent can complete them in one session

## Before writing the plan

- Confirm the design spec is approved and saved
- Identify all files that will change
- Sequence tasks to minimise merge conflicts
- Flag any tasks that require human decision (don't bury them in the middle)
