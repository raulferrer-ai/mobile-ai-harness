Feature: Sample items
  As a user
  I want to keep a simple list of items
  So that I can verify the app works end to end

  Background:
    Given the app is opened
    And no items exist yet

  Scenario: Empty list is explained
    When the user sees the items list
    Then an empty state explains that there are no items yet

  Scenario: Add an item
    When the user adds an item named "First item"
    Then the item appears in the list

  Scenario Outline: Reject a blank name
    When the user tries to add an item named "<name>"
    Then nothing is added
    And a calm message explains that a name is required

    Examples:
      | name |
      |      |
      | "  " |

  Scenario: Saving fails
    Given saving will fail
    When the user adds an item named "Second item"
    Then the item is not shown as added
    And the user sees a message and can try again
