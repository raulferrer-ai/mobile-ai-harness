---
name: workflow-validator
description: Audit finished work against the spec, architecture boundaries, states, accessibility and tests before the gate. Use before asking a human to close a feature.
---

# Workflow Validator

## Summary
Independent review: does the implementation demonstrably satisfy the spec and the contracts?

## When to use
- Both platforms are sensor-green and you are about to run the gate.
- Reviewing another agent's or person's change.

## Steps
1. Walk every scenario in the spec; point to the code and the test that covers each.
2. Check layer boundaries, error/empty/loading states, permission-denied paths and large files.
3. Check design-system use and accessibility basics (`mobile-accessibility-localization`).
4. Check security/privacy basics (`mobile-security-privacy`).
5. Run `make validate-harness` and `make gate`; read the output, do not assume.
6. Prepare the evidence for the human checklist (`docs/dual-checklist.md`): list gaps, parity differences, risks.

## Gotchas
- Never alter or delete tests to make checks pass.
- A feature is not verified if a sensor was skipped, partial or build-only; say so explicitly.
- Do not run `feature.py done`; closing is human-only.
