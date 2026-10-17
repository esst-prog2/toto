"""Shared deterministic serialization and overwrite policy for offline scripts."""

import csv
import io
from pathlib import Path
from collections.abc import Iterable, Mapping, Sequence


def serialize_csv(records: Iterable[Mapping[str, object]], columns: Sequence[str]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return buffer.getvalue().encode("utf-8")


def check_overwrite(paths: Sequence[Path], force: bool = False) -> None:
    for index, path in enumerate(paths):
        for other in paths[:index]:
            if path.resolve() == other.resolve() or (path.exists() and other.exists() and path.samefile(other)):
                raise ValueError(f"Output destinations must be distinct: {other} and {path}.")
    if not force:
        existing = [path for path in paths if path.exists()]
        if existing:
            names = ", ".join(str(path) for path in existing)
            raise FileExistsError(f"Refusing to overwrite existing file(s): {names}")


def ensure_parent_directories(paths: Sequence[Path]) -> None:
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
