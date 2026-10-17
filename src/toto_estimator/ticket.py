"""Complete-ticket validation for the fixed 13+1 workflow."""

from collections import defaultdict
from collections.abc import Iterable

import pandas as pd

from .config import TICKET_SIZE
from .data import normalize_ticket
from .models import DataValidationError, ValidationIssue
from .validation import exact_integer


def validate_ticket(ticket: pd.DataFrame, known_teams: Iterable[str]) -> list[ValidationIssue]:
    try:
        ticket = normalize_ticket(ticket)
    except DataValidationError as exc:
        return exc.issues
    known = set(known_teams)
    issues: list[ValidationIssue] = []
    if len(ticket) != TICKET_SIZE:
        issues.append(ValidationIssue("ticket_size", f"Ticket must contain exactly {TICKET_SIZE} fixtures; found {len(ticket)}."))
    positions: dict[int, list[int]] = defaultdict(list)
    pairs: dict[tuple[str, str], list[tuple[int | None, int]]] = defaultdict(list)
    for ordinal, row in enumerate(ticket.itertuples(index=False), start=1):
        source_row = ordinal + 1
        try:
            position = exact_integer(row.position)
        except ValueError as exc:
            position = None
            issues.append(ValidationIssue("invalid_position", f"position at ticket row {source_row} {exc}; received {row.position!r}.", row=source_row))
        if position is not None:
            positions[position].append(source_row)
            if not 1 <= position <= TICKET_SIZE:
                issues.append(ValidationIssue("ticket_positions", f"Ticket row {source_row}: position {position} is out of range; use 1 through {TICKET_SIZE}.", position=position, row=source_row))
        label = f"Position {position}" if position is not None else f"Ticket row {source_row}"
        for venue, team in (("home", row.home_team), ("away", row.away_team)):
            if not team:
                issues.append(ValidationIssue(f"blank_{venue}_team", f"{label}: choose a nonblank {venue} team name string (row {source_row}).", position=position, row=source_row))
            elif team not in known:
                issues.append(ValidationIssue("unknown_team", f"{label}: {venue} team {team} is not found in the historical data (row {source_row}).", position=position, row=source_row))
        home, away = row.home_team, row.away_team
        if home and home == away:
            issues.append(ValidationIssue("identical_teams", f"{label}: home and away teams must differ (row {source_row}).", position=position, row=source_row))
        elif home and away:
            pairs[tuple(sorted((home, away)))].append((position, source_row))
    missing = sorted(set(range(1, TICKET_SIZE + 1)) - positions.keys())
    if missing:
        issues.append(ValidationIssue("ticket_positions", f"Missing ticket positions: {', '.join(map(str, missing))}."))
    for position, rows in positions.items():
        if len(rows) > 1:
            for source_row in rows:
                issues.append(ValidationIssue("ticket_positions", f"Position {position} is duplicated at ticket rows {', '.join(map(str, rows))}.", position=position, row=source_row))
    for pair, entries in pairs.items():
        if len(entries) > 1:
            for position, source_row in entries:
                issues.append(ValidationIssue("duplicate_pair", f"Position {position} (row {source_row}): pairing {pair[0]}-{pair[1]} is duplicated at ticket rows {', '.join(str(r) for _, r in entries)}.", position=position, row=source_row))
    return issues
