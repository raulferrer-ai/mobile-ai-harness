# android/AGENTS.md - Android platform contract

> **Defaults, not dogma.** Everything under "Stack" is the template default. To change it, follow
> `docs/customizing.md` (ADR + update this file, `docs/stack.md`, `.agents/references/android-stack.md`).
> Patterns and code samples: `.agents/references/android-stack.md`. Versions baseline: `docs/stack.md`.

## Stack (defaults)
| Concern | Default | Typical alternative |
| --- | --- | --- |
| Language / build | Kotlin 2.4.x, Gradle Kotlin DSL, version catalog (`gradle/libs.versions.toml`) | - |
| UI | Jetpack Compose + Material 3 adapted to the design system | - |
| Architecture | MVVM with unidirectional data flow (UDF), immutable `UiState` per screen | MVI |
| State holder | `ViewModel` + `StateFlow`; `collectAsStateWithLifecycle()` in UI | - |
| Navigation | Navigation Compose, type-safe routes | Navigation 3 |
| Persistence | Room 3 (`androidx.room3`, KSP) behind a repository interface; DataStore for small settings | Room 2.x, SQLDelight |
| Concurrency | Coroutines + Flow; inject dispatchers; no `GlobalScope` | - |
| Dependency injection | Manual `AppContainer` + `ViewModel` factories (constructor injection) | Hilt, Koin |
| Networking (if any) | Retrofit/OkHttp or Ktor, behind an interface | - |
| Unit tests | JUnit 4, `kotlinx-coroutines-test`, Turbine; fakes over mocks | JUnit 5, MockK |
| UI tests | Compose test rule (`ui-test-junit4`) with test tags | - |
| Static analysis | Android Lint (`make lint-android`); detekt/ktlint optional | - |
| SDK levels | `minSdk` 26, `compileSdk`/`targetSdk` at the latest the toolchain supports | any |

## Project layout
`app/src/main/java/<package>/`: `features/<feature>/` (Screen, UiState, ViewModel) - `domain/` (model,
repository interfaces, usecase, scheduling) - `data/` (local/Room, repository, notifications, photos) -
`designsystem/` (tokens, theme, components) - `AppContainer.kt`, `<App>Application.kt`, `MainActivity.kt`.
Tests: `app/src/test/` (JVM) and `app/src/androidTest/` (instrumented).

## Rules
- **Layering:** features -> domain <- data. `domain/` has no Android SDK or Room imports.
  Never expose Room entities outside `data/`; map at the repository boundary.
- **UDF:** the UI renders `UiState` and sends events up; only the ViewModel mutates state.
  Expose `StateFlow<UiState>` (read-only) and plain functions for events.
- **Composables are declarative.** No business logic, database or scheduling calls inside them. Hoist state;
  keep composables small and previewable; use `remember`/`derivedStateOf` correctly.
- **Coroutines:** `viewModelScope` for ViewModel work; use `stateIn(WhileSubscribed(5_000))`; always
  rethrow `CancellationException`; no blocking I/O on the main thread.
- **Errors:** repositories throw typed errors; the ViewModel maps them to calm user-facing state. Never swallow silently.
- **Design system:** use tokens/components from `designsystem/`; no hardcoded colors, text sizes or dp literals in features.
- **Accessibility and i18n:** `contentDescription`/semantics on interactive elements, 48dp touch targets, support font
  scaling; user-facing strings in `res/values/strings.xml`, never inline.
- **Permissions:** request in context (notifications need runtime permission on API 33+); handle denial gracefully.
- **Build hygiene:** versions only in the version catalog; Kotlin 2.4 removed `kotlinOptions {}`, use
  `kotlin { compilerOptions { } }`; check the AGP release notes before copying older Gradle snippets.
- **Time and IDs:** inject a clock/ID source where logic depends on them.

## Testing
- ViewModels and domain: JVM unit tests with fakes, `runTest`, Turbine for Flow emissions.
- Repositories/DAOs: instrumented tests with an in-memory database.
- UI flows: Compose tests with `testTag`s; no `Thread.sleep`.
- Sensor: `make sensor-android` (`harness.env` -> `ANDROID_TEST_TASK`, needs JDK per `MIN_JDK`).

## Platform Definition of Done
Compiles cleanly - spec respected - tests pass (`make sensor-android`) - design system and accessibility respected -
main flow runs without crashes - differences from iOS logged in `docs/parity-matrix.md`.

## Skills to load
`android-architecture-compose`, `design-system-parity`, `mobile-data-permissions`, `mobile-testing-harness`,
`mobile-accessibility-localization`, `mobile-security-privacy` (only when relevant).
