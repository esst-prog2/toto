import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _verify(csv_path: Path, checksum_path: Path) -> bool:
    expected, filename = checksum_path.read_text(encoding="utf-8").strip().split(maxsplit=1)
    return filename == csv_path.name and hashlib.sha256(csv_path.read_bytes()).hexdigest() == expected


def test_canonical_csv_checksum_matches() -> None:
    assert _verify(
        PROJECT_ROOT / "data" / "historical_matches.csv",
        PROJECT_ROOT / "data" / "historical_matches.sha256",
    )


def test_checksum_detects_changed_bytes(tmp_path: Path) -> None:
    source_csv = PROJECT_ROOT / "data" / "historical_matches.csv"
    source_checksum = PROJECT_ROOT / "data" / "historical_matches.sha256"
    changed_csv = tmp_path / source_csv.name
    checksum = tmp_path / source_checksum.name
    changed_csv.write_bytes(source_csv.read_bytes() + b"\n")
    checksum.write_bytes(source_checksum.read_bytes())
    assert not _verify(changed_csv, checksum)

