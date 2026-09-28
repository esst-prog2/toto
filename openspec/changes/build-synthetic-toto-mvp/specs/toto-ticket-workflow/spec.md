## Purpose

Provide a repeatable 13+1 ticket workflow that validates fourteen editable fixtures as one unit and coordinates predictions independently of the user interface.

## ADDED Requirements

### Requirement: Fixed sample ticket
The project SHALL provide `sample_ticket.csv` with columns `position`, `home_team`, and `away_team` and exactly these fixtures: 1 Team A-Team B; 2 Team C-Team A; 3 Team A-Team D; 4 Team E-Team A; 5 Team A-Team F; 6 Team B-Team C; 7 Team B-Team D; 8 Team B-Team E; 9 Team F-Team B; 10 Team C-Team D; 11 Team E-Team C; 12 Team F-Team C; 13 Team D-Team E; and 14 Team D-Team F. The omitted unordered pairing SHALL be Team E-Team F.

#### Scenario: Sample ticket is loaded
- **WHEN** the sample ticket file is loaded at startup
- **THEN** it provides the same fourteen ordered positions and fixtures on every application start

### Requirement: Sample ticket startup validation
The system SHALL validate the sample ticket file before creating an editable ticket, including its required columns and all ticket rules.

#### Scenario: Committed sample ticket is valid
- **WHEN** the application starts with the committed sample ticket
- **THEN** startup validation succeeds and the ticket can be copied for editing

#### Scenario: Sample ticket file is invalid
- **WHEN** the startup file violates its schema or a ticket rule
- **THEN** the system reports a startup data error and does not attempt prediction

### Requirement: Complete ticket validation
A valid ticket SHALL contain exactly fourteen unique positions, one through fourteen, and fourteen fixtures using known teams. Each fixture SHALL contain different home and away teams, and no unordered team pairing SHALL occur more than once. Teams MAY appear in multiple different fixtures.

#### Scenario: Ticket satisfies every rule
- **WHEN** all fourteen edited fixtures satisfy the complete ticket rules
- **THEN** ticket validation succeeds

#### Scenario: Ticket contains invalid fixtures
- **WHEN** one or more fixtures use the same team twice, use an unknown team, duplicate an unordered pair, or otherwise violate ticket structure
- **THEN** validation reports every affected position and explains the correction required

### Requirement: Atomic prediction workflow
The service workflow SHALL validate historical data, the complete ticket, team availability, and minimum history before returning predictions. If any ticket position is invalid or cannot be predicted, it SHALL return no fixture predictions; otherwise, it SHALL return predictions for all fourteen positions together in position order.

#### Scenario: One or more positions fail validation
- **WHEN** any ticket or prediction prerequisite fails
- **THEN** the workflow returns all applicable errors and no partial prediction set

#### Scenario: Entire ticket is valid and predictable
- **WHEN** all fourteen positions pass every validation and history requirement
- **THEN** the workflow returns fourteen ordered predictions with their rating details

### Requirement: Interface-independent orchestration
The application workflow SHALL be callable independently of Streamlit using only the historical dataset and ticket as application inputs.

#### Scenario: End-to-end workflow is called without a UI
- **WHEN** a caller submits the canonical history and sample ticket through the service boundary
- **THEN** it receives the same validation outcome and predictions that the Streamlit interface would present

