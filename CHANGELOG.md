# Changelog

## 2.1.0 - 2026-11-20

Enterprise-readiness pass: security and supply chain, AI governance, and a reference slice to prove the loop.

### Added
- **Security and supply chain:** `docs/security.md` (OWASP MASVS checklist, threat-model template, supply-chain rules,
  release gate, incidents), `SECURITY.md`, `scripts/scan-secrets.py` (secret patterns + forbidden files; also in
  `make validate-harness`, the gate and CI), CI `security` job (secret scan, dependency review on PRs),
  `.github/dependabot.yml`, `.secrets-allowlist`.
- **Privacy and store compliance:** `docs/privacy-compliance.md` (data inventory, Apple privacy manifest and labels,
  Google Play Data safety, GDPR-style principles, accessibility as compliance, SDK review).
- **AI governance:** `docs/ai-governance.md` (approved tools, data classification, review, disclosure and traceability,
  IP, agent permissions, incidents, multi-agent rules), `.github/CODEOWNERS` covering the harness control files
  (validated), `CONTRIBUTING.md`, AI-assistance and security sections in the PR template, commit trailer convention.
- **Bootstrap:** `docs/bootstrap.md` (step by step, plus the organization adoption checklist), `scripts/doctor.sh`
  (`make doctor`), and `templates/sample-feature/` (spec + iOS/Android slice with tests) to verify the loop on your toolchain.

### Fixed
- `.gitignore` ignored `Package.resolved`; apps must commit it for reproducible dependency resolution.

### Known limits (unchanged scope)
- The reference slice and the native build settings have **not been compiled** by the template (no Xcode/Gradle project
  is bundled); the first `make sensors` on a real toolchain is the verification. Release/delivery, environments,
  feature flags and crash reporting are planned for v3.

## 2.0.0 - 2026-10-09

Rebuilt from v1 (symlink-free harness) plus what the Leafly case study taught in practice (Loop, Graph, Flywheel).

### Added
- **Default stack and architecture per platform**, clearly marked as modifiable: platform contracts,
  `docs/stack.md` (with a version baseline verified 2026-09-18), `docs/architecture.md`,
  `.agents/references/{ios,android}-stack.md`, ADR `0001`, and `docs/customizing.md` with swap recipes.
- **Loop / Graph / Flywheel** from Leafly: `docs/workflow.md` (mermaid graph, nodes, routes, suspend points),
  `docs/flywheel.md`, `progress/flywheel-log.md`, flywheel-recorder skill.
- **Board state machine** `scripts/feature.py`: one `in_progress` feature, sensors write `sensor_green`, a gate is recorded,
  closing needs `--human-checklist-ok` (blocked for agents by hooks/permissions). Validator re-checks invariants.
- **`harness.env`** as the single configuration file (paths, simulator, JDK, budgets). No project names hardcoded.
- **`scripts/sensor.sh`**: one implementation for Makefile, gate and CI. Missing toolchains are *unavailable* (exit 3), never a silent pass.
- **Gate** can end `PASSED`, `FAILED` or `PARTIAL`; only a full pass is recorded.
- Skills: `feature-spec-writer`, `flywheel-recorder`, `mobile-accessibility-localization`, `mobile-security-privacy`
  (14 total, each within a line budget).
- `docs/product.md`, `docs/dual-checklist.md`, real `docs/parity-matrix.md`, PR template, `.gitattributes`, `.editorconfig`.
- Anti-drift validator checks: backticked paths and `make` targets in docs must exist, skills index consistency, shell syntax.
- Harness unit tests (`make test-harness`) and CI jobs for harness, Android and iOS.

### Fixed (v1 bugs)
- `docs/parity-matrix.md` was a copy of `design-system.md`.
- Feature board filename mismatch (`features/feature-list.json` vs `feature_list.json`) and an example entry pointing to a missing spec.
- `features/00-template.feature` was empty.
- Hook `case` patterns such as `"*.jks"` were quoted and never matched; hooks now parse the tool JSON and use real globs.
- Budgets duplicated in two scripts; now read from `harness.env`.
- Makefile and gate hardcoded the Leafly project path and simulator.
- `.agents/references/` was documented but missing.
- Gate treated a missing toolchain as success.

### Changed
- Hooks are Python 3 (`.agents/hooks/*.py`), not POSIX sh, to parse JSON reliably. Python 3.9+ is required.
- Skill `mobile-persistence-notifications` renamed to `mobile-data-permissions` (generic, not reminder-specific).
- `feature_list.json` is now `{ "schema_version": 2, "features": [...] }` with per-platform states and a `gate` record.
- Platform contract budget raised from 100 to 130 lines to hold the stack tables; root 140 -> 150.
- Contracts and docs are English; product copy language is set in `docs/product.md`.

### Migration
**From v1 (mobile-ai-harness):** copy the new files over; keep your own `features/`, `progress/`, specs and
platform-contract decisions; merge `harness.env` values; delete `.agents/hooks/*.sh` and `scripts/check-*` leftovers;
run `sh init.sh`.

**From Leafly (array board):**
```bash
cp /path/to/leafly/feature_list.json /tmp/leafly-board.json
python3 scripts/feature.py import-legacy /tmp/leafly-board.json   # converts to schema 2, marks done features as legacy-gated
make validate-harness
```
Then set `IOS_PROJECT`, `IOS_SCHEME`, `IOS_DESTINATION` in `harness.env` to your Leafly values.
