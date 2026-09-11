---
name: workflow-planner
description: Break a feature spec into small verifiable steps per platform and check parity before coding. Use when starting a feature or planning implementation order.
---

# Workflow Planner

## Summary
Turn one `.feature` spec and its board entry into a short, ordered, verifiable plan for each platform.

## When to use
- Starting a feature (`planned` -> `in_progress`).
- Re-planning after a spec change or a blocked sensor.

## Steps
1. Read `progress/current.md`, `make status`, the spec, `docs/parity-matrix.md` and both platform contracts.
2. Confirm the spec is complete (happy path, validation, empty/error/denied). If not, use `feature-spec-writer` first.
3. List per platform: domain models/rules, persistence, OS capabilities (permissions, notifications, media), design system
   components, state holder + screens, tests.
4. Split into increments that each end with a runnable sensor (core layers first, UI last).
5. Note expected platform differences up front (parity matrix).
6. Write the plan into `progress/current.md` under "Plan for the active feature" before touching app code.

## Gotchas
- Do not plan both platforms in one implementation session; plan both, implement one.
- Do not invent requirements; unknowns go back to the human as spec questions.
- Do not force a shared abstraction across platforms when native idioms are clearer.
