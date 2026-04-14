---
name: debug
description: Use when debugging any technical problem. Enforces root-cause investigation before any fix attempt.
---

# Systematic Debugging — Superpowers Skill

Sourced from: github.com/obra/superpowers

## Iron Law

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Applying a patch before understanding the cause just hides the bug.

## Four-Phase Methodology

### Phase 1 — Root Cause Investigation
- Read error messages completely and carefully
- Reproduce the issue consistently before touching anything
- Review recent changes — what changed when this broke?
- Trace data flow through system boundaries

### Phase 2 — Pattern Analysis
- Find working examples to compare against
- Identify what's different between working and broken states
- Map all dependencies

### Phase 3 — Hypothesis & Testing
- Form one specific hypothesis
- Test with a single minimal change
- Validate before concluding

### Phase 4 — Implementation
- Write a failing test that demonstrates the bug first
- Apply the single fix that addresses the root cause
- Verify the fix actually works

## Red flags — stop immediately if you see yourself

- Proposing a solution before understanding the problem
- Attempting multiple simultaneous fixes
- Continuing after three failed attempts without questioning fundamentals
- Using "it should work" language before verification

## After 3 failed fixes

Question architecture, not implementation. The problem may be deeper than the symptom.
