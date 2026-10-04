#!/usr/bin/env python3
"""Build the reproducible Homework 4 real-data spike artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from toto_estimator.predictor import predict_fixture
from toto_estimator.statistics import calculate_team_statistics


@dataclass(frozen=True)
class SourceFile:
    filename: str
    season: str
    division: str
    role: str
    expected_rows: int
    url: str


SOURCES = (
    SourceFile(
        "E0_2223.csv",
        "2022-23",
        "E0",
        "fit",
        380,
        "https://www.football-data.co.uk/mmz4281/2223/E0.csv",
    ),
    SourceFile(
        "E1_2223.csv",
        "2022-23",
        "E1",
        "fit",
        552,
        "https://www.football-data.co.uk/mmz4281/2223/E1.csv",
    ),
    SourceFile(
        "E0_2324.csv",
        "2023-24",
        "E0",
        "evaluation",
        380,
        "https://www.football-data.co.uk/mmz4281/2324/E0.csv",
    ),
)

SOURCE_COLUMNS = (
    "Div",
    "Date",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR",
    "B365CH",
    "B365CD",
    "B365CA",
)
OUTPUT_COLUMNS = (
    "season",
    "date",
    "home_team",
    "away_team",
    "home_goals",
    "away_goals",
    "source_division",
    "dataset_role",
    "bookmaker_home_odds",
    "bookmaker_draw_odds",
    "bookmaker_away_odds",
)
ODDS_OUTCOMES = (
    ("bookmaker_home_odds", "1"),
    ("bookmaker_draw_odds", "X"),
    ("bookmaker_away_odds", "2"),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _integer(value: str, field: str, source: SourceFile, row_number: int) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(
            f"{source.filename} row {row_number}: {field} must be an integer."
        ) from exc
    if parsed < 0:
        raise ValueError(
            f"{source.filename} row {row_number}: {field} must not be negative."
        )
    return parsed


def _odds(value: str, field: str, source: SourceFile, row_number: int) -> str:
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(
            f"{source.filename} row {row_number}: {field} must be decimal odds."
        ) from exc
    if parsed <= 1:
        raise ValueError(
            f"{source.filename} row {row_number}: {field} must be greater than 1."
        )
    return str(parsed)


def _result(home_goals: int, away_goals: int) -> str:
    if home_goals > away_goals:
        return "1"
    if home_goals < away_goals:
        return "2"
    return "X"


def load_source(source_dir: Path, source: SourceFile) -> tuple[list[dict[str, object]], str]:
    path = source_dir / source.filename
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in SOURCE_COLUMNS if column not in (reader.fieldnames or ())]
        if missing:
            raise ValueError(f"{source.filename} is missing columns: {', '.join(missing)}.")
        source_rows = list(reader)

    if len(source_rows) != source.expected_rows:
        raise ValueError(
            f"{source.filename} has {len(source_rows)} rows; expected {source.expected_rows}."
        )

    records: list[dict[str, object]] = []
    for row_number, row in enumerate(source_rows, start=2):
        if row["Div"].strip() != source.division:
            raise ValueError(
                f"{source.filename} row {row_number}: expected division {source.division}."
            )
        try:
            match_date = datetime.strptime(row["Date"].strip(), "%d/%m/%Y").date()
        except ValueError as exc:
            raise ValueError(
                f"{source.filename} row {row_number}: Date must use DD/MM/YYYY."
            ) from exc
        home_team = row["HomeTeam"].strip()
        away_team = row["AwayTeam"].strip()
        if not home_team or not away_team or home_team == away_team:
            raise ValueError(
                f"{source.filename} row {row_number}: teams must be nonblank and distinct."
            )
        home_goals = _integer(row["FTHG"].strip(), "FTHG", source, row_number)
        away_goals = _integer(row["FTAG"].strip(), "FTAG", source, row_number)
        derived_result = _result(home_goals, away_goals)
        expected_ftr = {"1": "H", "X": "D", "2": "A"}[derived_result]
        if row["FTR"].strip() != expected_ftr:
            raise ValueError(
                f"{source.filename} row {row_number}: FTR does not agree with full-time goals."
            )
        records.append(
            {
                "season": source.season,
                "date": match_date.isoformat(),
                "home_team": home_team,
                "away_team": away_team,
                "home_goals": home_goals,
                "away_goals": away_goals,
                "source_division": source.division,
                "dataset_role": source.role,
                "bookmaker_home_odds": _odds(
                    row["B365CH"].strip(), "B365CH", source, row_number
                ),
                "bookmaker_draw_odds": _odds(
                    row["B365CD"].strip(), "B365CD", source, row_number
                ),
                "bookmaker_away_odds": _odds(
                    row["B365CA"].strip(), "B365CA", source, row_number
                ),
            }
        )
    return records, _sha256(path)


def build_records(source_dir: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    source_evidence: list[dict[str, object]] = []
    for source in SOURCES:
        source_records, digest = load_source(source_dir, source)
        records.extend(source_records)
        source_evidence.append(
            {
                "filename": source.filename,
                "url": source.url,
                "season": source.season,
                "division": source.division,
                "dataset_role": source.role,
                "rows": len(source_records),
                "sha256": digest,
            }
        )
    records.sort(
        key=lambda record: (
            str(record["date"]),
            str(record["source_division"]),
            str(record["home_team"]),
            str(record["away_team"]),
        )
    )
    return records, source_evidence


def serialize_records(records: list[dict[str, object]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return buffer.getvalue().encode("utf-8")


def _favourites(record: dict[str, object]) -> list[str]:
    priced_outcomes = [
        (Decimal(str(record[column])), outcome) for column, outcome in ODDS_OUTCOMES
    ]
    minimum = min(price for price, _ in priced_outcomes)
    return [outcome for price, outcome in priced_outcomes if price == minimum]


def held_out_evaluation(records: list[dict[str, object]]) -> dict[str, object]:
    fitting = [record for record in records if record["dataset_role"] == "fit"]
    evaluation = [
        record for record in records if record["dataset_role"] == "evaluation"
    ]
    fitting_frame = pd.DataFrame.from_records(fitting)
    statistics = calculate_team_statistics(fitting_frame)

    correct = 0
    always_one_correct = 0
    favourite_correct = 0
    calls: Counter[str] = Counter()
    for position, record in enumerate(evaluation, start=1):
        actual = _result(int(record["home_goals"]), int(record["away_goals"]))
        prediction = predict_fixture(
            statistics,
            position,
            str(record["home_team"]),
            str(record["away_team"]),
        ).prediction
        calls[prediction] += 1
        correct += prediction == actual
        always_one_correct += actual == "1"
        favourite_correct += actual in _favourites(record)

    rows = len(evaluation)
    return {
        "fitting_rows_used": len(fitting),
        "held_out_rows_used_for_fitting": 0,
        "held_out_matches_evaluated": rows,
        "correct_predictions": correct,
        "predictor_accuracy_percentage": round(100 * correct / rows, 6),
        "always_predict_1_correct": always_one_correct,
        "always_predict_1_accuracy_percentage": round(
            100 * always_one_correct / rows, 6
        ),
        "bookmaker_favourite_correct": favourite_correct,
        "bookmaker_favourite_accuracy_percentage": round(
            100 * favourite_correct / rows, 6
        ),
        "prediction_counts": {outcome: calls[outcome] for outcome in ("1", "X", "2")},
    }


def measurement_report(
    records: list[dict[str, object]], source_evidence: list[dict[str, object]]
) -> dict[str, object]:
    home_wins = 0
    favourite_wins = 0
    joint_favourites: list[dict[str, object]] = []
    for record in records:
        result = _result(int(record["home_goals"]), int(record["away_goals"]))
        home_wins += result == "1"
        favourites = _favourites(record)
        favourite_wins += result in favourites
        if len(favourites) > 1:
            joint_favourites.append(
                {
                    "season": record["season"],
                    "date": record["date"],
                    "division": record["source_division"],
                    "home_team": record["home_team"],
                    "away_team": record["away_team"],
                    "favourite_outcomes": favourites,
                    "actual_result": result,
                }
            )

    rows = len(records)
    return {
        "sources": source_evidence,
        "transformation": {
            "rows_loaded": rows,
            "fitting_rows": sum(record["dataset_role"] == "fit" for record in records),
            "evaluation_rows": sum(
                record["dataset_role"] == "evaluation" for record in records
            ),
            "ftr_rows_validated": rows,
            "output_columns": list(OUTPUT_COLUMNS),
        },
        "measurements": {
            "scope": "all loaded rows",
            "home_wins": home_wins,
            "home_win_percentage": round(100 * home_wins / rows, 6),
            "bookmaker_favourite_wins": favourite_wins,
            "bookmaker_favourite_win_percentage": round(
                100 * favourite_wins / rows, 6
            ),
            "bookmaker_favourite_rule": (
                "Minimum closing Bet365 decimal odds across 1/X/2; equal minima are "
                "joint favourites and win when the actual result is among them."
            ),
            "joint_favourite_rows": len(joint_favourites),
            "joint_favourites": joint_favourites,
        },
        "held_out_evaluation": held_out_evaluation(records),
    }


def serialize_report(report: dict[str, object]) -> bytes:
    return (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def write_artifacts(
    source_dir: Path, output: Path, report_path: Path, force: bool = False
) -> dict[str, object]:
    if not force:
        existing = [path for path in (output, report_path) if path.exists()]
        if existing:
            names = ", ".join(str(path) for path in existing)
            raise FileExistsError(f"Refusing to overwrite existing file(s): {names}")
    records, source_evidence = build_records(source_dir)
    report = measurement_report(records, source_evidence)
    output.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(serialize_records(records))
    report_path.write_bytes(serialize_report(report))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=PROJECT_ROOT / "data" / "football_data_raw",
    )
    parser.add_argument(
        "--output", type=Path, default=PROJECT_ROOT / "data" / "real_matches.csv"
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=PROJECT_ROOT / "data" / "real_spike_measurements.json",
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    report = write_artifacts(args.source_dir, args.output, args.report, args.force)
    print(json.dumps(report["transformation"], sort_keys=True))


if __name__ == "__main__":
    main()
