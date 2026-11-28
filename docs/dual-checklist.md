# Dual Checklist - Feature Completion Across Platforms

This checklist is the human-verified step that closes a feature. It must be completed before running `feature.py done <id> --human-checklist-ok`. The purpose is to confirm that both platform implementations share the same behavior, tone, and acceptance intent, while respecting native platform conventions.

## How to Use
1. After both sensors are green and the gate is recorded, review this checklist
2. For each area, mark the status: ✅ (pass) or ❌ (fail)
3. If any item is ❌, the feature is not done; fix the implementation and re-run sensors
4. A human must review and accept the checklist before closing the feature
5. Record the completion date and any notes

## Behavior & Flow
| # | Area | iOS Implementation | Android Implementation | Status |
|---|---|---|---|---|
| 1 | **Main flow completes successfully** | User can complete the primary use case from start to finish | User can complete the primary use case from start to finish | |
| 2 | **Error scenarios handled** | Error states (network failure, validation, not found) show calm messages with retry/actions | Error states show calm messages with retry/actions | |
| 3 | **Empty state handled** | Empty state screen with message and optional action when no data | Empty state screen with message and optional action when no data | |
| 4 | **Loading state handled** | Skeleton or progress indicator during data fetch (no blocking spinners for lists) | Skeleton or progress indicator during data fetch (no blocking spinners for lists) | |
| 5 | **Navigation works** | Navigation stack behaves correctly (push/pop, typed paths) | Navigation Compose routes work correctly (navController, typed routes) | |
| 6 | **Platform back convention** | Swipe-back gesture or system back button works as expected | System back button/handleBackBehavior works as expected | |
| 7 | **State persistence** | UI state survives configuration changes (memory/Storage as appropriate) | UI state survives configuration changes (ViewModel-scoped) | |

## Tone & Copy
| # | Area | iOS Implementation | Android Implementation | Status |
|---|---|---|---|---|
| 8 | **Error message language** | Plain-language, user-friendly messages | Plain-language, user-friendly messages | |
| 9 | **Empty state copy** | Calm, helpful text with optional action | Calm, helpful text with optional action | |
| 10 | **Button labels** | Consistent verb+noun format (e.g., "Save", "Delete", "Retry") | Consistent verb+noun format | |
| 11 | **Progress indicators** | Descriptive text during async operations | Descriptive text during async operations | |
| 12 | **Permission requests** | Contextual explanation before prompt | Contextual explanation before prompt | |

## Appearance & Design System
| # | Area | iOS Implementation | Android Implementation | Status |
|---|---|---|---|---|
| 13 | **Primary color** | Uses DesignSystem `primary` token | Uses designsystem `primary` token | |
| 14 | **Text styles** | Uses mapped text styles (body, title, etc.) | Uses mapped text styles (bodyLarge, etc.) | |
| 15 | **Spacing** | Uses 4-pt grid values from DesignSystem | Uses 4-pt grid values from designsystem | |
| 16 | **Corner radius** | Uses semantic radii (small/medium/large/pill) | Uses semantic radii (small/medium/large/pill) | |
| 17 | **Elevation/shadows** | Soft, diffuse shadows only | Soft, diffuse shadows only | |
| 18 | **Touch targets** | Minimum 44pt on interactive elements | Minimum 48dp on interactive elements | |
| 19 | **Dark mode** | Adaptive colors for light/dark | Adaptive colors for light/dark | |

## Accessibility
| # | Area | iOS Implementation | Android Implementation | Status |
|---|---|---|---|---|
| 20 | **All interactive elements have labels** | Every button, link, form field has accessibilityLabel | Every button, link, form field has contentDescription/accessibilityLabel | |
| 21 | **Dynamic Type / font scaling** | Layout adjusts to largest accessibility sizes without clipping | Layout adjusts to largest font sizes without clipping | |
| 22 | **Contrast ratio** | Minimum 4.5:1 for body text (3:1 for large text) | Minimum 4.5:1 for body text (3:1 for large text) | |
| 23 | **Color is not sole meaning** | Status conveyed by color + text/icon | Status conveyed by color + text/icon | |
| 24 | **Focus order** | Visual order matches accessibility focus order | Visual order matches accessibility focus order | |
| 25 | **Reduce motion** | Respects reduced motion settings | Respects reduced motion settings | |

## Privacy & Permissions
| # | Area | iOS Implementation | Android Implementation | Status |
|---|---|---|---|---|
| 26 | **Permission rationale** | Usage strings in Info.plist; permission requested in context | Manifest permissions justified; in-app explanation before request | |
| 27 | **Denied/restricted handling** | Graceful fallback when permission denied | Graceful fallback when permission denied | |
| 28 | **Data collection inventory** | Matches privacy-compliance.md inventory | Matches privacy-compliance.md inventory | |
| 29 | **Privacy manifest** | PrivacyInfo.xcprivacy current and complete | Data safety form matches actual behavior | |

## Checklist Completion
- [ ] All above items reviewed and marked ✅ or ❌
- [ ] Any ❌ items have been fixed and re-verified via sensors
- [ ] Gate `make gate` has passed (recorded on board)
- [ ] Both sensors green (`sensor_green` on board for both platforms)
- [ ] Human has independently verified both implementations
- [ ] No unresolved flywheel deviations in `progress/flywheel-log.md`

**Sign-off**: ________________________ Date: ___________

**Feature ID**: ________________________