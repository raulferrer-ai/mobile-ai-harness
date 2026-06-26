# @template-placeholder  <- delete this line when you copy the file; the validator rejects specs that still have it.
# Copy to features/NN-<kebab-id>.feature, then register it:
#   python3 scripts/feature.py add <kebab-id> "<Title>" --spec features/NN-<kebab-id>.feature
# Style guide: .agents/references/gherkin-guide.md
Feature: <Short feature name>
  As a <type of user>
  I want <capability>
  So that <benefit>

  Background:
    Given <shared starting state>

  Scenario: <Happy path>
    When <user action>
    Then <observable outcome>

  Scenario: <Validation or empty state>
    When <user action with missing or invalid input>
    Then <calm, clear feedback and nothing is saved>

  Scenario: <Error or denied permission>
    Given <failure condition>
    When <user action>
    Then <the user can understand what happened and recover>
