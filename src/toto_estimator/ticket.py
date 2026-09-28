"""Complete-ticket validation for the fixed 13+1 workflow."""

from collections import defaultdict
from collections.abc import Iterable

import pandas as pd

from .config import TICKET_SIZE
from .data import TICKET_COLUMNS
from .models import ValidationIssue


def validate_ticket(
    ticket: pd.DataFrame, known_teams: Iterable[str]
) -> list[ValidationIssue]:
    known = set(known_teams)
    issues: list[ValidationIssue] = []
    missing = [column for column in TICKET_COLUMNS if column not in ticket.columns]
    if missing:
        return [
            ValidationIssue(
                "missing_columns",
                f"Ticket is missing required columns: {', '.join(missing)}.",
            )
        ]

    if len(ticket) != TICKET_SIZE:
        issues.append(
            ValidationIssue(
                "ticket_size",
                f"Ticket must contain exactly {TICKET_SIZE} fixtures; found {len(ticket)}.",
            )
        )

    parsed_positions = pd.to_numeric(ticket["position"], errors="coerce")
    integral = parsed_positions.notna() & (parsed_positions % 1 == 0)
    for index in ticket.index[~integral]:
        issues.append(
            ValidationIssue(
                "invalid_position",
                f"Ticket row {int(index) + 2} has a non-integer position.",
                row=int(index) + 2,
            )
        )

    valid_positions = parsed_positions[integral].astype(int)
    expected = set(range(1, TICKET_SIZE + 1))
    actual = set(valid_positions.tolist())
    if actual != expected or valid_positions.duplicated(keep=False).any():
        issues.append(
            ValidationIssue(
                "ticket_positions",
                f"Ticket positions must be unique and cover 1 through {TICKET_SIZE}.",
            )
        )

    pairs: dict[tuple[str, str], list[int]] = defaultdict(list)
    for ordinal, (_, row) in enumerate(ticket.iterrows(), start=1):
        raw_position = parsed_positions.iloc[ordinal - 1]
        position = int(raw_position) if pd.notna(raw_position) and raw_position % 1 == 0 else ordinal
        home = str(row["home_team"]).strip()
        away = str(row["away_team"]).strip()
        if not home:
            issues.append(
                ValidationIssue(
                    "blank_home_team",
                    f"Position {position}: choose a home team.",
                    position=position,
                )
            )
        elif home not in known:
            issues.append(
                ValidationIssue(
                    "unknown_team",
                    f"Position {position}: home team {home} is not found in the historical data.",
                    position=position,
                )
            )
        if not away:
            issues.append(
                ValidationIssue(
                    "blank_away_team",
                    f"Position {position}: choose an away team.",
                    position=position,
                )
            )
        elif away not in known:
            issues.append(
                ValidationIssue(
                    "unknown_team",
                    f"Position {position}: away team {away} is not found in the historical data.",
                    position=position,
                )
            )
        if home and away and home == away:
            issues.append(
                ValidationIssue(
                    "identical_teams",
                    f"Position {position}: home and away teams must differ.",
                    position=position,
                )
            )
        elif home and away:
            pairs[tuple(sorted((home, away)))].append(position)

    for pair, positions in pairs.items():
        if len(positions) > 1:
            joined = ", ".join(str(position) for position in positions)
            for position in positions:
                issues.append(
                    ValidationIssue(
                        "duplicate_pair",
                        f"Position {position}: pairing {pair[0]}-{pair[1]} is duplicated at positions {joined}.",
                        position=position,
                    )
                )
    return issues

