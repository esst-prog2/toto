"""Canonical v2 match metadata, with explicit v1 adapter compatibility.

Neutrality describes the official competition format, never stadium location.
No prediction or feature behavior belongs in this module.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date
from numbers import Integral

LEGACY_COLUMNS = ("match_id", "date", "league", "season", "home_team", "away_team",
                  "home_goals", "away_goals")
CANONICAL_COLUMNS = LEGACY_COLUMNS + ("neutral_venue",)
SCHEMA_VERSION = 2


def canonical_match_id(league: str, season: str, day: str, home: str, away: str) -> str:
    """Existing identity algorithm; scores and neutrality never affect identity."""
    payload = json.dumps((league, season, day, home, away), ensure_ascii=False,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def neutral_value(value: object) -> int | None:
    """Strict wire values: 0, 1, empty or None. Booleans/floats are rejected."""
    if value is None or (isinstance(value, str) and value == ""):
        return None
    if isinstance(value, bool):
        raise ValueError("neutral_venue must be 0, 1 or missing")
    if isinstance(value, Integral) and value in (0, 1):
        return int(value)
    if isinstance(value, str) and value in ("0", "1"):
        return int(value)
    raise ValueError("neutral_venue must be 0, 1 or missing")


def validate_canonical_records(records, *, require_order=True):
    """Validate v2 fields/identity without changing their values or order."""
    seen = set()
    previous = None
    count = 0
    for row in records:
        if tuple(row) != CANONICAL_COLUMNS:
            raise ValueError("canonical v2 requires the ordered nine-column schema")
        for key in ("league", "season", "home_team", "away_team"):
            if not isinstance(row[key], str) or not row[key] or row[key].strip() != row[key]:
                raise ValueError("blank or unnormalized canonical identity: " + key)
        if row["home_team"] == row["away_team"]:
            raise ValueError("identical teams")
        day = date.fromisoformat(row["date"])
        if day.isoformat() != row["date"] or day.year not in [int(x) for x in row["season"].split("/")]:
            raise ValueError("noncanonical date or season membership")
        years = row["season"].split("/")
        if len(years) not in (1, 2) or any(len(x) != 4 for x in years) or (len(years) == 2 and int(years[1]) != int(years[0]) + 1):
            raise ValueError("noncanonical season")
        for key in ("home_goals", "away_goals"):
            value = row[key]
            if isinstance(value, bool) or not str(value).isascii() or not str(value).isdecimal() or str(int(value)) != str(value):
                raise ValueError("noncanonical nonnegative goals")
        neutral_value(row["neutral_venue"])
        identity = tuple(row[k] for k in ("league", "season", "date", "home_team", "away_team"))
        if row["match_id"] != canonical_match_id(*identity):
            raise ValueError("canonical identity mismatch")
        if row["match_id"] in seen:
            raise ValueError("duplicate canonical match")
        if require_order and previous is not None and identity < previous:
            raise ValueError("noncanonical ordering")
        seen.add(row["match_id"])
        previous = identity
        count += 1
    return count
