from pathlib import Path

import scripts.build_real_spike_dataset as real_spike
from scripts.build_real_spike_dataset import (
    build_records,
    held_out_evaluation,
    measurement_report,
    serialize_records,
    serialize_report,
    write_artifacts,
)
from toto_estimator.data import load_historical_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "data" / "football_data_raw"


def test_sources_transform_and_validate_against_ftr() -> None:
    records, source_evidence = build_records(SOURCE_DIR)
    report = measurement_report(records, source_evidence)

    assert len(records) == 1312
    assert report["transformation"]["fitting_rows"] == 932
    assert report["transformation"]["evaluation_rows"] == 380
    assert report["transformation"]["ftr_rows_validated"] == 1312
    assert report["measurements"]["joint_favourite_rows"] == 11


def test_held_out_evaluation_uses_only_fitting_rows_and_has_exact_results() -> None:
    records, _ = build_records(SOURCE_DIR)

    evaluation = held_out_evaluation(records)

    assert evaluation == {
        "fitting_rows_used": 932,
        "held_out_rows_used_for_fitting": 0,
        "held_out_matches_evaluated": 380,
        "correct_predictions": 152,
        "predictor_accuracy_percentage": 40.0,
        "always_predict_1_correct": 175,
        "always_predict_1_accuracy_percentage": 46.052632,
        "bookmaker_favourite_correct": 227,
        "bookmaker_favourite_accuracy_percentage": 59.736842,
        "prediction_counts": {"1": 154, "X": 77, "2": 149},
    }


def test_held_out_rows_are_not_passed_to_statistics(monkeypatch) -> None:
    records, _ = build_records(SOURCE_DIR)
    original = real_spike.calculate_team_statistics
    captured: dict[str, object] = {}

    def capture_statistics(matches):
        captured["rows"] = len(matches)
        captured["roles"] = set(matches["dataset_role"])
        captured["seasons"] = set(matches["season"])
        return original(matches)

    monkeypatch.setattr(real_spike, "calculate_team_statistics", capture_statistics)
    held_out_evaluation(records)

    assert captured == {
        "rows": 932,
        "roles": {"fit"},
        "seasons": {"2022-23"},
    }


def test_real_csv_loads_through_existing_schema() -> None:
    frame = load_historical_data(PROJECT_ROOT / "data" / "real_matches.csv")

    assert len(frame) == 1312
    assert set(frame["season"]) == {"2022-23", "2023-24"}
    assert set(frame["result"]) == {"1", "X", "2"}


def test_committed_artifacts_are_reproducible(tmp_path: Path) -> None:
    output = tmp_path / "real_matches.csv"
    report_path = tmp_path / "real_spike_measurements.json"
    write_artifacts(SOURCE_DIR, output, report_path)

    records, evidence = build_records(SOURCE_DIR)
    assert output.read_bytes() == serialize_records(records)
    assert report_path.read_bytes() == serialize_report(measurement_report(records, evidence))
    assert output.read_bytes() == (PROJECT_ROOT / "data" / "real_matches.csv").read_bytes()
    assert report_path.read_bytes() == (
        PROJECT_ROOT / "data" / "real_spike_measurements.json"
    ).read_bytes()
