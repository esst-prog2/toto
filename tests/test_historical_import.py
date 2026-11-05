import csv
from dataclasses import replace
from pathlib import Path

import pytest

from toto_estimator.historical_import import (
    HistoricalSource, OUTPUT_COLUMNS, canonical_season, import_historical_csvs,
)
from toto_estimator.models import DataValidationError


def source_file(tmp_path, rows, headers=None, name="source.csv", **metadata):
    headers = headers or ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"]
    path = tmp_path / name
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)
    return HistoricalSource(path, "england.premier-league", **({"season": "1993/94"} | metadata))


@pytest.mark.parametrize("headers", [
    ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"],
    ["Date", "Home", "Away", "HG", "AG"],
])
def test_formats_and_raw_preservation(tmp_path, headers):
    source = source_file(tmp_path, [["14/08/93", " A ", "B", "2", "1"]], headers)
    before = source.path.read_bytes()
    result = import_historical_csvs([source])
    record = result.records[0]
    assert tuple(record) == OUTPUT_COLUMNS
    assert record | {"match_id": "ID"} == {
        "match_id": "ID", "date": "1993-08-14", "league": "england.premier-league",
        "season": "1993/1994", "home_team": "A", "away_team": "B",
        "home_goals": 2, "away_goals": 1,
    }
    assert source.path.read_bytes() == before
    assert result.summary == dict(total=1, accepted=1, rejected=0, duplicates=0, fixtures=0, conflicts=0)


@pytest.mark.parametrize("raw,season,expected", [
    ("14/08/1993", "1993-94", "1993-08-14"),
    ("01/01/00", "1999/00", "2000-01-01"),
    ("31/12/99", "1999/2000", "1999-12-31"),
    ("29/02/00", "2000", "2000-02-29"),
    ("01/01/69", "2069", "2069-01-01"),
])
def test_historical_dates_use_season_not_century_pivot(tmp_path, raw, season, expected):
    source = source_file(tmp_path, [[raw, "A", "B", 0, 0]], season=season)
    assert import_historical_csvs([source]).records[0]["date"] == expected


@pytest.mark.parametrize("home,away,category", [
    ("", "", "fixtures"), (" ", " ", "fixtures"),
    ("", "1", "rejected"), ("1", "", "rejected"),
    ("-1", "0", "rejected"), ("1.5", "0", "rejected"),
    ("NaN", "0", "rejected"), ("Infinity", "0", "rejected"),
    (str(2**63), "0", "rejected"), ("abc", "0", "rejected"),
    ("1.0", "0", "accepted"),
])
def test_missing_and_invalid_scores(tmp_path, home, away, category):
    source = source_file(tmp_path, [["14/08/93", "A", "B", home, away]])
    result = import_historical_csvs([source])
    assert result.summary[category] == 1
    if category != "accepted":
        assert result.issues[0].row == 2
        assert str(source.path) in result.issues[0].message


def test_duplicates_across_files_and_conflicts_quarantine_all_rows(tmp_path):
    row = ["14/08/93", "A", "B", 1, 0]
    a = source_file(tmp_path, [row, row])
    b = source_file(tmp_path, [row], name="other.csv")
    result = import_historical_csvs([a, b])
    assert result.summary["accepted"] == 1
    assert result.summary["duplicates"] == 2
    conflict = source_file(tmp_path, [["14/08/93", "A", "B", 2, 0]], name="conflict.csv")
    for sources in ([a, b, conflict], [conflict, b, a]):
        result = import_historical_csvs(sources)
        assert result.records == []
        assert result.summary == dict(total=4, accepted=0, rejected=4, duplicates=0, fixtures=0, conflicts=4)
        assert all(i.code == "conflicting_duplicate" for i in result.issues)
        assert "1-0" in result.issues[0].message and "2-0" in result.issues[0].message


def test_ids_and_order_are_deterministic_and_competitions_distinct(tmp_path):
    a = source_file(tmp_path, [["14/08/93", "A", "B", 1, 0]])
    b = source_file(tmp_path, [["15/08/93", "A", "B", 2, 0]], name="other.csv")
    first = import_historical_csvs([a, b]).records
    assert first == import_historical_csvs([b, a]).records
    assert first[0]["match_id"] == import_historical_csvs([a, a]).records[0]["match_id"]
    different = replace(a, league="england.championship")
    records = import_historical_csvs([a, different]).records
    assert len({r["match_id"] for r in records}) == 2
    changed_score = source_file(tmp_path, [["14/08/93", "A", "B", 3, 0]], name="corrected.csv")
    assert import_historical_csvs([changed_score]).records[0]["match_id"] == first[0]["match_id"]


def test_row_seasons_and_explicit_source_mapping(tmp_path):
    headers = ["Date", "Home", "Away", "HG", "AG", "Season", "Country", "League"]
    source = source_file(tmp_path, [
        ["14/08/2012", "A", "B", 1, 0, "2012", "Sweden", "Allsvenskan"],
        ["14/08/2013", "A", "B", 0, 0, "2013", "Sweden", "Allsvenskan"],
    ], headers, season=None, country="Sweden", source_league="Allsvenskan")
    result = import_historical_csvs([source])
    assert [r["season"] for r in result.records] == ["2012", "2013"]
    assert import_historical_csvs([replace(source, season="2012")]).summary["rejected"] == 1
    with pytest.raises(DataValidationError, match="source mapping"):
        import_historical_csvs([replace(source, country=None)])


def test_competition_mismatch_and_mapping_collision(tmp_path):
    source = source_file(tmp_path, [["14/08/93", "A", "B", 1, 0, "E1"]],
                         ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "Div"], division="E0")
    assert import_historical_csvs([source]).summary["rejected"] == 1
    with pytest.raises(DataValidationError, match="same league"):
        import_historical_csvs([source, replace(source, division="E1")])


@pytest.mark.parametrize("season", ["1993/95", "1993", "2026-26", "", "0000", "9999/00"])
def test_season_and_date_disagreement(tmp_path, season):
    source = source_file(tmp_path, [["14/08/94", "A", "B", 1, 0]], season=season)
    if season == "1993":
        assert import_historical_csvs([source]).summary["rejected"] == 1
    else:
        with pytest.raises(DataValidationError):
            import_historical_csvs([source])


@pytest.mark.parametrize("raw", ["31/02/93", "08/14/93", "1993-08-14", "", "14/08/92"])
def test_invalid_dates(tmp_path, raw):
    source = source_file(tmp_path, [[raw, "A", "B", 1, 0]])
    assert import_historical_csvs([source]).summary["rejected"] == 1


@pytest.mark.parametrize("text", [
    "", "garbage\n", "Date,HomeTeam,HomeTeam,FTHG,FTAG\n",
    'Date,HomeTeam,AwayTeam,FTHG,FTAG\n"unterminated',
])
def test_empty_and_structurally_malformed_files_fail(tmp_path, text):
    path = tmp_path / "bad.csv"
    path.write_text(text)
    with pytest.raises(DataValidationError, match="bad.csv"):
        import_historical_csvs([HistoricalSource(path, "explicit", "1993/94")])


def test_header_only_short_rows_and_historical_padding(tmp_path):
    source = source_file(tmp_path, [])
    assert import_historical_csvs([source]).summary["total"] == 0
    source = source_file(tmp_path, [["14/08/93", "A", "B", 1]])
    assert import_historical_csvs([source]).summary["rejected"] == 1
    source = source_file(tmp_path, [["14/08/93", "A", "B", 1, 0, "", ""]],
                         ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "", ""])
    assert import_historical_csvs([source]).summary["accepted"] == 1


@pytest.mark.parametrize("home,away,result", [("A", "A", "H"), ("", "B", "H"), ("A", "B", "A")])
def test_team_and_result_validation(tmp_path, home, away, result):
    source = source_file(tmp_path, [["14/08/93", home, away, 1, 0, result]],
                         ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
    assert import_historical_csvs([source]).summary["rejected"] == 1


def test_missing_file_encoding_metadata_and_result_without_goals(tmp_path):
    with pytest.raises(DataValidationError):
        import_historical_csvs([HistoricalSource(tmp_path / "missing.csv", "explicit", "1993")])
    source = source_file(tmp_path, [["14/08/93", "A", "B", "", "", "H"]],
                         ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
    assert import_historical_csvs([source]).summary["rejected"] == 1
    with pytest.raises(DataValidationError):
        import_historical_csvs([replace(source, season=None)])
    with pytest.raises(DataValidationError):
        import_historical_csvs([replace(source, league=" ")])
    source.path.write_bytes(b"\xff")
    with pytest.raises(DataValidationError):
        import_historical_csvs([source])


def test_existing_repository_samples_import_without_changing_homework_outputs():
    directory = Path(__file__).resolve().parents[1] / "data" / "football_data_raw"
    result = import_historical_csvs([
        HistoricalSource(directory / "E0_2223.csv", "england.premier-league", "2022/23", division="E0"),
        HistoricalSource(directory / "E1_2223.csv", "england.championship", "2022/23", division="E1"),
        HistoricalSource(directory / "E0_2324.csv", "england.premier-league", "2023/24", division="E0"),
    ])
    assert result.summary == dict(total=1312, accepted=1312, rejected=0, duplicates=0, fixtures=0, conflicts=0)


def test_season_spellings():
    assert canonical_season("1999-00") == canonical_season("1999/2000") == "1999/2000"
