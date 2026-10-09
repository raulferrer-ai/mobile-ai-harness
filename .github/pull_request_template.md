## What and why
<!-- One paragraph. Link the spec: features/NN-<id>.feature -->

## Feature board
- [ ] Feature id: `<id>` - state changed only through `scripts/feature.py`
- [ ] Spec in `features/` matches the behaviour (no invented requirements)

## Verification (paste the output)
- [ ] `make validate-harness` green
- [ ] iOS sensor green (`make sensor-ios`)
- [ ] Android sensor green (`make sensor-android`)
- [ ] Gate passed (`make gate`)

## Dual checklist (human) - see `docs/dual-checklist.md`
- [ ] Same flows and acceptance intent on both platforms
- [ ] Empty / loading / error states and denied permissions checked
- [ ] Accessibility basics checked (screen reader labels, text scaling)
- [ ] Intentional platform differences logged in `docs/parity-matrix.md`

## AI assistance (see `docs/ai-governance.md`)
- [ ] No AI used, **or** tools and role stated: <!-- e.g. Claude Code wrote the view model; I reviewed and ran sensors -->
- [ ] Commits materially produced by an agent carry an `AI-Assisted:` trailer
- [ ] No confidential data was placed in prompts; no new dependency without a reason and license check
- [ ] Security/privacy impact considered (`docs/security.md`, `docs/privacy-compliance.md`); data inventory updated if data changed

## Harness feedback
- [ ] If the agent deviated from spec/rules, an entry exists in `progress/flywheel-log.md`
- [ ] `progress/current.md` and `progress/log.md` updated
