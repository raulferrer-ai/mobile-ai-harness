---
name: flywheel-recorder
description: Turn an agent deviation or missed defect into a log entry plus a rule, spec scenario or sensor. Use when work drifted from the spec, design system or Definition of Done.
---

# Flywheel Recorder

## Summary
Fixing code is half the job; the other half is making the same failure impossible or at least detectable next time.

## When to use
- You or the human noticed a deviation (spec, design system, contract, DoD).
- The same kind of problem has appeared before.

## Steps
1. Fix the code first and re-run the sensor.
2. Add an entry at the top of `progress/flywheel-log.md` using the template in `docs/flywheel.md`.
3. Choose the strongest fix that is justified: sensor/validator check > spec scenario > contract rule > doc note.
4. If the failure occurred twice, the fix is mandatory, not optional.
5. Apply it in the right place (platform contract, `docs/`, test, `scripts/validate-harness.py`) and keep it short.
6. Run `make validate-harness` and `make test-harness`.

## Gotchas
- Do not add long prose to `AGENTS.md` for a one-off; it consumes always-loaded context.
- A rule the agent cannot verify is weak; prefer something a script can check.
- Record the failure even when the fix is "nothing, because...": the justification is data.
