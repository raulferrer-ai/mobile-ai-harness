---
name: mobile-accessibility-localization
description: Make UI accessible and localizable on both platforms: labels, text scaling, touch targets, contrast, string resources. Use when building or reviewing screens and copy.
---

# Accessibility and Localization

## Summary
Accessible and translatable by default, checked as part of done.

## When to use
- Adding screens, components, copy, icons or images; reviewing a feature before the dual checklist.

## Steps
1. Give every interactive element an accessible label; mark decorative images as such.
2. Support the largest text sizes without clipping; use design-system text styles, not fixed sizes.
3. Keep touch targets at least 44pt (iOS) / 48dp (Android) and contrast at least 4.5:1 for body text.
4. Never rely on color or motion alone; honor reduce-motion.
5. Put every user-facing string in the platform's resources (String Catalog / `strings.xml`); use plural and format rules, not concatenation.
6. Expose stable identifiers for UI tests (accessibility id / test tag) without leaking them into labels.
7. Check with a screen reader and large text on both platforms during the dual checklist.

## Gotchas
- Hardcoded strings and string concatenation break translation.
- Layouts that assume short English text break in other languages.
- Copy tone follows `docs/product.md`.
