---
name: mobile-testing-harness
description: Write fast, deterministic unit, repository and UI tests on both platforms and diagnose flaky tests. Use when adding or fixing tests or interpreting sensor failures.
---

# Mobile Testing

## Summary
Tests are the sensors of the loop; they must be fast, deterministic and meaningful.

## When to use
- Adding tests for domain rules, mappers, repositories, state holders or UI flows.
- A sensor is red or flaky.

## Steps
1. Start at the bottom: pure domain rules and mappers with plain unit tests.
2. Test state holders with hand-written fakes; assert state transitions, including error and empty.
3. Test repositories against in-memory storage; test migrations.
4. For UI flows, seed data through launch arguments/fixtures; identify controls with accessibility ids/test tags.
5. Inject time, IDs and dispatchers; never depend on wall-clock, network or real device services.
6. Run the sensor; if red, read the failure, fix the cause, repeat. Patterns: `.agents/references/<platform>-stack.md`.

## Gotchas
- `sleep`/`Thread.sleep` causes flakiness; wait on conditions.
- Never edit or delete a test just to get green; if the test is wrong, say why and ask the human.
- Build-only or skipped sensors are degraded evidence and are recorded as such.
