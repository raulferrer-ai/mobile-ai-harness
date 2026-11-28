# Bootstrap Guide - Getting Started with mobile-ai-harness

This guide walks through the initial setup and project creation process for the mobile-ai-harness template.

## Prerequisites

### Hardware
- **macOS** with Xcode 27+ for iOS development (required for iOS sensors and build)
- **Linux or macOS** with JDK 17+ for Android development (ANDROID_TEST_TASK sensor needs JDK per MIN_JDK in harness.env)
- **Intel or Apple Silicon** Mac (Apple Silicon recommended for Xcode 27)

### Software
- **Xcode 27+** (contains Swift 6.4, iOS 27 SDK)
  - Accept licenses: `sudo xcodebuild -runFirstLaunch`
- **Android Studio** Koala (2024) or newer
  - Contains Android SDK, build tools, emulator
  - AGP 9.x required for Compose 1.12+
- **Python 3.9+** (for harness scripts: `init.sh`, `feature.py`, `make` commands)
- **Git** (for version control)
- **Homebrew** (macOS package manager, recommended for tooling)

### Verification
Run `sh init.sh` to verify your environment and initialize the project state.

## Step 1: Initialize the Project

```bash
cd mobile-ai-harness
sh init.sh
```

### What init.sh Does
1. **Validates required tools**: Checks for `git`, `python3`, `xcodebuild` (on macOS), `java` (for Android)
2. **Creates missing state files**:
   - `progress/current.md` - Active feature and next step
   - `progress/log.md` - Delivery log with milestones
   - `progress/flywheel-log.md` - Deviations and rules
   - `feature_list.json` - Feature board (state machine)
3. **Validates harness structure**: Checks docs/, scripts/, .agents/ structure
4. **Scans for secrets**: Runs `scripts/scan-secrets.py`
5. **Prints status**: Toolchain availability, project name, feature board state
6. **Lists sensor availability**:
   - iOS: `xcodebuild present` (macOS only)
   - Android: `java present` (JDK needed for Gradle)

### Expected Output
```
Project: my-mobile-app
Board:   planned=0  in_progress=0  done=0  blocked=0

Active:  none. Board is empty. Write a spec (skill: feature-spec-writer), then:
         python3 scripts/feature.py add <id> "<title>" --spec features/01-sample-items.feature

Sensors available on this machine:
  ios:     xcodebuild present
  android: java present (gradlew is checked when the sensor runs)
```

## Step 2: Configure harness.env

Edit `harness.env` for your project-specific settings:

```bash
# Project name (appears in build outputs, CI, etc.)
PROJECT_NAME=my-mobile-app

# iOS configuration
IOS_DIR=ios
IOS_PROJECT=ios/App/App.xcodeproj     # Path to .xcodeproj directory
IOS_SCHEME=App                       # Xcode scheme name
IOS_DESTINATION="platform=iOS Simulator,name=iPhone 17 Pro"  # Sensor default
IOS_SENSOR_MODE=test                 # test | build (CI only)
IOS_CI_DESTINATION="generic/platform=iOS Simulator"        # CI build mode
IOS_LINT_CMD=                      # e.g., "swift format lint --strict --recursive ios"

# Android configuration
ANDROID_TEST_TASK=:app:testDebugUnitTest    # Gradle task for sensor
ANDROID_LINT_TASK=:app:lintDebug            # Gradle task for lint
MIN_JDK=17                                  # Minimum JDK major version

# Budget limits (max lines for agent instructions)
BUDGET_ROOT_AGENTS=150
BUDGET_PLATFORM_AGENTS=130
BUDGET_POINTER=15
BUDGET_SKILL=80
```

### Key Configuration Items

#### iOS
- **IOS_PROJECT**: Path relative to project root pointing to the `.xcodeproj` directory
- **IOS_SCHEME**: Must match an Xcode scheme in your project
- **IOS_DESTINATION**: Simulator name for sensor tests; format: `platform=iOS Simulator,name=<device>`
- **IOS_SENSOR_MODE**: 
  - `test`: Runs `xcodebuild test` (full sensor, counts as test execution)
  - `build`: Runs `xcodebuild build only` (degraded mode, recorded as such in gate)
- **IOS_CI_DESTINATION**: For CI build-only checks (no simulator name needed)

#### Android
- **ANDROID_TEST_TASK**: Gradle task for running JVM unit tests (typically `:app:testDebugUnitTest`)
- **ANDROID_LINT_TASK**: Gradle task for running Android Lint (typically `:app:lintDebug`)
- **MIN_JDK**: Minimum JDK major version required by your AGP; defaults to 17

## Step 3: Create Native Projects

### iOS Native Project
```bash
# The iOS project should already exist at ios/App/
# If starting from scratch, create via Xcode:
# 1. Open Xcode
# 2. Create a new "App" project (SwiftUI, Swift 6)
# 3. Name it per PROJECT_NAME in harness.env
# 4. Save at ios/App/

# Verify:
# - Swift language mode 6 is enabled
# - Deployment target matches docs/stack.md (default: iOS 26.0)
# - String Catalogs are enabled
# - AppContainer is set up in the composition root
# - Scheme name matches IOS_SCHEME in harness.env
```

### Android Native Project
```bash
# The Android project should already exist at android/app/
# If starting from scratch, create via Android Studio:
# 1. Open Android Studio
# 2. Create a new "Empty Views Activity" project (Compose-enabled)
# 3. Name it per PROJECT_NAME
# 4. Save at android/app/

# Verify:
# - Gradle Wrapper matches baseline (AGP 9.x, Kotlin 2.4.x)
# - minSdk = 26 (default per stack.md)
# - compileSdk/targetSdk at latest supported by toolchain
# - composeBOM 2026.09.00 (Compose 1.12.x stable)
# - AppContainer implemented in the Application class
```

## Step 4: Fill Product Documentation

### docs/product.md
Complete the product brief with your app's specifics:

1. **What it is**: One or two sentences describing the app and problem it solves
2. **Who it is for**: Primary user, context of use, technical comfort
3. **Principles**: 3-5 product principles (e.g., "calm over clever", "offline first")
4. **Tone of voice**: Examples of how the app speaks (good and bad)
5. **Languages**: Product copy language(s) and code identifier language
6. **Non-goals**: What this app deliberately does not do
7. **Success criteria**: How you will know the product works

### docs/design-system.md
Replace design tokens with your brand values:

1. **Color roles**: Replace the semantic color values with your brand colors (light/dark)
2. **Typography**: Map roles to your font families and sizes
3. **Spacing**: Customize the 4-pt grid values and screen horizontal padding
4. **Corner radius**: Replace small/medium/large/pill values
5. **Elevation**: Customize shadow settings
6. **Components**: Add your component catalog entries

## Step 5: Write Your First Feature Specification

### Create a Gherkin Spec
```bash
# Option A: Copy the template
cp templates/sample-feature/spec/01-sample-items.feature features/01-sample-items.feature

# Option B: Write from scratch using feature-spec-writer skill
# Create features/01-my-feature.feature with:
# - Feature: description
# - One or more Scenario blocks
# - No @template-placeholder markers
# - Following the Gherkin format
```

### Validate the Spec
```bash
python3 scripts/feature.py check features/01-my-feature.feature
# Or via make
make validate-harness  # includes spec validation
```

Expected: "OK: spec for '01-my-feature' has Feature and Scenario(s)."

## Step 6: Register and Start the Feature

```bash
# Register the feature on the board
python3 scripts/feature.py add sample-items "Sample Items" --spec features/01-sample-items.feature

# Start the feature (makes it in_progress)
python3 scripts/feature.py start sample-items

# Verify status
make status
# Should show: Active: sample-items - Sample Items with platforms=ios=pending, android=pending
```

## Step 7: Implement the Feature

### On iOS
1. Create `ios/Features/<Feature>/` directory structure
2. Implement domain models and repository protocols in `ios/Domain/`
3. Implement the view model in `ios/Features/<Feature>/<Feature>ViewModel.swift`
4. Implement the SwiftUI view in `ios/Features/<Feature>/<Feature>View.swift`
5. Add JVM-compatible fake repository for testing
6. Write Swift Testing unit tests
7. Write XCUITest UI tests (if applicable)

### On Android
1. Create `android/features/<feature>/` directory structure
2. Implement domain models and repository interfaces in `android/domain/`
3. Implement the ViewModel in `android/features/<feature>/<Feature>ViewModel.kt`
4. Implement the Compose screen in `android/features/<feature>/<Feature>Screen.kt`
5. Add small, stateless composables
6. Write JUnit + Turbine JVM unit tests
7. Write Compose UI tests with testTags (no Thread.sleep)

## Step 8: Run the Development Loop

### Single Platform
```bash
# iOS sensor (runs on simulator)
make sensor-ios

# Android sensor (JVM unit tests)
make sensor-android
```

### Both Platforms
```bash
make sensors  # Runs both sensor-ios and sensor-android
```

### Expected Sensor Results
- **Green**: All tests pass, sensor records `sensor_green` on the board
- **Red**: Some tests failed; fix the implementation and re-run
- **Degraded**: iOS build-only mode; recorded as degraded in the gate

### Record Gate (after both platforms green)
```bash
make gate
```

### Close Feature (human step)
```bash
# Human completes the dual checklist first, then:
python3 scripts/feature.py done sample-items --human-checklist-ok
```

## Step 9: Repeat for Additional Features

Each new feature follows the same loop:
1. Write spec in `features/`
2. Register with `feature.py add`
3. Start with `feature.py start`
4. Implement on targeted platforms
5. Run sensors `make sensor-ios && make sensor-android`
6. Complete dual checklist
7. Record gate `make gate`
8. Close with `feature.py done --human-checklist-ok`

Then start the next feature.

## Troubleshooting

### Common Issues

| Problem | Cause | Fix |
| --- | --- | --- |
| `make sensor-ios` fails with "scheme not found" | IOS_SCHEME mismatch in harness.env | Fix IOS_SCHEME in harness.env; run `xcodebuild -list` to see available schemes |
| `make sensor-android` fails with "task not found" | ANDROID_TEST_TASK mismatch | Fix ANDROID_TEST_TASK in harness.env; check Gradle task names |
| `make gate` fails - "no recorded gate" | Sensors not recorded on board | Ensure both `make sensor-ios && make sensor-android` ran successfully; sensors auto-record |
| "only one feature may be in_progress" | Another feature is already in_progress | Complete or block the current feature, then start the new one |
| Swift compilation errors | Version mismatch (Xcode/Swift/AGP) | Check version baseline in docs/stack.md; verify toolchain versions |
| "Duplicate id in feature_list.json" | Feature ID already exists | Use a different ID or check the board status |
| Tests fail on real device but pass on simulator | Device-specific issues | Verify the issue is not in the template; check device OS version, Xcode version |

### Need Help?
- Read `AGENTS.md` for platform-specific rules (`ios/AGENTS.md`, `android/AGENTS.md`)
- Check `docs/workflow.md` for the feature workflow graph
- Review `docs/architecture.md` for layered architecture principles
- Check `docs/decisions/` for architecture decision records
- Run `make validate-harness` for overall harness validation