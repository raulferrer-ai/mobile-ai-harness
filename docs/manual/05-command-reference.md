# 05 - Command Reference

This chapter documents **all** harness commands: `make` targets, the board CLI, scripts, hooks and external commands that run underneath. The validator checks that every `make` target and every `scripts/feature.py` subcommand appears here.

## 1. Conventions

### Exit Codes (common to the whole harness)

| Code | Meaning |
| --- | --- |
| 0 | Correct |
| 1 | Failure: a test, a validation or a precondition is not met |
| 2 | Blocked by policy: action prohibited to an agent (close a feature, mark `sensor_green` by hand, destructive command) |
| 3 | Partial or not available: a sensor could not execute on this machine. **Never equals green** |
| 64 | Incorrect use of `scripts/sensor.sh` (unknown goal) |

**Important when using `make`:** when a recipe target fails, `make` always ends with code 2, regardless of the script's original code. To see the original code (e.g. 3, partial), execute the script directly (`sh scripts/verify-feature.sh`, `sh scripts/sensor.sh ios`).

**Who can execute what:** except where indicated, all commands can be executed by people and agents. Marked **only person** (`feature.py done` and `feature.py remove`) are blocked for agents by hooks and permissions.

All commands are executed from the repository root.

## 2. `make` Targets

`make help` (or `make` alone) lists the targets. All read `harness.env` configuration.

| Command | What exactly it executes | When to use it |
| --- | --- | --- |
| `make help` | Shows the list of targets with their description and reminds what is only human | When you don't remember a command |
| `make init` | `sh init.sh` | When cloning the repo and after updating the template |
| `make validate-harness` | `python3 scripts/validate-harness.py`, then `python3 .agents/hooks/check-contract-size.py`, then `python3 scripts/scan-secrets.py` | Before each commit and in CI |
| `make scan-secrets` | `python3 scripts/scan-secrets.py` | To check only secrets |
| `make audit` | `python3 scripts/audit-architecture.py` | After code changes; part of the gate |
| `make doctor` | `sh scripts/doctor.sh` | When preparing a new machine or environment failures |
| `make test-harness` | `python3 -m unittest discover -s scripts/tests -v` | After touching scripts or hooks of the harness; in CI |
| `make status` | `python3 scripts/feature.py status` | At the start and end of each session |
| `make sensor-ios` | `sh scripts/sensor.sh ios` | After implementing in iOS |
| `make sensor-android` | `sh scripts/sensor.sh android` | After implementing in Android |
| `make sensors` | Runs `sensor-ios` and then `sensor-android` | In a Mac, with both platforms. Stops at the first failure |
| `make build-ios` | `sh scripts/sensor.sh build-ios` | CI: compiles without signing and without specific simulator |
| `make lint-ios` | `sh scripts/sensor.sh lint-ios` | If you have configured `IOS_LINT_CMD` |
| `make lint-android` | `sh scripts/sensor.sh lint-android` | If you have configured `ANDROID_LINT_TASK` |
| `make gate` | `sh scripts/verify-feature.sh $(FEATURE)` | When both platforms are in green. Admits `make gate FEATURE=<id>` |
| `make verify` | `validate-harness`, then `test-harness`, then `gate` | Complete check before requesting review |
| `make simulators` | `xcrun simctl list devices available` | To choose `IOS_DESTINATION` |
| `make clean-ide` | `find` that deletes `*.xcuserstate`, `.DS_Store` and `Thumbs.db` (excludes `.git`) | If the gate rejects local artefacts |

**Important notes:**

- **No target to close a feature** or for the dual checklist: human decisions.
- On Linux or Windows, `make sensors` fails in iOS (code 3, "not available"). Use `make sensor-android` and leave the iOS part for a Mac or CI.
- `make gate` without any `in_progress` feature executes only the harness checks and ends in 0.

## 3. Board CLI: `scripts/feature.py`

It is **the only authorized way** to change `feature_list.json`. Invoked as `python3 scripts/feature.py <subcommand>`. Help: `python3 scripts/feature.py --help`.

| Subcommand | Syntax | What it does and what it demands | Errors and codes |
| --- | --- | --- | --- |
| `feature.py status` | `status` | Shows project, count by state, active feature (or the next planned) and what command to execute | 0 |
| `feature.py list` | `list` | One line per feature: priority, state, id and state by platform | 0 |
| `feature.py next` | `next [--active-only]` | Prints the id of the active feature; without `--active-only`, if there isn't, the next `planned` by priority. The gate uses it | 0 |
| `feature.py platforms` | `platforms <id>` | Prints the platforms of the feature separated by spaces. The gate uses it | 1 if the id does not exist |
| `feature.py add` | `add <id> "<título>" --spec <ruta> [--priority N] [--platforms ios,android]` | Registers a `planned` feature. The id goes in lowercase with hyphens; must be unique; the spec must exist, contain `Feature:` and at least one `Scenario:` and not keep `@template-placeholder`. Without `--platforms`, uses all from `harness.env`. Without `--priority`, uses the maximum existing plus one | 1 if any condition fails |
| `feature.py start` | `start <id>` | Takes the feature to `in_progress`. Only one at a time; only if it's `planned` or `blocked`; revalidates the spec | 1 if there's already another active or the state doesn't allow it |
| `feature.py platform` | `platform <id> <plataforma> <estado>` | Changes by hand the state of a platform between `pending` and `in_progress` (feature in progress). **`sensor_green` is prohibited**: only writes it a sensor | 2 if you ask for `sensor_green`; 1 in other failures |
| `feature.py record-sensor` | `record-sensor <plataforma> [--fail] [--mode test o build]` | Invoked by `scripts/sensor.sh`. Success: the platform goes to `sensor_green`, saves hour and mode and **deletes the previous gate**. With `--fail`: goes back to `in_progress`, removes the sensor and deletes the gate. If there's not a single active feature, it warns and ends in 0 | 0 |
| `feature.py gate` | `gate <id> --sensors ios,android` | Invoked by the gate. Demands feature `in_progress` and that the list covers all its platforms. Records hour, sensors and degraded platforms (mode different from `test`) | 3 if missing platforms ("incomplete gate"); 1 in other failures |
| `feature.py done` | `done <id> --human-checklist-ok` | **Only person.** Closes the feature: demands the flag, feature `in_progress`, gate registered that covers all platforms and all `sensor_green`. Takes platforms to `done`, state `done`, `verified: true` and `completed_at`. Warns if closed with degraded sensors | 2 without the flag; 1 in other failures |
| `feature.py block` | `block <id> --reason "<motivo>"` | Marks the feature as `blocked`, saves the reason and deletes the gate. Cannot block a `done`. Resumed with `start` | 1 if the feature is `done` |
| `feature.py remove` | `remove <id>` | **Only person** (it's a scope decision). Eliminates from the board a feature that **is not `done`**; warns that its spec should also be deleted if no longer needed. A `done` feature is part of the history and cannot be eliminated with the CLI | 1 if the feature is `done` or does not exist |
| `feature.py check` | `check [id]` | Validates the spec of the indicated feature or the active one. The gate uses it | 1 if the spec is not valid |
| `feature.py validate` | `validate` | Reviews the board invariants (schema, ids, states, only one active, coherent `done` with its gate) | 1 with the list of violations |
| `feature.py import-legacy` | `import-legacy <ruta-al-json>` | Converts an old v1 board format to the current format. `done` features keep `legacy` gate. **Overwrites `feature_list.json`** | 1 if the origin is not a list |

### Minimum Cycle Example:

```bash
python3 scripts/feature.py add plant-list "Lista de plantas" --spec features/02-plant-list.feature
python3 scripts/feature.py start plant-list
make sensor-ios            # the sensor marks ios as sensor_green
make sensor-android        # idem android
make gate                  # registers the gate
python3 scripts/feature.py done plant-list --human-checklist-ok   # ONLY a person
```

## 4. Scripts

### 4.1 `scripts/sensor.sh`

Usage: `sh scripts/sensor.sh <goal>`. It's the only implementation of the sensors (used by `make`, the gate and the CI).

| Goal | What it does | Detail |
| --- | --- | --- |
| `ios` | Executes iOS tests | With `IOS_SENSOR_MODE=test`: `xcodebuild test`. With `build`: `xcodebuild build` (degraded mode, registers as such). Registers the result in the board |
| `android` | Executes Android JVM tests | `sh ./gradlew <ANDROID_TEST_TASK> --quiet` within `ANDROID_DIR`. Requires JDK equal or superior to `MIN_JDK` |
| `build-ios` | Compiles iOS without signing | `xcodebuild build` with `CODE_SIGNING_ALLOWED=NO` and the destination `IOS_CI_DESTINATION`. Does not register anything in the board |
| `lint-ios` | Executes optional lint | Executes `IOS_LINT_CMD`; if empty, warns and exits with 0 |

**Codes:** 0 green; 1 red (tests or compilation fail); 3 sensor **not available** (iOS: not macOS, missing `xcodebuild` or `IOS_PROJECT` does not exist; Android: missing `gradlew`, missing `java` or JDK previous to `MIN_JNK`); 64 unknown goal.

### 4.2 `scripts/verify-feature.sh` (the gate)

Usage: `sh scripts/verify-feature.sh [id-de-feature]` (or `make gate`). Optional variable: `SKIP_SENSORS="ios"` to explicitly omit a platform (the result will be partial).

| Step | Checks |
| --- | --- |
| 1/5 | Integrity of the harness (`validate-harness.py`), contract budgets (`check-contract-size.py`), secrets (`scan-secrets.py`) and architecture audit (`audit-architecture.py`) |
| 2/5 | That there are no prohibited local artefacts (`*.xcuserstate`, `.DS_Store`, `Thumbs.db`) |
| 3/5 | Resolves the feature: the indicated one or the active. If there's none, ends in 0 after steps 1 and 2 |
| 4/5 | The spec is valid (`feature.py check`) |
| 5/5 | Executes the sensor of each platform of the feature and, if all pass, registers the gate |

**Result:** **0** gate approved and registered (prints next human step); **1** gate failed (some sensor red); **3** gate partial (some sensor not available or omitted: does not register and does not allow closing).

### 4.3 `init.sh`

Usage: `sh init.sh` or `sh init.sh --check`. Checks that `git` and `python3` (3.9 or superior) exist. Without `--check`, creates the missing state files (`progress/current.md`, `progress/log.md`, `progress/flywheel-log.md`, `feature_list.json`) and gives execution permission to the scripts. In both modes validates the harness, shows the board state, indicates what sensors are available in the machine and, without `--check`, prints the next steps. It is idempotent: it can be repeated without risk.

### 4.4 `scripts/doctor.sh`

Usage: `sh scripts/doctor.sh` (or `make doctor`). Diagnoses and marks `[ok]`, `[warn]` or `[FAIL]`:

- **Core:** `git`, `make` and Python 3.9 or superior.
- **Android:** JDK equal or superior to `MIN_JDK`, existence of `gradlew` and variable `ANDROID_HOME` or `ANDROID_SDK_ROOT`.
- **iOS** (only in macOS): `xcodebuild`, Swift version, number of iPhone simulators and existence of `IOS_PROJECT`.

Exits with 1 if there's any `[FAIL]`; `[warn]` do not block.

### 4.5 `scripts/validate-harness.py`

Usage: `python3 scripts/validate-harness.py`. Executes, in order:

1. Prohibition of symbolic links.
2. Existence of mandatory files.
3. Presence of required keys in `harness.env`.
4. Contract line budgets.
5. `CLAUDE.md` and `GEMINI.md` point to `AGENTS.md`.
6. Scripts hygiene: correct shebang, shell syntax (`sh -n`) and Python compilation.
7. Validity of JSON and TOML.
8. `CODEOWNERS` coverage over control files (the `@your-org` markers only warn).
9. Board invariants and warning of unregistered specs.
10. Skills: correct header, same name as folder, description up to 1024 characters, line budget and coherent index.
11. Document and route links that must exist; `make <target>` mentioned must exist.
12. Manual completeness (warning or error according to `DOCS_COMPLETENESS`).

### 4.6 `scripts/scan-secrets.py`

Usage: `python3 scripts/scan-secrets.py` (or `make scan-secrets`). Analyzes repo files (according to `git ls-files` or, without git, traversing the tree). Detects:

- Private keys, AWS access keys, Google API keys, Slack and GitHub tokens.
- Credentials written in the code (`api_key`, `secret`, `passwd`, `password` or `token` assigned to a chain of 12 or more characters).
- Prohibited file types: `.env` and `.env.*` (except `.env.example` and `.env.sample`), `*.jks`, `*.keystore`, `keystore.properties`, `*.p12`, `*.pfx`, `*.pem`, `*.mobileprovision`, `*.provisionprofile`, `google-services.json`, `GoogleService-Info.plist` and `local.properties`.

Omits binaries, files of more than 1 MB and the routes of `.secrets-allowlist`. A line is exempted with the `secrets:allow` marker. If something appears: **rotate the secret** (it's already compromised) and then eliminate it.

### 4.7 `scripts/audit-architecture.py`

Usage: `python3 scripts/audit-architecture.py [--update-baseline] [--warn-only]`. Reads `IOS_SRC_DIR`, `ANDROID_SRC_DIR` and `IOS_DOMAIN_ALLOWED_IMPORTS` from `harness.env`.

| Rule | What it detects |
| --- | --- |
| `IOS-DOMAIN-IMPORT` | A `Domain` file imports something outside the allowed list (by default, only Foundation) |
| `IOS-FEATURE-PERSISTENCE` | A feature uses `import SwiftData`, `@Query` or `ModelContext` |
| `IOS-COLOR-LITERAL` | Color literal outside the design system in a feature |
| `IOS-TASK-DETACHED` | Use of `Task.detached` without justification |
| `IOS-UNCHECKED-SENDABLE` | Use of `@unchecked Sendable` |
| `IOS-FORCE-TRY` | `try!` in production code |
| `IOS-TEST-SLEEP` | `sleep` in tests |
| `AND-DOMAIN-IMPORT` | A `domain` file imports Android or Jetpack APIs ( `androidx.annotation` is allowed) |
| `AND-FEATURE-PERSISTENCE` | A feature imports Room or `data.local` types |
| `AND-COLOR-LITERAL` | `Color(0x...)` outside the design system in a feature |
| `AND-GLOBALSCOPE` | Use of `GlobalScope` |
| `AND-TEST-SLEEP` | `Thread.sleep` in tests |

- A line is exempted with `audit:allow` followed by the reason.
- `--update-baseline` writes `.audit-baseline` with the current count per file and rule; from then on only new violations (more occurrences than registered) fail.
- `--warn-only` shows the violations without failing.
- Without audit sources, ends in 0.

### 4.8 `.agents/hooks/check-contract-size.py`

Checks the line budget of `AGENTS.md`, `ios/AGENTS.md`, `android/AGENTS.md`, `CLAUDE.md` and `GEMINI.md` (limits `BUDGET_*` of `harness.env`). Exits with 1 if any of them is exceeded.

### 4.9 Security Hooks

They are invoked by IA tools before each action; they receive the content of the action via standard input. They return **2** to block (the reason is shown to the agent) and **0** to allow.

**`.agents/hooks/block-destructive.py`** (shell commands) blocks:

| Pattern | Reason |
| --- | --- |
| `rm -rf`, `rm -fr`, `rm -r -f` and variants | Forced recursive deletion |
| `git reset --hard` | Discards work |
| `git push --force` and `git push -f` (not `--force-with-lease`) | Rewrites shared history |
| `git clean -f` | Deletes untracked files |
| `git checkout .` | Discards changes |
| `git branch -D` | Deletes branches without checking |
| `--no-verify` | Skips git checks |
| `sudo` | Privilege escalation |
| `curl` or `wget` chained to `sh`, `bash` or `zsh` | Executes downloaded code without review |
| `chmod -R 777` | Open permissions |

**`.agents/hooks/guard-sensitive-paths.py`** (editing hook) blocks `.env` and `.env.*` (except `.env.example` and `.env.sample`), `*.jks`, `*.keystore`, `keystore.properties`, `*.p12`, `*.pfx`, `*.pem`, `*.key`, `*.cer`, `*.crt`, `*.der`, `*.mobileprovision`, `*.provisionprofile`, `local.properties`, `google-services.json`, `GoogleService-Info.plist`, `*.xcuserstate`, the `xcuserdata` routes and `.idea/workspace.xml`, and the direct editing of `feature_list.json`.

## 5. External Commands the Harness Executes

| Command | Who executes it | For what |
| --- | --- | --- |
| `xcodebuild test -project <IOS_PROJECT> -scheme <IOS_SCHEME> -destination <IOS_DESTINATION> -quiet` | `sensor.sh ios` | Compile and run iOS tests |
| `xcodebuild build ... -quiet` | `sensor.sh ios` (mode `build`) | Only compile |
| `xcodebuild build ... -destination <IOS_CI_DESTINATION> CODE_SIGNING_ALLOWED=NO -quiet` | `sensor.sh build-ios` | Compile for CI without signing |
| `sh ./gradlew <tarea> --quiet` | `sensor.sh android` and `lint-android` | Execute Android tests or lint |
| `java -version` | `sensor.sh`, `doctor.sh` | Read the JDK version |
| `xcodebuild -version`, `swift --version` | `doctor.sh`, CI | Show Apple tools versions |
| `xcrun simctl list devices available` | `make simulators`, `doctor.sh`, CI | List simulators |
| `git ls-files -co --exclude-standard` | `scan-secrets.py` | Obtain files to analyze |
| `git --version` | `doctor.sh` | Show the git version |
| `sh -n <fichero>` | `validate-harness.py` | Check shell script syntax |
| `find`, `grep`, `awk`, `uname`, `chmod`, `mkdir`, `cat`, `printf`, `command -v` | `Makefile`, `init.sh`, scripts | POSIX utilities for searches, formatting and checks |
| `python3 -m unittest discover -s scripts/tests -v` | `make test-harness` | Execute the harness tests |

## 6. `make` Environment Variables and Make

| Variable | Where it is used | Effect |
| --- | --- | --- |
| `FEATURE` | `make gate FEATURE=<id>` | Verifies that feature instead of the active one |
| `SKIP_SENSORS` | `scripts/verify-feature.sh` | List of platforms to omit (partial result) |
| `JAVA_HOME` | Gradle and `java` | Selects the JDK; the Android sensor requires the minimum version |
| `ANDROID_HOME` or `ANDROID_SDK_ROOT` | `doctor.sh` and Gradle | SDK of Android location |
| `DOCS_COMPLETENESS` | `scripts/validate-harness.py` | `strict` or `warn`; has priority over `harness.env` |
| `PYTHONDONTWRITEBYTECODE` | CI | Avoids creating `.pyc` files |

The rest of the configuration is in `harness.env` (see chapter 06).

## 7. Recommended `git` Commands

| Command | When |
| --- | --- |
| `git status` and `git diff` | Before each commit: review each file |
| `git commit -m "..."` with the final line `AI-Assisted: <herramienta>/<modelo>` | If an agent materially produced the change |
| `git apply --check <parche>` and `git apply <parche>` | When applying an external patch |
| `git rm -r --cached <ruta>` | To stop versioning already confirmed local artefacts |

## 8. What an Agent Should Never Execute

`feature.py done`, `feature.py remove`, the flag `--human-checklist-ok`, `rm -rf` and variants, `git reset --hard`, `git push --force`, `git commit --no-verify`, `sudo`, downloaded shell chains, and any reading or editing of secrets or signing material. They are blocked by hooks and permissions; if an agent attempts it, it's treated as a deviation and registered in `progress/flywheel-log.md`.

## 9. Commands of git that the process recommends

| Command | When |
| --- | --- |
| `git status` and `git diff` | Before each commit: review each file |
| `git commit -m "..."` with the final line `AI-Assisted: <herramienta>/<modelo>` | If an agent produced materially the change |
| `git apply --check <parche>` and `git apply <parche>` | When applying an external patch |
| `git rm -r --cached <ruta>` | To stop versioning already confirmed local artefacts |

## 9. External Commands the Harness Executes (repeated for completeness)

| Command | Who executes it | For what |
| --- | --- | --- |
| `xcodebuild test -project <IOS_PROJECT> -scheme <IOS_SCHEME> -destination <IOS_DESTINATION> -quiet` | `sensor.sh ios` | Compile and run iOS tests |
| `xcodebuild build ... -quiet` | `sensor.sh ios` (mode `build`) | Only compile |
| `xcodebuild build ... -destination <IOS_CI_DESTINATION> CODE_SIGNING_ALLOWED=NO -quiet` | `sensor.sh build-ios` | Compile for CI without signing |
| `sh ./gradlew <tarea> --quiet` | `sensor.sh android` and `lint-android` | Execute Android tests or lint |
| `java -version` | `sensor.sh`, `doctor.sh` | Read the JDK version |
| `xcodebuild -version`, `swift --version` | `doctor.sh`, CI | Show Apple tools versions |
| `xcrun simctl list devices available` | `make simulators`, `doctor.sh`, CI | List simulators |
| `git ls-files -co --exclude-standard` | `scan-secrets.py` | Obtain files to analyze |
| `git --version` | `doctor.sh` | Show the git version |
| `sh -n <fichero>` | `validate-harness.py` | Check shell script syntax |
| `find`, `grep`, `awk`, `uname`, `chmod`, `mkdir`, `cat`, `printf`, `command -v` | `Makefile`, `init.sh`, scripts | POSIX utilities for searches, formatting and checks |
| `python3 -m unittest discover -s scripts/tests -v` | `make test-harness` | Execute the harness tests |

## 10. Environment Variables and `make` (repeated for completeness)

| Variable | Where it is used | Effect |
| --- | --- | --- |
| `FEATURE` | `make gate FEATURE=<id>` | Verifies that feature instead of the active one |
| `SKIP_SENSORS` | `scripts/verify-feature.sh` | List of platforms to omit (partial result) |
| `JAVA_HOME` | Gradle and `java` | Selects the JDK; the Android sensor requires the minimum version |
| `ANDROID_HOME` or `ANDROID_SDK_ROOT` | `doctor.sh` and Gradle | SDK of Android location |
| `DOCS_COMPLETENESS` | `scripts/validate-harness.py` | `strict` or `warn`; has priority over `harness.env` |
| `PYTHONDONTWRITEBYTECODE` | CI | Avoids creating `.pyc` files |

The rest of the configuration is in `harness.env` (see chapter 06).

## 11. Recommended `git` Commands (repeated for completeness)

| Command | When |
| --- | --- |
| `git status` and `git diff` | Before each commit: review each file |
| `git commit -m "..."` with the final line `AI-Assisted: <herramienta>/<modelo>` | If an agent materially produced the change |
| `git apply --check <parche>` and `git apply <parche>` | When applying an external patch |
| `git rm -r --cached <ruta>` | To stop versioning already confirmed local artefacts |

## 12. What an Agent Should Never Execute (repeated for completeness)

`feature.py done`, `feature.py remove`, the flag `--human-checklist-ok`, `rm -rf` and variants, `git reset --hard`, `git push --force`, `git commit --no-verify`, `sudo`, downloaded shell chains, and any reading or editing of secrets or signing material. They are blocked by hooks and permissions; if an agent attempts it, it's treated as a deviation and registered in `progress/flywheel-log.md`.

---

## 6. Environment Variables and `make` (summary)

| Variable | Where it is used | Effect |
| --- | --- | --- |
| `FEATURE` | `make gate FEATURE=<id>` | Verifies that feature instead of the active one |
| `SKIP_SENSORS` | `scripts/verify-feature.sh` | List of platforms to omit (partial result) |
| `JAVA_HOME` | Gradle and `java` | Selects the JDK; the Android sensor requires the minimum version |
| `ANDROID_HOME` or `ANDROID_SDK_ROOT` | `doctor.sh` and Gradle | SDK of Android location |
| `DOCS_COMPLETENESS` | `scripts/validate-harness.py` | `strict` or `warn`; has priority over `harness.env` |
| `PYTHONDONTWRITEBYTECODE` | CI | Avoids creating `.pyc` files |

The rest of the configuration is in `harness.env` (see chapter 06).

## 12. Recommended `git` Commands (summary)

| Command | When |
| --- | --- |
| `git status` and `git diff` | Before each commit: review each file |
| `git commit -m "..."` with the final line `AI-Assisted: <herramienta>/<modelo>` | If an agent materially produced the change |
| `git apply --check <parche>` and `git apply <parche>` | When applying an external patch |
| `git rm -r --cached <ruta>` | To stop versioning already confirmed local artefacts |

---

## 7. What an Agent Should Never Execute (summary)

`feature.py done`, `feature.py remove`, the flag `--human-checklist-ok`, `rm -rf` and variants, `git reset --hard`, `git push --force`, `git commit --no-verify`, `sudo`, downloaded shell chains, and any reading or editing of secrets or signing material. They are blocked by hooks and permissions; if an agent attempts it, it's treated as a deviation and registered in `progress/flywheel-log.md`.
