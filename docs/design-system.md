# Design system

> Template with sane defaults. **Replace the values marked CUSTOMIZE** with your brand. Both platforms implement
> the same *semantic* tokens in their `DesignSystem/` / `designsystem/` layer; widget trees may differ.
> Skill: `design-system-parity`. Intentional differences: `docs/parity-matrix.md`.

## Principles <!-- CUSTOMIZE -->
- Clear hierarchy, generous whitespace, one primary action per screen.
- Native feel first: follow Human Interface Guidelines on iOS and Material 3 on Android, adapted by these tokens.
- Calm states: empty, loading and error are designed screens, not afterthoughts.

## Color roles (semantic)
Define each role for light and dark. Values are examples. <!-- CUSTOMIZE -->
| Role | Meaning | Light | Dark |
| --- | --- | --- | --- |
| `primary` | Main actions, active states | #3F51B5 | #9FA8DA |
| `onPrimary` | Content on primary | #FFFFFF | #1A1C3A |
| `primarySoft` | Soft backgrounds, chips | #E8EAF6 | #2A2D52 |
| `background` | App background | #FAFAFA | #121212 |
| `surface` | Cards, sheets | #FFFFFF | #1E1E1E |
| `textPrimary` | Main text | #1C1B1F | #E6E1E5 |
| `textSecondary` | Supporting text | #49454F | #CAC4D0 |
| `success` / `warning` / `danger` | Status | #2E7D32 / #ED6C02 / #C62828 | lighter variants |

Rules: never hardcode color literals in features; contrast at least 4.5:1 for body text; never use color alone to convey status.

## Typography
Map roles to platform text styles so Dynamic Type / font scaling work.
| Role | iOS | Android (Material 3) |
| --- | --- | --- |
| `display` | `.largeTitle` | `displaySmall` |
| `title` | `.title2` | `titleLarge` |
| `headline` | `.headline` | `titleMedium` |
| `body` | `.body` | `bodyLarge` |
| `label` | `.subheadline` | `labelLarge` |
| `caption` | `.caption` | `bodySmall` |

## Spacing, shape, elevation
- Spacing scale (4-pt grid): 4, 8, 12, 16, 24, 32, 48. Screen horizontal padding: 16-20. <!-- CUSTOMIZE -->
- Corner radius: small 8, medium 12, large 20, pill = fully rounded. <!-- CUSTOMIZE -->
- Elevation: soft, diffuse shadows only; avoid hard shadows. <!-- CUSTOMIZE -->

## Components (catalog)
Add one line per component when it is created. Features compose these; they do not restyle them.
| Component | Purpose | Notes |
| --- | --- | --- |
| Primary / secondary button | Main and secondary actions | Minimum 44pt / 48dp touch target |
| Card | Group related content | Uses `surface`, medium/large radius |
| Chip / status badge | Compact status or filter | Color + text, never color alone |
| Empty state | No data yet | Icon/illustration, calm message, single action |
| Error state | Something failed | Plain-language message, retry action |
| Loading state | Waiting | Skeleton or progress, no blocking spinners for lists |

## Motion
Subtle and purposeful (appear, expand, confirm). Respect "reduce motion" settings on both platforms.

## Accessibility minimums
Labels on all interactive elements, text scales to the largest sizes without clipping, touch targets 44pt/48dp,
focus order matches visual order, no information conveyed only by color or motion.

## Copy
Voice and examples live in `docs/product.md`. All user-facing strings go through localization resources.
