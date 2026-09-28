from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import pytest

from scripts.generate_synthetic_history import (
    SEASONS,
    TEAMS,
    checksum_line,
    generate_records,
    serialize_records,
    write_dataset,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_generation_is_reproducible() -> None:
    first = generate_records()
    second = generate_records()
    assert first == second
    assert serialize_records(first) == serialize_records(second)


def test_generated_history_invariants() -> None:
    records = generate_records()
    assert len(records) == 150
    assert {record["season"] for record in records} == set(SEASONS)
    assert {
        record["home_team"] for record in records
    } | {record["away_team"] for record in records} == set(TEAMS)

    season_counts = Counter(record["season"] for record in records)
    assert set(season_counts.values()) == {30}

    pair_counts: Counter[tuple[str, str]] = Counter()
    orientations: defaultdict[tuple[str, str], Counter[tuple[str, str]]] = defaultdict(Counter)
    for record in records:
        home = str(record["home_team"])
        away = str(record["away_team"])
        pair = tuple(sorted((home, away)))
        pair_counts[pair] += 1
        orientations[pair][(home, away)] += 1
    assert len(pair_counts) == 15
    assert set(pair_counts.values()) == {10}
    assert all(sorted(counts.values()) == [5, 5] for counts in orientations.values())


def test_dates_form_ten_three_week_matchdays_per_season() -> None:
    records = generate_records()
    starts = [date(2020, 8, 15), date(2021, 8, 14), date(2022, 8, 13), date(2023, 8, 12), date(2024, 8, 10)]
    for season, expected_start in zip(SEASONS, starts, strict=True):
        dates = [
            date.fromisoformat(str(record["date"]))
            for record in records
            if record["season"] == season
        ]
        unique_dates = list(dict.fromkeys(dates))
        assert len(unique_dates) == 10
        assert unique_dates[0] == expected_start
        assert all(dates.count(matchday) == 3 for matchday in unique_dates)
        assert all(
            (later - earlier).days == 21
            for earlier, later in zip(unique_dates, unique_dates[1:])
        )
    all_dates = [date.fromisoformat(str(record["date"])) for record in records]
    assert all_dates == sorted(all_dates)


def test_committed_csv_and_checksum_are_reproducible(tmp_path: Path) -> None:
    output = tmp_path / "historical_matches.csv"
    checksum = tmp_path / "historical_matches.sha256"
    write_dataset(output, checksum)
    committed = PROJECT_ROOT / "data" / "historical_matches.csv"
    committed_checksum = PROJECT_ROOT / "data" / "historical_matches.sha256"
    assert output.read_bytes() == committed.read_bytes()
    assert checksum.read_text(encoding="utf-8") == committed_checksum.read_text(
        encoding="utf-8"
    )
    assert checksum.read_text(encoding="utf-8") == checksum_line(
        output.read_bytes(), output.name
    )
    with pytest.raises(FileExistsError):
        write_dataset(output, checksum)
