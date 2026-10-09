# Stack defaults

This template ships with a **default stack for each platform** so a new project is ready to use on day one.
**Every default can be changed.** How: `docs/customizing.md`. Why these defaults: `docs/decisions/0001-stack-defaults.md`.

How to read the tables: *Default* is what agents will use unless told otherwise; *Alternatives* are common,
supported-by-the-process swaps (they still need an ADR and the update checklist).

## iOS
| Concern | Default | Alternatives |
| --- | --- | --- |
| Language | Swift 6 mode, strict concurrency | - |
| UI | SwiftUI | UIKit via representables |
| Presentation state | `@Observable` + `@MainActor` view models | - |
| Navigation | `NavigationStack`, typed paths | Coordinators |
| Persistence | SwiftData behind repository protocol | Core Data, GRDB |
| Async | async/await, actors | - |
| DI | Constructor injection, composition root in `App/` | Container libraries |
| Tests | Swift Testing (unit), XCUITest (UI) | XCTest for unit |
| Localization | String Catalogs | - |
| Deployment target | iOS 26.0 | any |

## Android
| Concern | Default | Alternatives |
| --- | --- | --- |
| Language / build | Kotlin 2.4.x, Gradle KTS, version catalog | - |
| UI | Jetpack Compose + Material 3 (themed to design system) | - |
| Architecture | MVVM + UDF, immutable `UiState` | MVI |
| Navigation | Navigation Compose (type-safe routes) | Navigation 3 |
| Persistence | Room 3 (`androidx.room3`) + DataStore | Room 2.x, SQLDelight |
| Async | Coroutines + Flow | - |
| DI | Manual `AppContainer` + ViewModel factories | Hilt, Koin |
| Tests | JUnit 4, coroutines-test, Turbine, Compose test | JUnit 5, MockK |
| Static analysis | Android Lint | detekt, ktlint |
| SDK levels | `minSdk` 26; `compileSdk`/`targetSdk` latest supported by toolchain | any |

## Shared
| Concern | Default |
| --- | --- |
| Behaviour specs | Gherkin in `features/` |
| Cross-platform code sharing | None (native UI and logic per platform). KMP/Flutter are out of scope by design |
| Backend | None assumed (local-first). Add behind repository contracts when needed |
| CI | GitHub Actions: harness job, Android sensor, iOS build |
| Product language(s) | Declared in `docs/product.md` |

## Version baseline
**Verified 2026-09-18** against official release pages. Versions drift quickly: re-verify at project start and
update this table when you bump (skill: `harness-maintainer`).

| Component | Baseline | Notes |
| --- | --- | --- |
| Xcode / Swift | Xcode 27 with Swift 6.4 (iOS 27 released 2026-09-14; Xcode 27 RC available since 2026-09-10); Xcode 26.6 was the latest 26.x seen | Apple requires the iOS 27 SDK for App Store uploads from April 2027 |
| iOS deployment target | 26.0 (current minus one) | Your choice per product |
| Kotlin | 2.4.x stable (2.5.0 is in RC) | `kotlinOptions {}` was removed in 2.4 |
| Android Gradle Plugin | 9.4.x (max API level 37) | Compose 1.12+ requires `compileSdk` 37 and AGP 9; AGP 9 changes Kotlin integration, read its release notes |
| Gradle | 9.x as required by the AGP release notes | Pinned by `gradle/wrapper/gradle-wrapper.properties` |
| JDK | 17+ (`MIN_JDK` in `harness.env`) | |
| Jetpack Compose | BOM 2026.09.00 per Android docs (Compose 1.12.x stable, 1.13 RC) | Check the BOM mapping page for newer BOMs |
| Room | 3.0.x (`androidx.room3`, KSP only, suspend/Flow DAOs) | Room 2.x is in maintenance mode |

Never copy versions from older tutorials or from memory: check the sources above or the project's own catalog.
