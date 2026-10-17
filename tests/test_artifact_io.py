from pathlib import Path

import pytest

from scripts.artifact_io import serialize_csv
from scripts.build_real_spike_dataset import write_artifacts
from scripts.generate_synthetic_history import write_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_csv_bytes_preserve_unicode_order_quoting_and_lf() -> None:
    assert serialize_csv(
        [{"away": "B", "home": "Á, FC"}], ("home", "away")
    ) == 'home,away\n"Á, FC",B\n'.encode("utf-8")


@pytest.mark.parametrize("kind", ["synthetic", "real"])
@pytest.mark.parametrize("existing_index", [0, 1])
def test_writers_protect_either_output_and_allow_explicit_force(
    tmp_path: Path, kind: str, existing_index: int
) -> None:
    output = tmp_path / "nested" / "matches.csv"
    companion = tmp_path / "evidence" / ("matches.sha256" if kind == "synthetic" else "report.json")
    paths = (output, companion)
    existing = paths[existing_index]
    existing.parent.mkdir(parents=True)
    existing.write_bytes(b"keep me")

    def write(force=False):
        if kind == "synthetic":
            write_dataset(output, companion, force=force)
        else:
            write_artifacts(PROJECT_ROOT / "data" / "football_data_raw", output, companion, force=force)

    with pytest.raises(FileExistsError, match="Refusing to overwrite"):
        write()
    assert existing.read_bytes() == b"keep me"
    assert not paths[1 - existing_index].exists()

    write(force=True)
    expected_csv = "historical_matches.csv" if kind == "synthetic" else "real_matches.csv"
    assert output.read_bytes() == (PROJECT_ROOT / "data" / expected_csv).read_bytes()
    assert companion.read_bytes() != b"keep me"


@pytest.mark.parametrize("kind", ["synthetic", "real"])
@pytest.mark.parametrize("force", [False, True])
@pytest.mark.parametrize("alias", ["identical", "relative", "symlink", "hardlink"])
def test_output_collisions_fail_before_writing(tmp_path, kind, force, alias):
    output = tmp_path / "output"
    other = output
    if alias == "relative":
        other = tmp_path / "missing-parent" / ".." / "output"
    if alias in ("symlink", "hardlink"):
        output.write_bytes(b"unchanged")
        other = tmp_path / "alias"
        if alias == "symlink":
            other.symlink_to(output)
        else:
            import os
            os.link(output, other)
    with pytest.raises(ValueError, match="distinct"):
        if kind == "synthetic":
            write_dataset(output, other, force=force)
        else:
            write_artifacts(PROJECT_ROOT / "data" / "football_data_raw", output, other, force=force)
    if output.exists():
        assert output.read_bytes() == b"unchanged"
    else:
        assert not (tmp_path / "missing-parent").exists()
