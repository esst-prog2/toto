import csv
from dataclasses import replace

import pytest

from scripts.build_real_spike_dataset import SOURCE_COLUMNS, SOURCES, load_source


@pytest.fixture
def source(tmp_path):
    source = replace(SOURCES[0], expected_rows=1)
    row = dict(zip(SOURCE_COLUMNS, ["E0", "01/08/2022", "A", "B", "1", "0", "H", "2.0", "3.0", "4.0"]))
    return source, row


def write_source(tmp_path, source, row):
    with (tmp_path / source.filename).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SOURCE_COLUMNS)
        writer.writeheader()
        writer.writerow(row)


@pytest.mark.parametrize("odds", ["", "abc", "NaN", "sNaN", "Infinity", "-Infinity", "1", "0", "-2"])
@pytest.mark.parametrize("field", ["B365CH", "B365CD", "B365CA"])
def test_invalid_odds_have_full_source_context(tmp_path, source, odds, field):
    spec, row = source
    row[field] = odds
    write_source(tmp_path, spec, row)
    with pytest.raises(ValueError) as error:
        load_source(tmp_path, spec)
    message = str(error.value)
    assert spec.filename in message and "row 2" in message and field in message


@pytest.mark.parametrize("field", SOURCE_COLUMNS)
def test_missing_source_cells_have_context(tmp_path, source, field):
    spec, row = source
    row[field] = " "
    write_source(tmp_path, spec, row)
    with pytest.raises(ValueError) as error:
        load_source(tmp_path, spec)
    assert f"{spec.filename} row 2: {field}" in str(error.value)


def test_truncated_source_row_has_field_context(tmp_path, source):
    spec, row = source
    with (tmp_path / spec.filename).open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(SOURCE_COLUMNS)
        writer.writerow([row[k] for k in SOURCE_COLUMNS[:-1]])
    with pytest.raises(ValueError, match="row 2: B365CA"):
        load_source(tmp_path, spec)


@pytest.mark.parametrize("kind", ["duplicate", "extra", "encoding"])
def test_malformed_source_files(tmp_path, source, kind):
    spec, row = source
    path = tmp_path / spec.filename
    if kind == "encoding":
        path.write_bytes(b"\xff")
    else:
        with path.open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(list(SOURCE_COLUMNS) + (["FTHG"] if kind == "duplicate" else []))
            writer.writerow(list(row.values()) + ["1"])
    with pytest.raises(ValueError) as error:
        load_source(tmp_path, spec)
    assert spec.filename in str(error.value)


@pytest.mark.parametrize("value", ["-1", "1.5", str(2**63), "NaN"])
def test_source_goals_reject_invalid_numbers(tmp_path, source, value):
    spec, row = source
    row["FTHG"] = value
    write_source(tmp_path, spec, row)
    with pytest.raises(ValueError, match="row 2: FTHG"):
        load_source(tmp_path, spec)


def test_source_result_consistency_and_extra_columns(tmp_path, source):
    spec, row = source
    row["FTR"] = "A"
    write_source(tmp_path, spec, row)
    with pytest.raises(ValueError, match="FTR"):
        load_source(tmp_path, spec)
    row["FTR"] = "H"
    with (tmp_path / spec.filename).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[*SOURCE_COLUMNS, "extra"])
        writer.writeheader()
        writer.writerow(row | {"extra": "permitted"})
    records, _ = load_source(tmp_path, spec)
    assert records[0]["home_goals"] == 1
