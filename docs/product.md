# Product Brief - mobile-ai-harness

## What it is
This is a dual-native mobile application template designed for professional development of complex iOS and Android applications using a shared architecture, design system, and workflow. The template provides a complete, production-ready foundation that enables teams to build native mobile applications with consistent behavior, tone, and architecture across both platforms, while respecting each platform's native idioms.

The template implements:
- **Two native codebases, one product**: Separate iOS (SwiftUI) and Android (Jetpack Compose) codebases that share domain logic, design tokens, and behavioral specifications
- **Layered architecture**: Dependencies point inward (features → domain ← data), making the system testable and maintainable
- **Unidirectional data flow (UDF)**: UI renders state and emits events; only the state holder mutates state
- **Local-first by default**: The local store is the single source of truth; network syncs into it when needed
- **Explicit errors and states**: Every screen models loading, empty, content, and error states with no silent failures

## Who it is for
- **Primary users**: Professional mobile development teams building complex iOS and Android applications
- **Target projects**: Business apps, consumer apps, enterprise apps requiring native performance and platform-specific UX
- **Development teams**: Teams that need to maintain feature parity across iOS and Android while respecting native platform conventions
- **New team onboarding**: Teams needing a standardized starting point that follows best practices and organizational guidelines

## Platforms
- **iOS**: Swift 6, SwiftUI, Xcode 27+, iOS 26.0 deployment target
- **Android**: Kotlin 2.4.x, Gradle Kotlin DSL, Jetpack Compose 1.12+, minSdk 26, compileSdk/targetSdk latest supported by toolchain

## Principles (Product Design)
1. **Calm over clever**: Interfaces should be peaceful and predictable, not surprising or experimental
2. **Offline first**: The app functions correctly with minimal or no network connectivity; local data is primary
3. **One primary action per screen**: Each screen has a clear focus; secondary actions are subordinate
4. **Native feel first**: Follow Human Interface Guidelines on iOS and Material 3 on Android, adapted through shared design tokens
5. **Deterministic logic**: Business rules are unit-testable; time, randomness, and IDs are injected for testability
6. **Privacy by design**: No personal data in logs; minimal permissions; user control over data collection
7. **Accessibility as default**: All interactive elements have labels; Dynamic Type support; 48dp touch targets

## Tone of Voice
The app's communication style should be:
- **Human and direct**: Use simple, clear language; avoid corporate jargon
- **Calm and reassuring**: Error messages and empty states are supportive, not alarming
- **Consistent**: Same terminology and style across both platforms
- **Respectful**: Address users by their choices; never blame or confuse

### Good examples
- "No items yet" instead of "Data not found"
- "Try again" with a clear retry action instead of "Error 404"
- "Permissions needed" with context about why instead of generic system alerts

### Bad examples
- "Failed to fetch resource" (too technical)
- "Invalid input" without saying what's invalid
- System default alerts without app context

## Languages
- **Product copy language(s)**: English (all user-facing strings)
- **Code identifiers, comments, and commits**: English
- **Localization**: All user-facing strings must be externalized to platform resources (String Catalogs iOS, strings.xml Android). The app must support at least English and one additional language per market requirements.

## Non-Goals (Explicitly out of scope)
- Cross-platform frameworks (KMP, Flutter, React Native) - this is a native template only
- Backend services - the template is local-first by default; add backend adapters behind repository contracts when needed
- UIKit for iOS - SwiftUI is the default; UIKit via representables is an alternative documented elsewhere
- Game development or heavy graphics pipelines - the template is for standard business/consumer apps
- Wear OS, tvOS, or watchOS extensions - focus on iPhone and phone-form-factor Android devices only

## Success Criteria
The template is successful when:
1. **A new developer can onboard**: A professional iOS or Android developer, unfamiliar with the template, can understand the architecture, build the project, and create a new feature from scratch within 2 days
2. **Feature parity is achievable**: Complex features (forms, lists with CRUD, authentication flows, empty/loading/error states) can be implemented on both platforms with consistent behavior and tone
3. **Sensors pass cleanly**: `make sensor-ios` and `make sensor-android` both complete with green results for implemented features
4. **Gate passes**: `make gate` passes, indicating both platforms have recorded sensors and the human dual checklist is complete
5. **Design system compliance**: No hardcoded color, typography, or spacing literals in feature code; all values come from the DesignSystem layer
6. **Security compliance**: The project passes `make validate-harness`; no secrets in source; MASVS baseline requirements met
7. **Accessibility compliance**: All interactive elements have accessibility labels; the app supports Dynamic Type (iOS) and font scaling (Android) without clipping or breaking layout