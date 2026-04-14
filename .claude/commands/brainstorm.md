---
name: brainstorm
description: Use when starting any new feature, document, or project design. Enforces design-before-code gate — no implementation until you approve the design.
---

# Brainstorming & Design — Superpowers Skill

Sourced from: github.com/obra/superpowers

## Core Principle

**Hard gate: DO NOT write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it.**

This applies even for seemingly simple projects.

## Process

1. **Explore context** — review existing files and documentation first
2. **Clarifying questions** — one at a time, multiple-choice preferred
3. **Propose 2–3 approaches** with trade-offs and a recommendation
4. **Present design** in sections, seek approval after each section
5. **Write design doc** to `docs/specs/YYYY-MM-DD-<topic>-design.md`
6. **Self-review spec** — check for placeholders, contradictions, ambiguity
7. **Get user approval** of written spec
8. **Transition to writing-plans** only (no direct implementation)

## Design philosophy

- Break systems into small units with single purposes and clear interfaces
- No assumption that anything is "too simple" to document
- One question per message — don't barrage the user

## Hard constraints

- Never invoke implementation until design is approved in writing
- Never assume the user's goal without asking
- Two or more options presented for every significant trade-off
