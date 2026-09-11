---
name: workflow-implementer
description: Implement a scoped feature increment on one platform following layer boundaries, small UI units and the build-sensor-fix loop. Use when writing or refactoring app code.
---

# Workflow Implementer

## Summary
Implement the smallest change the spec demands, with tests, then let the sensor judge.

## When to use
- Writing or refactoring production code in `ios/` or `android/`.

## Steps
1. Load the platform skill (`ios-architecture-swiftui` or `android-architecture-compose`) plus any relevant domain/UI skill.
2. Build from the core outward: domain -> data -> state holder -> UI. Do not leak UI or storage types into domain.
3. Keep screens small: extract sections, forms, sheets and rows into focused components.
4. Add or update tests with the code (see `mobile-testing-harness`).
5. Run the platform sensor (`make sensor-ios` / `make sensor-android`). Red: fix and repeat. Do not stop at red.
6. Update `progress/current.md` (state and handoff notes) when the increment is green.

## Gotchas
- Business rules, queries and scheduling never go inside views/composables.
- Keep the diff focused on the active feature; unrelated cleanups go in a separate change.
- Never weaken or delete an existing test to get green.
- A default you dislike is a human decision (`docs/customizing.md`), not a local workaround.
