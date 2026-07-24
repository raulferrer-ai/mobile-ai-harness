# Dual checklist (human)

Run this with both apps open side by side before closing a feature. It is a human suspend point:
agents may prepare the evidence, but a human decides. Paste the result in the PR.

## Behaviour
- [ ] Every scenario in the spec works on iOS and on Android
- [ ] Same flow, same order of steps, same outcome
- [ ] Validation and error messages say the same thing in the same tone

## States
- [ ] Empty, loading and error states exist and look intentional on both
- [ ] Offline / slow behaviour is acceptable
- [ ] Denied or restricted permissions have a usable fallback

## Quality
- [ ] Accessibility: screen reader labels, large text (largest size), touch targets, contrast
- [ ] Light and dark appearance; rotation or large screens if supported
- [ ] No debug UI, test data or secrets left behind; no personal data in logs
- [ ] Data created before this change (existing installs) still works (migrations)

## Parity and harness
- [ ] Intentional differences are logged in `docs/parity-matrix.md`
- [ ] Any agent deviation is in `progress/flywheel-log.md`
- [ ] `make gate` passed and is recorded on the board

When all boxes are checked, in your own terminal:
`python3 scripts/feature.py done <id> --human-checklist-ok`
