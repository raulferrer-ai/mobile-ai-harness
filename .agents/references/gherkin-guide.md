# Gherkin guide for feature specs

Specs are the contract both platforms implement. Skill: `feature-spec-writer`. Template: `features/00-template.feature`.

## Style rules
- **Declarative, not procedural.** Describe behaviour, not taps ("the user adds a plant", not "taps the + button at the top right").
- **One behaviour per scenario**, 3-7 steps each. If it needs more, split it.
- **User language.** No class, screen-id or database words in steps.
- **Cover the unhappy paths:** validation, empty, error, denied permission, offline, interrupted flow.
- **Be concrete with data** using `Scenario Outline` + `Examples` when rules depend on values (thresholds, dates).
- **State copy intent, not final strings**, unless the exact text matters; exact strings live in localization files.
- **No invented requirements.** If it is not in the spec it is not in scope; ask the human to extend the spec first.
- **Tag platform-specific behaviour**: `@ios`, `@android`; log the reason in `docs/parity-matrix.md`.
- **Accessibility scenario** when the feature adds interactive UI (labels, text scaling).

## File naming
`features/NN-kebab-id.feature` with NN the priority order; the board id is the kebab part.

## Worked example
```gherkin
Feature: Add an item
  As a new user
  I want to add my first item quickly
  So that I can start using the app

  Background:
    Given the app is opened for the first time
    And no items exist

  Scenario: Add an item with a name
    When the user chooses to add an item
    And enters the name "Reading list"
    And confirms
    Then the item is saved locally
    And the user sees it in the list

  Scenario: Cancel adding an item
    Given the user is adding an item
    When the user cancels
    Then nothing is saved
    And the user returns to the previous screen

  Scenario Outline: Reject invalid names
    When the user tries to save an item named "<name>"
    Then saving is not allowed
    And a clear, calm message explains why

    Examples:
      | name |
      |      |
      | " "  |

  Scenario: Storage fails while saving
    Given saving will fail
    When the user confirms a valid item
    Then the item is not shown as saved
    And the user is offered a way to try again
```

## Review checklist
Every scenario is observable and testable - happy path, validation, empty/error/denied covered - no UI
implementation details - consistent vocabulary with other specs - registered on the board.
