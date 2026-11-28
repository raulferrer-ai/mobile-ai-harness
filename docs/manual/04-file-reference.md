# 04 - File Reference

This chapter describes **all** the files that make up the template. The validator checks that none are missing here.

Columns: **What it is** (its function), **Who modifies it** and **When**. "Nobody normally" means it's part of the mechanism and only changes if the harness itself evolves (with owner approval).

The files in your project (code in `ios/` and `android/`, specs `features/NN-*.feature` and ADR own in `docs/decisions/`) are not listed one by one: they are the product, not the harness.

## Repository Root

| File | What it is | Who modifies it | When |
| --- | --- | --- | --- |
| `.aiexclude` | List of routes that IA tools must not index (secrets, builds, IDE state) | Person | When adding sensitive file types |
| `.cursorignore` | Equivalent for Cursor | Person | Same as `.aiexclude` |
| `.editorconfig` | Common indentation and encoding for all editors | Person | When changing style |
| `.gitattributes` | Forces LF line endings in scripts and marks binaries; prevents breaks in Windows | Nobody normally | Almost never |
| `.gitignore` | Excludes from git local artefacts, builds, IDE state and secret material; `Package.resolved` is versioned | Person | When adding tools with new artefacts |
| `.secrets-allowlist` | Patterns of files that the secret scanner must omit (known false positives) | Person | Only after a justifiable false positive |
| `AGENTS.md` | Root contract that every agent reads: truth sources, session graph, loop, dual definition of done, guardrails, flywheel | Person (changes with owner approval) | When adapting project rules; never occasional |
| `CHANGELOG.md` | History of template versions and migration guide | Person | When publishing a template version |
| `CLAUDE.md` | Three-line pointer that refers to `AGENTS.md` for Claude Code | Nobody normally | Almost never |
| `CONTRIBUTING.md` | Collaboration rules for people and agents: spec first, sensors, PR with evidence, owners | Person | When changing the collaboration process |
| `GEMINI.md` | Equivalent pointer for Gemini / Antigravity | Nobody normally | Almost never |
| `Makefile` | Standard entry points (`make ...`) for people, agents and CI; reads `harness.env` | Person (rarely) | Only if a command is added |
| `README.md` | Repo presentation: what it is, quick start, structure, flow, default stack, state | Person | When changing scope or structure |
| `SECURITY.md` | Security policy: how to report vulnerabilities, scope, supported versions, secret handling | Person (security responsible) | When starting the project (fill contact) and when changing policy |
| `feature_list.json` | Board: all features with state, platforms, sensors and gate. It's a state machine | Script (`feature.py`); person does not edit it manually | In every feature transition |
| `harness.env` | Single configuration file: project, platforms, routes, simulator, JDK, budgets and documentation mode | Person | When starting and when routes or tools change |
| `init.sh` | Idempotent start: creates missing state files, validates and shows state and next steps; `--check` only validates | Person or CI | When cloning the repo and after updating the template |

## Platform Contracts

| File | What it is | Who modifies it | When |
| --- | --- | --- | --- |
| `android/AGENTS.md` | Android platform contract: default stack (modifiable), layers, UDF, coroutines, tests and dual definition of done | Person | When deciding or changing Android technology (with ADR) |
| `ios/AGENTS.md` | iOS platform contract: default stack (modifiable), layers, concurrency rules, errors, tests and dual definition of done | Person | When deciding or changing iOS technology (with ADR) |

## Skills (`.agents/skills/`)

| File | What it is | Who modifies it | When |
| --- | --- | --- | --- |
| `.agents/skills/README.md` | Index of the 14 skills; the validator requires it to match existing folders | Person | When adding or removing a skill |
| `.agents/skills/android-architecture-compose/SKILL.md` | Skill: Apply Android contract: layers, UDF, small composables, coroutines and the repository boundary | Person | When improving the procedure (within line budget) |
| `.agents/skills/design-system-parity/SKILL.md` | Skill: Keep tokens, components and states coherent between iOS and Android | Person | When improving the procedure (within line budget) |
| `.agents/skills/feature-spec-writer/SKILL.md` | Skill: Write or refine a Gherkin spec and register it on the board | Person | When improving the procedure (within line budget) |
| `.agents/skills/flywheel-recorder/SKILL.md` | Skill: Convert a deviation into a recorded rule, scenario or sensor | Person | When improving the procedure (within line budget) |
| `.agents/skills/git-governance/SKILL.md` | Skill: Keep commits and work tree clean, scoped and verified, with no IDE artifacts or secrets; with IA trailer | Person | When improving the procedure (within line budget) |
| `.agents/skills/harness-maintainer/SKILL.md` | Skill: Evolve the very harness: skills, scripts, contracts and version baseline | Person | When improving the procedure (within line budget) |
| `.agents/skills/ios-architecture-swiftui/SKILL.md` | Skill: Apply iOS contract: layers, small views, observable view models, concurrency and repository boundary | Person | When improving the procedure (within line budget) |
| `.agents/skills/mobile-accessibility-localization/SKILL.md` | Skill: Accessible and localizable interface: labels, text scaling, contrast, resources | Person | When improving the procedure (within line budget) |
| `.agents/skills/mobile-data-permissions/SKILL.md` | Skill: Persistence, migrations, media, permissions and reminders on both platforms | Person | When improving the procedure (within line budget) |
| `.agents/skills/mobile-security-privacy/SKILL.md` | Skill: Secrets, secure storage, data minimization, logging and network | Person | When improving the procedure (within line budget) |
| `.agents/skills/mobile-testing-harness/SKILL.md` | Skill: Write fast, deterministic unit, repository and UI tests on both platforms and diagnose flaky tests | Person | When adding or fixing tests or interpreting sensor failures |
| `.agents/skills/workflow-implementer/SKILL.md` | Skill: Implement small increments respecting layers and the build-measure-correct loop | Person | When improving the procedure (within line budget) |
| `.agents/skills/workflow-planner/SKILL.md` | Skill: Decompose a spec into verifiable per-platform steps and check parity before coding | Person | When improving the procedure (within line budget) |
| `.agents/skills/workflow-validator/SKILL.md` | Skill: Audit finished work against spec, architecture, states, accessibility and tests before the gate | Person | When improving the procedure (within line budget) |

## Technical References (`.agents/references/`)

| File | What it is | Who modifies it | When |
| --- | --- | --- | --- |
| `.agents/references/android-stack.md` | Android default stack patterns and examples: build, UDF, Room, manual DI, tests, traps | Person | When changing the Android stack (along with ADR and contract) |
| `.agents/references/gherkin-guide.md` | Gherkin spec writing style with complete example and review list | Person | When refining spec style |
| `.agents/references/ios-stack.md` | iOS default stack patterns and examples: Xcode settings, layers, concurrency, view model, repository, tests, traps | Person | When changing the iOS stack (along with ADR and contract) |

## Hooks (`.agents/hooks/`)

| File | What it is | Who modifies it | When |
| --- | --- | --- | --- |
| `.agents/hooks/block-destructive.py` | Hook of commands: blocks recursive forced deletions, `git reset --hard`, forced push, `--no-verify`, shell downloads and feature close by an agent | Nobody normally | Only to adjust command policy |
| `.agents/hooks/check-contract-size.py` | Checks that contracts do not exceed their line budget (limits in `harness.env`) | Nobody normally | Executed by `make validate-harness` and the gate |
| `.agents/hooks/guard-sensitive-paths.py` | Hook of editing: blocks secrets, signing material, IDE state and board editing | Nobody normally | Only to adjust route policy |

## IA Tool Adapters

| File | What it is | Who modifies it | When |
| --- | --- | --- | --- |
| `.claude/settings.json` | Permissions (allow/deny) and hooks for Claude Code; chapter 06 | Person (IA owners) | When changing the tool policy |
| `.codex/config.toml` | Codex configuration: approval policy and sandbox mode | Person (IA owners) | When changing the tool policy |
| `.cursor/hooks.json` | Records the command hook in Cursor | Person (IA owners) | When changing the tool policy |
| `.opencode/opencode.json` | OpenCode configuration: contracts to load and command permissions | Person (IA owners) | When changing the tool policy |

## GitHub Integration (`.github/`)

| File | What it is | Who modifies it | When |
| --- | --- | --- | --- |
| `.github/CODEOWNERS` | Code owners; requires their review on harness control documents and security docs | Person | When starting (replace @your-org markers with real teams) and when changing teams |
| `.github/dependabot.yml` | Automatic dependency updates (GitHub actions active; Gradle and Swift commented) | Person | When creating native projects |
| `.github/pull_request_template.md` | PR template: evidence, dual checklist, IA disclosure, security and flywheel | Person | When changing the review process |
| `.github/workflows/ci.yml` | Continuous integration: harness validation, security, Android sensor and iOS compilation | Person | When adapting CI or activating iOS tests |

### CI Job Table

| Job (visible name) | Machine | What it does | Skip if |
| --- | --- | --- | --- |
| Harness integrity | Ubuntu | Prepares Python 3.12, runs `make validate-harness`, `make audit`, `make test-harness` and checks prohibited local artefacts | Never |
| Secret scan and dependency review | Ubuntu | Runs `make scan-secrets` and, only in pull requests, dependency review | Dependency review requires dependency graph (in private repos, GitHub Advanced Security) |
| Android sensor | Ubuntu | Detects `android/gradlew`, installs JDK 17 and Gradle and runs `make sensor-android` | No `android/gradlew` exists |
| iOS build | macOS | Detects `IOS_PROJECT`, shows Xcode and simulator versions and runs `make build-ios` | No Xcode project exists |

To execute iOS tests in CI, replace `make build-ios` with `make sensor-ios` and fix `IOS_DESTINATION` to a simulator that exists in the executor. If your policy requires it, pin third-party actions to a commit SHA. For branch protection, mark the four names in the table as required checks.

## Code Owners: `.github/CODEOWNERS`

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

## Dependabot: `.github/dependabot.yml`

Activates weekly updates of GitHub actions. Gradle (`/android`) and Swift (`/ios`) entries are commented: uncomment after creating native projects.

## Ignored and Style Files

| File | What it controls |
| --- | --- |
| `.gitignore` | What is not versioned: system noise, IDE state, builds, secrets and signature. `Package.resolved` **is** versioned |
| `.gitattributes` | LF line endings for scripts and binary marker |
| `.editorconfig` | Indentation (2 spaces by default; 4 in Swift, Kotlin and Python; tabulators in the Makefile) |
| `.aiexclude` and `.cursorignore` | Routes that IA tools must not index |
| `.secrets-allowlist` | Routes that the secret scanner omits |

## Pull Request Template: `.github/pull_request_template.md`

Sections: what and why; board state; verification with command output; dual checklist; IA assistance (tool, trailer, confidential data, dependencies); security and privacy impact; and harness feedback (flywheel, progress notes).

## Where to Change Everything

| What I want to change | I edit |
| --- | --- |
| Project name, Xcode or Gradle routes, simulator, JDK | `harness.env` |
| A technology of the stack (database, navigation, DI, tests) | `docs/customizing.md` procedure (ADR, contract, `docs/stack.md` and reference) |
| The rules the agent follows | `AGENTS.md` or the platform contract, within the line budget |
| What an agent can do | `.claude/settings.json`, `.opencode/opencode.json`, `.codex/config.toml` and the hooks, with IA owners approval |
| The order or routes of a feature | `docs/workflow.md` and `AGENTS.md` in the same change |
| Colors, typographies and components | `docs/design-system.md` and each platform's design system layer |
