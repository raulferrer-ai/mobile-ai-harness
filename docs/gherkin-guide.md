# Gherkin Specification Guide - mobile-ai-harness

This guide provides detailed instructions for writing Gherkin feature specifications that drive the development of mobile features in this template. All features must have a Gherkin specification registered on the feature board before implementation begins.

## Gherkin Format Requirements

### Basic Structure
Every feature specification must follow this format:

```gherkin
Feature: < meaningful description of the feature >
  As a < user type >
  I want < goal >
  So that < benefit >

  Scenario: < descriptive scenario title >
    Given < pre-condition or initial state >
    And < another pre-condition >
    When < user action or system event >
    Then < expected result >
    And < another expected result >
```

### Mandatory Elements
1. **Feature keyword** followed by a colon and descriptive text
2. **At least one Scenario** with Given/When/Then steps
3. **No `@template-placeholder` markers** - the template must be completed, not copied
4. **Feature ID consistency**: The spec filename should match the feature ID in `feature_list.json`

### Scenario Requirements
- Each scenario must have at least one `Given`, `When`, and `Then` step
- Steps must be descriptive of the user behavior, not implementation details
- Use `And` to combine related steps when appropriate
- Scenarios should cover: happy path, error cases, empty states, and edge cases

### Example Feature Specification
```gherkin
Feature: Item list display
  As a registered user
  I want to view a list of items
  So that I can see available content

  Scenario: Items display successfully
    Given the user is authenticated
    And items exist in the backend
    When the user requests the item list
    Then the list is displayed with item count
    And each item shows title and description

  Scenario: Empty state when no items
    Given the user is authenticated
    And no items exist in the backend
    When the user requests the item list
    Then the empty state screen is displayed
    And the message "No items yet" is shown
    And a primary action "Add Item" is available

  Scenario: Error state when fetch fails
    Given the user is authenticated
    And the backend is temporarily unavailable
    When the user requests the item list
    Then the error state is displayed
    And the message "Unable to load items. Try again." is shown
    And a retry action is available
    And the retry action returns the user to the fetch attempt
```

## Step-Style Conventions

### Given Steps (Pre-conditions)
Describe the initial state of the system or user before the action:

- **Good**: "the user is authenticated", "items exist in the backend", "the user is on the item screen"
- **Bad**: "the button is tapped", "the network request is made" (these are When steps)
- **Tip**: Given steps set the scene; they rarely describe user actions

### When Steps (User Actions)
Describe the single event that triggers the behavior under test:

- **Good**: "the user requests the item list", "the user taps the retry button", "the network response returns"
- **Bad**: "the data appears", "the screen loads" (these are Then/expected results)
- **Tip**: One When step per scenario is ideal; multiple When steps should be OR-related, not sequential

### Then Steps (Expected Results)
Describe the observable outcome, using user-facing language:

- **Good**: "the list is displayed with item count", "the error message is shown", "the retry action is available"
- **Bad**: "the API returns 200", "the view model updates" (implementation details)
- **Tip**: Use user-facing language, not technical details; "Try again" not "Error 404"

### And Steps
- Combine related steps of the same type: "And the user is authenticated"
- Add additional expected results: "And the button is enabled"
- Avoid overuse; more than 3-4 `And` steps per scenario may indicate the scenario is doing too much

## Feature ID and Specification Filename

The specification filename must match the feature ID in `feature_list.json`:

```
feature_list.json feature ID:    sample-items
spec filename:                     features/01-sample-items.feature  (or features/sample-items.feature)
```

### Recommended Pattern
```
features/<two-digit-id>-<feature-id>.feature
```

Examples:
- `features/01-sample-items.feature`
- `features/02-user-authentication.feature`
- `features/15-payment-processing.feature`

## Validation Checks

### feature.py check
```bash
python3 scripts/feature.py check features/01-sample-items.feature
```
Output: "OK: spec for '01-sample-items' has Feature and Scenario(s)."

### Common Spec Errors
| Error | Cause | Fix |
| --- | --- | --- |
| "no 'Feature:' line" | Missing Feature keyword | Add `Feature:` at the top of the file |
| "no 'Scenario:' found" | Missing Scenario block | Add one or more Scenario blocks |
| "still contains '@template-placeholder'" | Template not completed | Remove or replace all `@template-placeholder` occurrences |
| "spec file not found: features/XX-feature.feature" | Wrong filename path | Ensure file exists at the specified path |
| "id must be kebab-case" | Feature ID not kebab-case | Rename to lowercase with hyphens (e.g., `my-feature`) |

### make validate-harness
Includes spec validation as part of the full harness validation. All spec errors must be fixed before gate passes.

## Multi-Scenario Features

Features may have multiple scenarios, each covering different paths:

```gherkin
Feature: User profile edit
  As a user
  I want to edit my profile
  So that I can update my information

  Scenario: Edit successfully
    Given the user is on their profile page
    When the user taps the edit button
    Then the edit form is displayed
    And the user updates the fields
    And the user taps save
    And the profile is updated

  Scenario: Edit cancelled
    Given the user is on their profile page
    When the user taps the edit button
    And the user taps the cancel button
    Then the edit form is closed
    And the profile is unchanged

  Scenario: Validation error
    Given the user is on the edit profile page
    When the user taps save without entering a name
    Then the validation error "Name is required" is shown
    And the profile is not updated
```

## Scenario Outline (Deprecated in favor of individual scenarios)

This template prefers individual `Scenario:` blocks over `Scenario Outline:` with Examples tables, because:
- Individual scenarios are easier to map to test cases
- Better readability for mobile feature specifications
- Clearer acceptance criteria per path
- `feature.py spec_errors` checks for `@template-placeholder` which works better with individual scenarios

If you use `Scenario Outline:`, ensure it does not contain `@template-placeholder` and that the feature passes `feature.py check`.

## Platform-Specific Considerations

### iOS Features
- Scenarios should test SwiftUI view behavior
- May test `@Observable` view model state transitions
- May include `#if DEBUG` seeding for UI test data
- Consider accessibility state in Given/Then steps

### Android Features
- Scenarios should test Compose screen behavior
- May test `StateFlow<UiState>` emissions
- May use Turbine for Flow assertions in tests
- Consider permission states (denied/restricted) in scenarios

## Tips for Good Gherkin Specs

1. **Keep scenarios independent**: Each scenario should be able to run without others
2. **Use business language**: "the user taps save" not "the save button sends a network request"
3. **One outcome per scenario**: If you need to test multiple outcomes, use separate scenarios
4. **Edge cases are scenarios too**: Empty state, error state, timeout, cancellation are all valid scenarios
5. **Review with the team**: Ensure all stakeholders understand the spec before implementation
6. **Update specs when behavior changes**: Treat specs as living documentation; update when behavior changes
7. **Avoid implementation details**: Specs should be writable by product managers, not just developers

## Failure to Specify

If a feature is started without a valid spec:
- `feature.py start <id>` will fail with spec validation errors
- The board will not allow starting a feature with a broken spec
- Fix the spec before starting, or use `feature.py block <id> --reason "..."` to block it

If a spec becomes invalid during implementation (e.g., behavior changes):
- Update the spec to match the new behavior
- The sensor will re-record; the gate may be invalidated if spec changes
- A human should verify the spec still matches the implemented behavior before closing