# Customizing the harness

Everything in this template is a default. Changing a default is normal and supported; changing it *silently* is not.
The rule: **one decision, one change set** - decide, record, update every place that states it, validate.

## The change checklist (any stack or architecture change)
1. **Decide** (human). Confirm the reason is real, not preference drift.
2. **Record** an ADR: copy `docs/decisions/0000-template.md` to `docs/decisions/NNNN-<title>.md`.
3. **Update the places that state the default** (tech specifics live in only these four):
   - platform contract `ios/AGENTS.md` / `android/AGENTS.md` (Stack table + Rules)
   - `docs/stack.md` (tables + baseline)
   - `.agents/references/ios-stack.md` / `android-stack.md` (patterns, samples)
   - `harness.env` and `Makefile`/CI if a command, path or tool changes
4. **Check skills.** Skills are deliberately tech-light and link to the references; only edit one if its steps changed.
5. **Validate:** `make validate-harness` and `make test-harness`.
6. **Log** the change in `progress/log.md`.

## Recipes
| I want to... | Do this |
| --- | --- |
| Swap Room for SQLDelight (or Room 3 -> 2.x) | Checklist above; edit the Persistence row/rules in `android/AGENTS.md`, the Room section in `android-stack.md`, the dependency lines in your version catalog |
| Swap SwiftData for Core Data/GRDB | Same; keep the repository protocol and the "never expose entities" rule |
| Use Hilt or Koin instead of the manual container | Update the DI row and rule; keep constructor injection; update the composition-root section in `android-stack.md` |
| Use Navigation 3 | Update the Navigation row and the navigation section in `android-stack.md` |
| Use XCTest instead of Swift Testing | Update the "Unit tests" row and the testing samples in `ios-stack.md` |
| Ship on one platform only | Set `PLATFORMS="android"` (or `ios`) in `harness.env`; delete the other contract only if you are sure; `validate-harness` adapts |
| Add a platform (e.g. watchOS, Wear OS) | Add its directory + `AGENTS.md`, add it to `PLATFORMS`, add it to the sensors in `scripts/sensor.sh`, extend `docs/parity-matrix.md`, ADR |
| Change the order of work (Android first) | It is only a convention: say it in `progress/current.md`; the graph is order-agnostic |
| Loosen/tighten line budgets | `BUDGET_*` in `harness.env` |
| Change the product language | `docs/product.md`; keep code identifiers in English |
| Apply company-wide rules on top of this template | Keep corporate rules in a separate, versioned "base" repo or template and merge it in; project-specific decisions stay in this repo's ADRs. Tool-level managed settings (where vendors offer them) enforce what must not be loosened locally |
| Use a different CI | Keep calling `make validate-harness`, `make test-harness`, `make sensor-*`; they are the contract |
| Share code with KMP or move to Flutter | Out of this template's thesis. Fork it, rewrite `docs/architecture.md` and the contracts, add a shared-module contract |

## What not to change casually
- The board state machine (`scripts/feature.py`) and the "human-only" close step. They exist so a green status means evidence.
- The zero-symlink rule and plain-text pointers (`CLAUDE.md`, `GEMINI.md`): they keep the harness portable across OSes and tools.
- The Flywheel rule (same failure twice means a new rule or sensor).

## Updating from a newer template version
Diff by area: `scripts/` and `.agents/hooks/` (take the new ones), `docs/workflow.md` and `docs/flywheel.md` (take),
`harness.env` (merge: keep yours, add new keys; `validate-harness` names missing ones), platform contracts and
`docs/stack.md` (merge by hand: these hold your decisions).
