"""Offline, value-redacting audit for the project's eight-column match CSV schema."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from datetime import date
from pathlib import Path

COLUMNS = (
    "match_id", "date", "league", "season", "home_team", "away_team",
    "home_goals", "away_goals",
)


def audit_csv_bytes(content: bytes, *, as_of: date) -> dict:
    """Check serialization, identities and completed-result fields without echoing rows.

    Seasons may be calendar years or consecutive cross-year seasons. Cross-year
    date windows follow this project's July–June convention. Source eligibility
    and historical adjudication require a separate provenance audit.
    """
    errors = []

    def issue(line: int, code: str, field: str = "") -> None:
        errors.append({"line": line, "code": code, "field": field})

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return {"rows": 0, "sha256": hashlib.sha256(content).hexdigest(),
                "errors": [{"line": 0, "code": "invalid_utf8", "field": ""}]}
    if content.startswith(b"\xef\xbb\xbf") or b"\r" in content or not content.endswith(b"\n"):
        issue(0, "noncanonical_serialization")
    try:
        parsed = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error:
        parsed = []
        issue(0, "invalid_csv")
    if not parsed or tuple(parsed[0]) != COLUMNS:
        issue(1, "wrong_schema")
        return {"rows": max(0, len(parsed) - 1), "sha256": hashlib.sha256(content).hexdigest(), "errors": errors}
    seen_ids = set()
    seen_keys = set()
    ordering = []
    for line, values in enumerate(parsed[1:], 2):
        if len(values) != len(COLUMNS):
            issue(line, "wrong_field_count")
            continue
        row = dict(zip(COLUMNS, values))
        for field in ("league", "home_team", "away_team"):
            if not row[field] or row[field] != row[field].strip():
                issue(line, "invalid_label", field)
        if row["home_team"] == row["away_team"]:
            issue(line, "same_team")
        try:
            day = date.fromisoformat(row["date"])
            if day.isoformat() != row["date"]:
                issue(line, "noncanonical_date", "date")
            if day > as_of:
                issue(line, "future_result", "date")
        except ValueError:
            day = None
            issue(line, "invalid_date", "date")
        season = re.fullmatch(r"([0-9]{4})(?:/([0-9]{4}))?", row["season"])
        if not season or not 1 <= int(season[1]) <= 9999 or (season[2] and int(season[2]) != int(season[1]) + 1):
            issue(line, "invalid_season", "season")
        elif day:
            start = int(season[1])
            if season[2]:
                in_window = date(start, 7, 1) <= day <= date(int(season[2]), 6, 30)
            else:
                in_window = day.year == start
            if not in_window:
                issue(line, "outside_season", "date")
        for field in ("home_goals", "away_goals"):
            if not re.fullmatch(r"0|[1-9][0-9]*", row[field]):
                issue(line, "invalid_goal", field)
        fields = [row[k] for k in ("league", "season", "date", "home_team", "away_team")]
        expected_id = hashlib.sha256(json.dumps(fields, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
        if row["match_id"] != expected_id:
            issue(line, "invalid_match_id", "match_id")
        key = tuple(fields)
        if row["match_id"] in seen_ids or key in seen_keys:
            issue(line, "duplicate_fixture")
        seen_ids.add(row["match_id"])
        seen_keys.add(key)
        ordering.append((row["league"], row["season"], row["date"], row["home_team"], row["away_team"]))
    if ordering != sorted(ordering):
        issue(0, "unsorted_rows")
    canonical = io.StringIO(newline="")
    csv.writer(canonical, lineterminator="\n").writerows(parsed)
    if canonical.getvalue().encode() != content:
        issue(0, "noncanonical_serialization")
    return {"rows": len(parsed) - 1, "sha256": hashlib.sha256(content).hexdigest(), "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--as-of", type=date.fromisoformat, required=True)
    args = parser.parse_args()
    result = audit_csv_bytes(args.path.read_bytes(), as_of=args.as_of)
    print(json.dumps(result, indent=2))
    return int(bool(result["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
