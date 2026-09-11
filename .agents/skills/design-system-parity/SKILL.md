---
name: design-system-parity
description: Keep tokens, typography, spacing, states and components consistent across iOS and Android. Use when building UI components, themes or reviewing visual consistency.
---

# Design System Parity

## Summary
One visual language, implemented natively twice, with intentional differences recorded.

## When to use
- Adding or changing colors, type, spacing, components, or empty/loading/error states.
- Checking cross-platform consistency against `docs/design-system.md`.

## Steps
1. Check `docs/design-system.md` for an existing role/component before creating one.
2. Add new tokens or components to the design system layer of both platforms, using the same semantic names.
3. Use only tokens/components in features: no color, font-size or spacing literals.
4. Map domain states (status, empty, error) to the same visual meaning on both platforms.
5. Log intentional differences in `docs/parity-matrix.md` and new components in the catalog.

## Gotchas
- Identical widget trees are not the goal; identical meaning, hierarchy and tone are.
- Never convey status by color alone.
- A token used in only one place belongs in the feature until a second use appears.
