---
name: feature-spec-writer
description: Write or refine a Gherkin feature spec and register it on the board. Use when a feature has no spec, the spec is vague, or scope changes.
---

# Feature Spec Writer

## Summary
Produce a declarative, testable `.feature` file that both platforms implement identically in intent.

## When to use
- Creating a new feature, or turning a request into acceptance criteria.
- A scenario is ambiguous, missing unhappy paths, or the scope changed mid-feature.

## Steps
1. Read `docs/product.md` (scope, tone, non-goals) and `.agents/references/gherkin-guide.md`.
2. Copy `features/00-template.feature` to `features/NN-<kebab-id>.feature`; delete the `@template-placeholder` line.
3. Write the happy path, then validation, empty, error, denied-permission and cancel/interrupt scenarios.
4. Use `Scenario Outline` for rule-based data; tag `@ios`/`@android` only for real differences.
5. Ask the human to confirm ambiguous behaviour; do not guess.
6. Register: `python3 scripts/feature.py add <kebab-id> "<Title>" --spec features/NN-<kebab-id>.feature`.
7. Note any intentional platform difference in `docs/parity-matrix.md`.

## Gotchas
- Steps describe behaviour, never UI mechanics or code.
- If scope changes during implementation, stop and rewrite the spec before more code (human suspend point).
- Specs with the template marker or without scenarios fail validation.
