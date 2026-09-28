## Purpose

Offer a small local interface for editing a complete Toto ticket, correcting validation problems, and viewing understandable predictions from the MVP service workflow.

## ADDED Requirements

### Requirement: Editable prefilled ticket
The Streamlit application SHALL start with an editable session copy of the validated sample ticket and SHALL provide home-team and away-team dropdowns for every one of its fourteen positions.

#### Scenario: Application starts a new session
- **WHEN** the application opens without existing ticket session state
- **THEN** all fourteen dropdown rows are prefilled from `sample_ticket.csv`

#### Scenario: User edits a fixture
- **WHEN** the user changes a home-team or away-team dropdown
- **THEN** the changed selection remains in the current session while the original CSV remains unchanged

#### Scenario: Application is restarted
- **WHEN** a new application session begins after restart
- **THEN** the dropdowns are restored from the original sample ticket rather than prior session edits

### Requirement: Atomic validation feedback
The interface SHALL preserve all current selections while displaying clear validation messages for every affected ticket position, and SHALL display no predictions until the complete ticket is valid and all fixtures are predictable.

#### Scenario: User submits an invalid ticket
- **WHEN** prediction is requested and one or more positions are invalid or lack sufficient history
- **THEN** all detected position-specific messages are shown, every current dropdown selection is preserved, and no prediction rows are shown

### Requirement: Complete prediction presentation
When the workflow succeeds, the interface SHALL display the fourteen fixtures and their `1`, `X`, or `2` predictions together in a readable table, with position 14 identifiable as the `+1` fixture.

#### Scenario: User submits a valid ticket
- **WHEN** prediction is requested for a valid and predictable ticket
- **THEN** one result table displays all fourteen positions, fixtures, and predictions in ticket order

### Requirement: Optional rating transparency
The interface SHALL provide an optional transparency section that displays each prediction's home rating, away rating, and rating difference without displaying hidden strengths or other generator-only parameters.

#### Scenario: User opens prediction details
- **WHEN** predictions are available and the transparency section is expanded
- **THEN** rating details for all fourteen fixtures are shown and no generator-only information is present

