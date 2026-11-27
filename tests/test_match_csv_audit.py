"""Only invented fixtures are used in these publication-safe tests."""
import csv
import hashlib
import io
import json
from datetime import date

import pytest

from scripts.audit_match_csv import COLUMNS, audit_csv_bytes


def fixture(**changes):
    row = dict(date="2020-08-01", league="Synthetic League", season="2020/2021",
               home_team="Example Alpha", away_team="Example Beta", home_goals="2", away_goals="1")
    row.update(changes)
    row["match_id"] = hashlib.sha256(json.dumps(
        [row[k] for k in ("league", "season", "date", "home_team", "away_team")],
        ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
    return row


def encoded(rows):
    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return text.getvalue().encode()


def audit(content):
    return audit_csv_bytes(content, as_of=date(2021, 7, 1))


def test_valid_synthetic_csv():
    assert audit(encoded([fixture()]))["errors"] == []


@pytest.mark.parametrize("changes,code", [
    ({"date": "2022-08-01", "season": "2022/2023"}, "future_result"),
    ({"date": "2020-02-30"}, "invalid_date"),
    ({"date": "2019-08-01"}, "outside_season"),
    ({"season": "2020/2022"}, "invalid_season"),
    ({"home_goals": "-1"}, "invalid_goal"),
    ({"away_goals": ""}, "invalid_goal"),
    ({"home_goals": "01"}, "invalid_goal"),
    ({"away_team": "Example Alpha"}, "same_team"),
    ({"home_team": " Example Alpha"}, "invalid_label"),
])
def test_invalid_fields_are_detected_without_echoing_values(changes, code):
    result = audit(encoded([fixture(**changes)]))
    assert code in {e["code"] for e in result["errors"]}
    assert "Example" not in json.dumps(result)


def test_duplicate_fixture_and_wrong_id():
    row = fixture()
    assert "duplicate_fixture" in {e["code"] for e in audit(encoded([row, row]))["errors"]}
    row["match_id"] = "0" * 64
    assert "invalid_match_id" in {e["code"] for e in audit(encoded([row]))["errors"]}


@pytest.mark.parametrize("transform", [lambda b: b"\xef\xbb\xbf" + b, lambda b: b.replace(b"\n", b"\r\n"), lambda b: b.rstrip(b"\n")])
def test_noncanonical_bytes(transform):
    assert audit(transform(encoded([fixture()])))["errors"]


def test_header_empty_and_malformed_input():
    for data in (b"", b"wrong,header\n", b"\xff\n", b'"unterminated\n'):
        assert audit(data)["errors"]
    assert audit(encoded([]))["errors"] == []


def test_order_and_calendar_season():
    rows = [fixture(date="2020-08-02"), fixture()]
    assert "unsorted_rows" in {e["code"] for e in audit(encoded(rows))["errors"]}
    assert audit(encoded([fixture(season="2020")]))["errors"] == []
