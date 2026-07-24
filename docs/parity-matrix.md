# Parity matrix

Same behaviour and tone on both platforms; native idioms for the rest. This file has two parts: how concepts map
across platforms (so agents translate correctly) and a log of intentional differences (so nobody "fixes" them).

## 1. Concept mapping (defaults; update when you change the stack)
| Concept | iOS | Android |
| --- | --- | --- |
| UI toolkit | SwiftUI | Jetpack Compose |
| State holder | `@Observable` view model | `ViewModel` + `StateFlow<UiState>` |
| Navigation | `NavigationStack` | Navigation Compose |
| Local database | SwiftData | Room |
| Small settings | `UserDefaults` / `@AppStorage` | DataStore |
| Async | async/await, actors | Coroutines, Flow |
| Local notifications | `UNUserNotificationCenter` | `NotificationManager` + `AlarmManager`/`WorkManager` |
| Background work | `BGTaskScheduler` | `WorkManager` |
| Photo picking | `PhotosPicker` / camera | Photo Picker / camera intent |
| Permissions | Info.plist usage strings + runtime prompts | Manifest + runtime permissions |
| Localization | String Catalogs | `strings.xml` |
| Unit tests | Swift Testing | JUnit + Turbine |
| UI tests | XCUITest | Compose test rule |
| Design tokens | `DesignSystem/` | `designsystem/` |

## 2. Intentional differences log
Add a row whenever behaviour or UI intentionally differs. Include the reason; reference the spec if relevant.
| Date | Area | iOS | Android | Reason | Spec |
| --- | --- | --- | --- | --- | --- |
| _example_ | Back navigation | Swipe-back gesture | System back | Platform convention | - |

## 3. Feature parity
Status lives on the board (`make status`, `feature_list.json`). A feature is not done until each targeted
platform is `done`. If a feature intentionally ships on one platform only, say so in the spec and in the board
(`--platforms`), and log it above.
