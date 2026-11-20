# Bootstrap: from template to a working project

Follow in order. Each step ends with something you can check.

## 1. Check the machine
`make doctor` reports what is missing (git, Python 3.9+, JDK per `MIN_JDK`, Xcode, simulators).
Fix blockers for the platforms you build on this machine. iOS needs macOS and Xcode.

## 2. Configure the harness
- `harness.env`: `PROJECT_NAME`, `PLATFORMS`, and after step 3 the iOS/Android values.
- `feature_list.json`: set `"project"` to the same name.
- Fill `docs/product.md` and `docs/design-system.md` (colors, type, spacing).
- Review the stack defaults in `docs/stack.md`; change deliberately with `docs/customizing.md`.
Check: `make validate-harness`.

## 3. Create the native projects
These steps use Xcode and Android Studio because project generators and templates change between versions.
Do them once, by hand, then commit.

**iOS** (`ios/`)
1. Xcode > New Project > iOS App; interface SwiftUI, language Swift; name it `App` (or edit `harness.env`), save under `ios/App`.
2. Include a unit-test target and a UI-test target; choose Swift Testing for unit tests if offered.
3. Set the deployment target (default in `docs/stack.md`), Swift language version 6, default actor isolation MainActor,
   approachable concurrency on, String Catalog on (see `.agents/references/ios-stack.md`).
4. Make the scheme shared (Manage Schemes > Shared).
5. Create the layer folders from `ios/AGENTS.md` (`App/`, `Features/`, `Domain/`, `Data/`, `DesignSystem/`).
6. Set `IOS_PROJECT`, `IOS_SCHEME` and a valid `IOS_DESTINATION` (`make simulators`) in `harness.env`.
Check: `make sensor-ios` builds and runs the default tests.

**Android** (`android/`)
1. Android Studio > New Project > Empty Activity (Compose), save under `android/`; set the package; `minSdk` per `docs/stack.md`.
2. Use the Gradle Kotlin DSL and a version catalog (`gradle/libs.versions.toml`); take versions from `docs/stack.md`, verified
   against the AGP release notes of the version you pick. Do not copy older plugin snippets: AGP 9 changed Kotlin integration.
3. Add test dependencies: JUnit 4, `kotlinx-coroutines-test`, Turbine, Compose UI test; add `lifecycle-runtime-compose`.
4. Create the layer packages from `android/AGENTS.md` (`features/`, `domain/`, `data/`, `designsystem/`).
5. Commit the Gradle wrapper (`gradlew`, `gradle/wrapper/*`). Set `ANDROID_TEST_TASK` if your module is not `:app`.
Check: `make sensor-android` runs `testDebugUnitTest`.

## 4. Prove the loop with the sample feature
`templates/sample-feature/README.md` explains how to copy the reference slice, register its spec and run
`make sensor-ios`, `make sensor-android`, `make gate`. This is the first real verification of the template on your
toolchain. If you hit API drift, fix it and record it in `progress/flywheel-log.md`.

## 5. Make CI real
Push to GitHub: the `harness`, `security`, `android` and `ios` jobs in `.github/workflows/ci.yml` run. Choose the simulator
available on the macOS runner (see the "Show Xcode version and simulators" step), then consider switching the iOS job from
build-only to tests (comment in the workflow).

## 6. Organization adoption checklist (human)
**Repository**
- [ ] Branch protection on the default branch: PRs required, required status checks (`harness`, `security`, `android`, `ios`),
      "Require review from Code Owners", no force pushes
- [ ] `.github/CODEOWNERS` placeholders replaced with real teams (they must have write access)
- [ ] Secret scanning and push protection enabled; Dependabot alerts enabled; uncomment ecosystems in `.github/dependabot.yml`
- [ ] Workflow permissions default to read-only; third-party actions pinned per policy

**Security and compliance**
- [ ] `SECURITY.md` contact set; `docs/security.md` threat model started
- [ ] `docs/privacy-compliance.md` data inventory started; privacy owner named
- [ ] License chosen with legal and added as `LICENSE`; dependency license policy agreed

**AI governance**
- [ ] `docs/ai-governance.md`: approved tools/tenants, data classes, retention and disclosure rules filled in
- [ ] Tool-level managed/organization settings applied where the vendor supports them
- [ ] Reviewers briefed on what to look for in AI-authored changes

**Delivery (outside this template's v2.1 scope)**
- [ ] Apple Developer and Play Console accounts, signing and release process, environments, crash reporting and analytics
      decided and recorded as ADRs

## 7. Shortcut: reuse a verified project
If you already have a compiling app, you can skip step 3 and migrate it instead: copy its `ios/` and `android/` into this
repo, point `harness.env` at it and run `make sensors`. A real, building project beats a hand-created one as the
starting point.
