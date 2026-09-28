#!/usr/bin/env python3
"""Generate the fixed synthetic history. Runtime code must not import this file."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
from datetime import date, timedelta
from pathlib import Path

import numpy as np

RANDOM_SEED = 20260927
BASE_EXPECTED_GOALS = 1.35
HOME_ADVANTAGE = 0.20
TEAMS = ("Team A", "Team B", "Team C", "Team D", "Team E", "Team F")
STRENGTHS = {
    "Team A": 0.35,
    "Team B": 0.20,
    "Team C": 0.08,
    "Team D": -0.05,
    "Team E": -0.18,
    "Team F": -0.32,
}
SEASONS = ("2020-21", "2021-22", "2022-23", "2023-24", "2024-25")
CSV_COLUMNS = (
    "season",
    "date",
    "home_team",
    "away_team",
    "home_goals",
    "away_goals",
)


def first_saturday_on_or_after_august_10(year: int) -> date:
    candidate = date(year, 8, 10)
    return candidate + timedelta(days=(5 - candidate.weekday()) % 7)


def first_half_schedule() -> list[list[tuple[str, str]]]:
    rotation = list(TEAMS)
    rounds: list[list[tuple[str, str]]] = []
    for _ in range(len(TEAMS) - 1):
        rounds.append(
            [(rotation[index], rotation[-index - 1]) for index in range(len(TEAMS) // 2)]
        )
        rotation = [rotation[0], rotation[-1], *rotation[1:-1]]
    return rounds


def full_season_schedule() -> list[list[tuple[str, str]]]:
    first_half = first_half_schedule()
    second_half = [
        [(away, home) for home, away in matchday] for matchday in first_half
    ]
    return first_half + second_half


def generate_records() -> list[dict[str, object]]:
    rng = np.random.Generator(np.random.PCG64(RANDOM_SEED))
    schedule = full_season_schedule()
    records: list[dict[str, object]] = []
    for season in SEASONS:
        start_year = int(season[:4])
        first_date = first_saturday_on_or_after_august_10(start_year)
        for matchday_index, fixtures in enumerate(schedule):
            match_date = first_date + timedelta(days=21 * matchday_index)
            for home_team, away_team in fixtures:
                home_rate = (
                    BASE_EXPECTED_GOALS
                    + STRENGTHS[home_team]
                    - STRENGTHS[away_team]
                    + HOME_ADVANTAGE
                )
                away_rate = (
                    BASE_EXPECTED_GOALS
                    + STRENGTHS[away_team]
                    - STRENGTHS[home_team]
                )
                home_goals = int(rng.poisson(home_rate))
                away_goals = int(rng.poisson(away_rate))
                records.append(
                    {
                        "season": season,
                        "date": match_date.isoformat(),
                        "home_team": home_team,
                        "away_team": away_team,
                        "home_goals": home_goals,
                        "away_goals": away_goals,
                    }
                )
    return records


def serialize_records(records: list[dict[str, object]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return buffer.getvalue().encode("utf-8")


def checksum_line(csv_bytes: bytes, filename: str) -> str:
    return f"{hashlib.sha256(csv_bytes).hexdigest()}  {filename}\n"


def write_dataset(output: Path, checksum: Path, force: bool = False) -> None:
    if not force:
        existing = [path for path in (output, checksum) if path.exists()]
        if existing:
            names = ", ".join(str(path) for path in existing)
            raise FileExistsError(f"Refusing to overwrite existing file(s): {names}")
    csv_bytes = serialize_records(generate_records())
    output.parent.mkdir(parents=True, exist_ok=True)
    checksum.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(csv_bytes)
    checksum.write_text(
        checksum_line(csv_bytes, output.name), encoding="utf-8", newline=""
    )


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "data" / "historical_matches.csv",
    )
    parser.add_argument(
        "--checksum",
        type=Path,
        default=project_root / "data" / "historical_matches.sha256",
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    write_dataset(args.output, args.checksum, force=args.force)


if __name__ == "__main__":
    main()

