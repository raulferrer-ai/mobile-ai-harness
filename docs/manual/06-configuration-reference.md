# 06 - Configuration Reference

This chapter explains **each key of `harness.env`**, each IA tool permission rule and each CI job. Golden rule: **change the configuration, not the scripts**.

## 1. `harness.env`

Format: `CLAVE=valor`, without spaces around the `=`; values with spaces go in quotes. Read by the `Makefile` (with `include`), shell scripts (with `.`) and Python (`scripts/harness_config.py`).

### 1.1 Project

| Key | What it controls | Default value | Who reads it | When to change it |
| --- | --- | --- | --- | --- |
| `PROJECT_NAME` | Project name; used when importing old boards | `my-mobile-app` | `feature.py` | When starting |
| `PLATFORMS` | Product platforms, separated by spaces. A feature can only use platforms from this list | `ios android` | `feature.py` | To deliver only one platform or add another (see `docs/customizing.md`) |

### 1.2 iOS

| Key | What it controls | Default value | Who reads it | When to change it |
| --- | --- | --- | --- | --- |
| `IOS_DIR` | iOS folder. Mandatory for the validator, but currently no script uses it beyond validation; maintained for consistency with `ANDROID_DIR` | `ios` | `harness_config.py` | Only if you move the folder |
| `IOS_PROJECT` | Path to the Xcode project (`.xcodeproj`, which is a directory) | `ios/App/App.xcodeproj` | `sensor.sh`, `doctor.sh`, CI | After creating the Xcode project |
| `IOS_SCHEME` | Xcode scheme that compiles and tests. Must be **shared** | `App` | `sensor.sh` | After creating the project |
| `IOS_DESTINATION` | Sensor destination: specific simulator | `platform=iOS Simulator,name=iPhone 17 Pro` | `sensor.sh`, `doctor.sh` | If that simulator doesn't exist in your Xcode (`make simulators`) |
| `IOS_SENSOR_MODE` | `test` runs tests; `build` only compiles and registers as **degraded** | `test` | `sensor.sh` | Only if tests cannot run temporarily |
| `IOS_CI_DESTINATION` | Destination for CI compilation, without specific simulator | `generic/platform=iOS Simulator` | `sensor.sh` | If the CI needs another destination |
| `IOS_LINT_CMD` | Optional lint command that runs `make lint-ios`. Empty means no lint | `(empty)` | `sensor.sh`, `Makefile` | If you adopt a linter (e.g. `swift format lint --strict --recursive ios`) |
| `IOS_SRC_DIR` | iOS code folder that `make audit` audits (contains `Domain`, `Features`...) | `ios/App/App` | `audit-architecture.py` | To match the real project structure |
| `IOS_DOMAIN_ALLOWED_IMPORTS` | Modules that `Domain` can import, separated by spaces | `Foundation` | `audit-architecture.py` | If the domain needs another pure module, after deciding it |

### 1.3 Android

| Key | What it controls | Default value | Who reads it | When to change it |
| --- | --- | --- | --- | --- |
| `ANDROID_DIR` | Gradle project folder (where `gradlew` exists) | `android` | `sensor.sh`, `doctor.sh` | Only if you move the folder |
| `ANDROID_TEST_TASK` | Gradle task of the sensor | `:app:testDebugUnitTest` | `sensor.sh` | If your module is not `:app` or you use another variant |
| `ANDROID_LINT_TASK` | Gradle lint task (`make lint-android`). Empty means no lint | `:app:lintDebug` | `sensor.sh` | If you change module or variant |
| `MIN_JDK` | Minimum JDK version with which Gradle runs | `17` | `sensor.sh`, `doctor.sh`, CI | If your AGP version requires a higher JDK |
| `ANDROID_SRC_DIR` | iOS code folder that `make audit` audits | `android/app/src` | `audit-architecture.py` | If the module structure is different |

### 1.4 Contract Line Budgets (maximum lines)

Keep the files that are always loaded brief. If a contract grows, move the detail to `docs/` or `.agents/references/`; raising the limit is the last resort.

| Key | Applies to | Default | Who reads it |
| --- | --- | --- | --- |
| `BUDGET_ROOT_AGENTS` | `AGENTS.md` | 150 | `harness_config.py` |
| `BUDGET_PLATFORM_AGENTS` | `ios/AGENTS.md` and `android/AGENTS.md` | 130 | `harness_config.py` |
| `BUDGET_POINTER` | `CLAUDE.md` and `GEMINI.md` | 15 | `harness_config.py` |
| `BUDGET_SKILL` | Each `SKILL.md` | 80 | `harness_config.py` |

### 1.5 Documentation

| Key | What it controls | Default value | Who reads it |
| --- | --- | --- | --- |
| `DOCS_COMPLETENESS` | `warn`: what's missing in the manual generates warnings. `strict`: makes validation fail | `warn` | `validate-harness.py` |

The environment variable `DOCS_COMPLETENESS` (e.g. `DOCS_COMPLETENESS=strict make validate-harness`) has priority over the file.

**Recommendation:** `strict` only in the template repository; `warn` in client projects, so adding your own file doesn't block the work.

## 2. Claude Code Permissions and `.claude/settings.json`

**Allowed without confirmation:** read `.agents/`, `docs/`, `features/`, `progress/`, `android/AGENTS.md` and `ios/AGENTS.md`; run `make ...`, `python3 scripts/...` and `sh scripts/...`; and `git status`, `git diff` and `git log`.

**Denied:** read `.env*`, `*.jks`, `*.keystore`, `*.p12`, `*.pem` and `*.mobileprovision`; edit `feature_list.json`; run `python3 scripts/feature.py done` or `python3 scripts/feature.py remove`; and `rm -rf`, `git reset --hard`, `git push --force`, `git push -f` and `git clean -f`.

**Hooks (before using the tool):**

| Activated with | Executes | Effect |
| --- | --- | --- |
| Shell commands | `python3 .agents/hooks/block-destructive.py` | Blocks destructive commands and feature close |
| Edit or write files | `python3 .agents/hooks/guard-sensitive-paths.py` | Blocks secrets, signature, IDE state and the board |

## 3. OpenCode: `.opencode/opencode.json`

- `instructions`: loads `AGENTS.md`, `android/AGENTS.md` and `ios/AGENTS.md`.
- `permission.bash`: allows everything by default and **denies** `rm -rf`, `rm -fr`, `git reset --hard`, `git push --force`, `git push -f`, `git clean -f`, `git commit` with `--no-verify`, `python3 scripts/feature.py done`, `python3 scripts/feature.py remove` and `sudo`.

## 4. Codex: `.codex/config.toml`

- `approval_policy = "on-request"`: requests confirmation when needed.
- `sandbox_mode = "workspace-write"`: writes only within the repository.
- `project_doc_fallback_filenames = ["AGENTS.md"]`: reads `AGENTS.md`.
- Note: Gradle downloads and simulators may require relaxing the sandbox. If you do, register the decision in an ADR.

## 5. Cursor: `.cursor/hooks.json`

Registers `python3 .agents/hooks/block-destructive.py` in `beforeShellExecution`. Cursor also reads `AGENTS.md` and respects `.cursorignore`.

## 6. Continuous Integration: `.github/workflows/ci.yml`

Runs on each push to `main` and each pull request. Minimal permissions (`contents: read`); cancels previous executions of the same branch.

| Job (visible name) | Machine | What it does | Skip if |
| --- | --- | --- | --- |
| Harness integrity | Ubuntu | Prepares Python 3.12, runs `make validate-harness`, `make audit`, `make test-harness` and checks prohibited local artefacts | Never |
| Secret scan and dependency review | Ubuntu | Runs `make scan-secrets` and, only in pull requests, the dependency review | Dependency review requires the dependency graph (in private repos, GitHub Advanced Security) |
| Android sensor | Ubuntu | Detects `android/gradlew`, installs JDK 17 and Gradle and runs `make sensor-android` | No `android/gradlew` exists |
| iOS build | macOS | Detects `IOS_PROJECT`, shows Xcode and simulator versions and runs `make build-ios` | No Xcode project exists |

To execute iOS tests in CI, replace `make build-ios` with `make sensor-ios` and fix `IOS_DESTINATION` to a simulator that exists in the executor. If your policy requires it, pin third-party actions to a commit SHA. For branch protection, mark the four names in the table as required checks.

## 7. Code Owners: `.github/CODEOWNERS`

The `@your-org/...` markers must be replaced by real teams with write permission. Structure:

| Route | Owners (marker) |
| --- | --- |
| Everything (`*`) | Mobile leaders |
| `/ios/` and `/android/` | iOS team and Android team |
| `AGENTS.md`, platform contracts and `/.agents/` | Mobile leaders and IA governance |
| `/harness.env` and `/scripts/` | Mobile leaders |
| `/.claude/`, `/.codex/`, `/.cursor/` and `/.opencode/` | IA governance |
| `/.github/` | Mobile leaders and security |
| `/.github/decisions/` | Mobile leaders |
| `SECURITY.md` and `docs/security.md` | Security |
| `docs/privacy-compliance.md` | Security and privacy |
| `docs/ai-governance.md` | IA governance and security |

It only takes effect with the branch protection "Require review from Code Owners". The validator checks that it covers control files.

## 8. Dependabot: `.github/dependabot.yml`

Activates weekly updates of GitHub actions. Gradle (`/android`) and Swift (`/ios`) entries are commented: uncomment after creating native projects.

## 9. Ignored and Style Files

| File | What it controls |
| --- | --- |
| `.gitignore` | What is not versioned: system noise, IDE state, builds, secrets and signature. `Package.resolved` **is** versioned |
| `.gitattributes` | LF line endings for scripts and binary marker |
| `.editorconfig` | Indentation (2 spaces by default; 4 in Swift, Kotlin and Python; tabulators in the Makefile) |
| `.aiexclude` and `.cursorignore` | Routes that IA tools must not index |
| `.secrets-allowlist` | Routes that the secret scanner omits |

## 10. Pull Request Template: `.github/pull_request_template.md`

Sections: what and why; board state; verification with command output; dual checklist; IA assistance (tool and trailer, confidential data, dependencies); security and privacy impact; and harness feedback (flywheel, progress notes).

## 11. Where to Change Everything

| What I want to change | I edit |
| --- | --- |
| Project name, Xcode or Gradle routes, simulator, JDK | `harness.env` |
| A technology of the stack (database, navigation, DI, tests) | `docs/customizing.md` procedure (ADR, contract, `docs/stack.md` and reference) |
| The rules the agent follows | `AGENTS.md` or the platform contract, within the line budget |
| What an agent can do | `.claude/settings.json`, `.opencode/opencode.json`, `.codex/config.toml` and the hooks, with IA owners approval |
| The order or routes of a feature | `docs/workflow.md` and `AGENTS.md` in the same change |
| Colors, typographies and components | `docs/design-system.md` and each platform's design system layer |
