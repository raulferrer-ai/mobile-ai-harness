# ios/AGENTS.md - iOS platform contract

> **Defaults, not dogma.** Everything under "Stack" is the template default. To change it, follow
> `docs/customizing.md` (ADR + update this file, `docs/stack.md`, `.agents/references/ios-stack.md`).
> Patterns and code samples: `.agents/references/ios-stack.md`. Versions baseline: `docs/stack.md`.

## Stack (defaults)
| Concern | Default | Typical alternative |
| --- | --- | --- |
| Language | Swift 6 language mode, strict concurrency | - |
| UI | SwiftUI, system components first (Liquid Glass on iOS 26+) | UIKit only via representables |
| Presentation state | `@Observable` view models, `@MainActor` | - |
| Navigation | `NavigationStack` with typed paths, owned by the feature/root | Coordinators if flows get complex |
| Persistence | SwiftData behind a repository protocol | Core Data, GRDB |
| Concurrency | async/await, structured concurrency, actors for shared mutable state | - |
| Dependency injection | Constructor injection, composition root in `App/` | Factory-style containers |
| Networking (if any) | `URLSession` + `Codable`, behind a protocol | - |
| Packages | Swift Package Manager only; justify every dependency | - |
| Unit tests | Swift Testing (`@Test`, `#expect`); XCTest still valid | XCTest |
| UI tests | XCTest / XCUITest with seeded launch arguments | - |
| Localization | String Catalogs (`.xcstrings`) | - |
| Lint / format | `swift format` (toolchain); optional SwiftLint via `IOS_LINT_CMD` | - |
| Deployment target | iOS 26.0 (current minus one). Edit in the Xcode project | any |

## Project layout
`App/` (entry point, composition root, root navigation) - `Features/<Feature>/` (View + ViewModel) -
`Domain/` (models, repository protocols, pure services) - `Data/` (SwiftData, notifications, media, network) -
`DesignSystem/` (tokens, components) - `Resources/` - Tests in `<App>Tests/`, UI tests in `<App>UITests/`.

## Rules
- **Layering:** Features -> Domain <- Data. `Domain` imports only Foundation. Never expose `@Model`
  entities outside `Data/`; map to domain types at the repository boundary.
- **Views are declarative.** No persistence, scheduling, networking or business rules inside a `View`.
  Do not use `@Query` in feature views; read through the repository/view model.
- **Small views:** extract subviews when a `body` exceeds ~60 lines or mixes concerns.
- **Concurrency:** UI and view models are `@MainActor`. Mark pure domain types `nonisolated`/`Sendable`.
  No `Task.detached` without a written reason; prefer `.task {}` in views; respect cancellation.
- **Errors:** throw typed errors from repositories; map to calm, user-facing messages in the view model.
  Never swallow errors silently; never force-unwrap (`!`) in production code.
- **State ownership:** `@State` owns a view model created by the view; pass `@Bindable` or plain
  values down; avoid global singletons.
- **Design system:** use tokens and components from `DesignSystem/`; no ad-hoc colors, fonts or spacing literals.
- **Accessibility and i18n:** every interactive element has an accessibility label; support Dynamic Type;
  user-facing strings live in the String Catalog, never inline.
- **Permissions:** request in context, handle denied/restricted states with a usable fallback.
- **Time and IDs:** inject a clock/calendar and ID generator where logic depends on them (testability).

## Testing
- Domain and view models: unit tests with fakes (not heavy mocks), no real storage or network.
- Repositories: in-memory store (`isStoredInMemoryOnly`) tests.
- UI flows: XCUITest with seeded data via launch arguments (`#if DEBUG` seeding), no `sleep`; use
  `waitForExistence`. Give controls `accessibilityIdentifier`s.
- Sensor: `make sensor-ios`. Build-only mode is degraded and is recorded as such in the gate.

## Platform Definition of Done
Compiles with no relevant warnings - spec respected - tests pass (`make sensor-ios`) - design system and
accessibility respected - main flow runs without crashes - differences from Android logged in `docs/parity-matrix.md`.

## Skills to load
`ios-architecture-swiftui`, `design-system-parity`, `mobile-data-permissions`, `mobile-testing-harness`,
`mobile-accessibility-localization`, `mobile-security-privacy` (only when relevant).
