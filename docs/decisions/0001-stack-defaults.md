# 0001 - Stack defaults for the template

- **Status:** accepted (template default)
- **Date:** 2026-09-18
- **Deciders:** template maintainer

## Context
A ready-to-use harness needs a concrete stack, otherwise agents improvise per session. The defaults must be
modern, supported by the platform vendors, testable with fast feedback, and idiomatic enough that agents
produce good code without extra libraries.

## Decision
- **iOS:** Swift 6, SwiftUI, `@Observable`, SwiftData behind repositories, async/await, Swift Testing + XCUITest.
- **Android:** Kotlin, Jetpack Compose, MVVM/UDF with `StateFlow`, Room 3 behind repositories, coroutines/Flow,
  manual DI, JUnit + Turbine + Compose tests.
- **Shared:** native UI and logic per platform, Gherkin specs, local-first, constructor injection, no code sharing.
- Exact versions are a baseline in `docs/stack.md`, verified on the date above.

## Consequences
- Fewer first-party dependencies, faster agent onboarding, strong fakes-based testing.
- Projects that need another stack follow `docs/customizing.md`; this ADR is superseded by a project-specific ADR.

## Alternatives considered
- Cross-platform UI (Flutter, React Native, KMP UI): contradicts the "two native codebases, shared knowledge" thesis.
- Hilt/Koin by default: valuable at scale, unnecessary ceremony for a starting graph; remains a documented swap.
- Core Data / GRDB, SQLDelight: fully valid; kept as documented swaps.
