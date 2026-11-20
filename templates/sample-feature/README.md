# Sample feature: "items" (reference slice)

A tiny, complete vertical slice for both platforms, used to **prove the harness works on your machine** before real
work starts: spec -> domain -> state holder -> UI -> tests -> sensor -> gate. It follows the default stack and rules in
`ios/AGENTS.md` and `android/AGENTS.md`.

> **Status: not compiled in the template's CI.** The template repository has no Xcode or Gradle project, so this code
> was written against the documented APIs but has not been built by the template itself. Treat the first
> `make sensors` run on your machine as its verification, and fix small API drift if your toolchain versions differ
> (that is exactly what the slice is for). Report drift as a flywheel entry.

## What is here
| Path | Purpose |
| --- | --- |
| `spec/01-sample-items.feature` | Behaviour contract (4 scenarios) |
| `ios/` | Domain model + repository protocol, `@Observable` view model, SwiftUI view, Swift Testing tests with a fake |
| `android/` | Domain model + repository interface, ViewModel with `StateFlow`, Compose screen, JVM tests with a fake and Turbine |

Persistence is intentionally an in-memory/fake repository: the slice proves the *loop*, not Room or SwiftData.
Replace the fake with your real repository when you build the first real feature.

## How to use
1. Create the native projects (`docs/bootstrap.md`).
2. Copy the files into your projects (adjust package/module names; keep the layer folders from the platform contracts):
   - iOS: `ios/Domain/*` -> `<App>/Domain/`, `ios/Features/Items/*` -> `<App>/Features/Items/`, `ios/Tests/*` -> `<App>Tests/`
   - Android: `android/domain/*` -> `app/src/main/java/<package>/domain/`, `android/features/items/*` ->
     `.../features/items/`, `android/test/*` -> `app/src/test/java/<package>/`
3. Android test dependencies: JUnit 4, `kotlinx-coroutines-test`, Turbine, `lifecycle-runtime-compose`, Material 3.
4. Register the spec and run the loop:
   ```bash
   cp templates/sample-feature/spec/01-sample-items.feature features/01-sample-items.feature
   python3 scripts/feature.py add sample-items "Sample items" --spec features/01-sample-items.feature
   python3 scripts/feature.py start sample-items
   make sensor-ios && make sensor-android && make gate
   ```
5. Complete the dual checklist, then a human closes it (`docs/dual-checklist.md`).
6. Delete the sample (or keep it as the first feature) before building the product.
