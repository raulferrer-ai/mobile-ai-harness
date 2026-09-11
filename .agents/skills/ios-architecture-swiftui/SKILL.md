---
name: ios-architecture-swiftui
description: Apply the iOS contract: layering, small SwiftUI views, observable view models, structured concurrency and the repository boundary. Use when working inside ios/.
---

# iOS Architecture

## Summary
Modular SwiftUI features with `@MainActor` view models and a pure domain, as declared in `ios/AGENTS.md`.

## When to use
- Creating or editing Swift files, views, view models, repositories or composition-root wiring in `ios/`.

## Steps
1. Read `ios/AGENTS.md`; open `.agents/references/ios-stack.md` for patterns and samples.
2. Put models and repository protocols in `Domain/`; implementations and OS adapters in `Data/`.
3. Keep views declarative and small; move logic into the view model, rules into domain.
4. Make isolation explicit: `@MainActor` for UI state, `Sendable`/`nonisolated` for pure domain types.
5. Map storage entities to domain types at the repository boundary; inject dependencies from `App/`.
6. Surface errors as calm user-facing state; never swallow them.

## Gotchas
- No persistence, scheduling or networking inside `View` bodies; no `@Query` in feature views.
- Do not silence Swift 6 diagnostics with `@unchecked Sendable`; decide the isolation properly.
- Do not swap a default technology here: use `docs/customizing.md`.
