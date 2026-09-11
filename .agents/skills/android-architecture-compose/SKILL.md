---
name: android-architecture-compose
description: Apply the Android contract: layering, UDF with immutable UiState, small composables, coroutines and the repository boundary. Use when working inside android/.
---

# Android Architecture

## Summary
MVVM with unidirectional data flow and Compose, as declared in `android/AGENTS.md`.

## When to use
- Creating or editing Kotlin, Compose screens, ViewModels, repositories or `AppContainer` wiring in `android/`.

## Steps
1. Read `android/AGENTS.md`; open `.agents/references/android-stack.md` for patterns and samples.
2. Keep `domain/` free of Android SDK and storage imports; implementations and OS adapters live in `data/`.
3. Expose immutable `UiState` as `StateFlow`; events are plain ViewModel functions.
4. Split composables into stateless, previewable pieces with hoisted state.
5. Use structured concurrency: `viewModelScope`, injected dispatchers, rethrow `CancellationException`.
6. Map storage entities to domain models at the repository boundary; wire dependencies in `AppContainer`.

## Gotchas
- No business logic, database or scheduling calls inside composables.
- Prefer `WhileSubscribed(5_000)` over `Eagerly` and lifecycle-aware collection in UI.
- Older Gradle/AGP snippets may not match the current toolchain; check `docs/stack.md` and release notes.
- Do not swap a default technology here: use `docs/customizing.md`.
