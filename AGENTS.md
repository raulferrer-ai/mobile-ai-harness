# AGENTS.md - Root contract

Dual-native mobile app (iOS + Android): two native codebases, one product, coordinated by this harness.
Read this file at the start of every session. Keep it lean: details live in `docs/` and `.agents/references/`.

## 1. Source of truth
| Artifact | Role |
| --- | --- |
| `docs/product.md` | What we build, for whom, tone, languages, non-goals |
| `features/*.feature` | Behaviour (Gherkin). Do not invent requirements outside a spec |
| `feature_list.json` | Feature board (a state machine; change it only with `scripts/feature.py`) |
| `progress/current.md` | Session memory: active feature, plan, handoff notes |
| `docs/architecture.md`, `docs/stack.md` | Shared architecture and the default stack per platform |
| `docs/design-system.md`, `docs/parity-matrix.md` | Visual language and intentional platform differences |
| `harness.env` | Commands, paths and budgets (never hardcode them elsewhere) |
| `docs/security.md`, `docs/privacy-compliance.md`, `docs/ai-governance.md` | Security baseline, privacy/store compliance, AI usage rules |

## 2. Rule precedence
1. Platform contract (`ios/AGENTS.md`, `android/AGENTS.md`) for platform idioms.
2. This root contract for workflow, safety and verification.
3. Specs and board. 4. On-demand skills in `.agents/skills/<name>/SKILL.md`.
If a human instruction conflicts with a rule, follow the human and record it (see Flywheel).

## 3. Stack defaults are defaults
The stack, architecture and conventions in the platform contracts are the project's **defaults**, chosen
to be ready to use. They are meant to be changed deliberately: follow `docs/customizing.md` and record the
decision in `docs/decisions/`. Never silently deviate; never "fix" a default by working around it.

## 4. Session protocol
1. Read `progress/current.md`, run `make status`, read the active spec.
2. Work on ONE feature (`in_progress`) and ONE platform per session, unless told otherwise.
3. Load only the skills you need (index: `.agents/skills/README.md`).
4. Follow the graph in `docs/workflow.md`; do not skip nodes.
5. Before ending: update `progress/current.md` (real state + handoff notes) and `progress/log.md`.

## 5. The Loop (build -> sensor -> fix)
1. Implement the smallest change the spec demands, with tests.
2. Run the platform sensor: `make sensor-ios` or `make sensor-android`.
3. Red: fix and repeat. Never report a platform "ready" with a red or unrun sensor.
4. Both platforms green: run the gate `make gate`.
5. Sensors write `sensor_green` to the board themselves; you cannot set it by hand.

## 6. Definition of Done (dual)
A feature is `done` only when ALL hold:
1. The spec exists and the behaviour matches it.
2. Implemented on every platform the feature targets, each with tests.
3. Sensors green on each platform; gate passed (`make gate`).
4. Human dual checklist completed (`docs/dual-checklist.md`).
5. A human ran `python3 scripts/feature.py done <id> --human-checklist-ok`.
Agents never run step 5 and never pass `--human-checklist-ok`.

## 7. Commands
`make help` lists everything. Key ones: `make status`, `make sensor-ios`, `make sensor-android`,
`make gate`, `make validate-harness`, `make test-harness`, `make clean-ide`.
Board: `python3 scripts/feature.py add|start|platform|block|status|list` (see `--help`).

## 8. Guardrails
- Never run destructive commands (`rm -rf`, `git reset --hard`, `git push --force`, `git clean -f`) without human approval.
- Never read, print or commit secrets (`.env*`, keystores, certificates, provisioning profiles,
  `google-services.json`, `GoogleService-Info.plist`) or local IDE state (`xcuserdata`, `.idea/`).
- Never edit or delete an existing test just to make a sensor pass. Fix the code or ask the human.
- Never hand-edit `feature_list.json`, bypass hooks (`--no-verify`) or mark work verified without evidence.
- Product copy and tone follow `docs/product.md`; UI follows `docs/design-system.md`.
- Logs and analytics must not contain personal data.
- Never put confidential data (credentials, customer data, unreleased plans) into prompts; follow `docs/ai-governance.md`
  and the security rules in `docs/security.md`. Disclose AI assistance in PRs.
- Do not add dependencies without a stated reason; verify the package is real and maintained.

## 9. Flywheel (failure -> rule)
If you deviate from a spec, the design system or this contract (or the human catches you doing so):
1. Fix the code. 2. Add an entry to `progress/flywheel-log.md` (template: `docs/flywheel.md`).
3. If the failure is clear and repeatable, add a rule, a spec scenario or a test (skill: flywheel-recorder).
The same failure twice means the harness has a hole: it must gain a rule or a sensor.

## 10. Human suspend points
Dual checklist, closing a feature, merge, tag/release, scope change, and any change to defaults
(`docs/customizing.md`). Stop and ask; do not decide these alone.

## 11. Anti-bloat
This file stays within the budget in `harness.env` (checked by `make validate-harness`). Add detail to `docs/`
or `.agents/references/`, not here. Do not duplicate content across skills; link to it.
