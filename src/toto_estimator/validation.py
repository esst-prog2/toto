"""Shared input checks with exact integer conversion and source-row diagnostics."""

from decimal import Decimal, InvalidOperation
from numbers import Integral, Real

import pandas as pd

from .models import ValidationIssue

INT_MIN = -(2**63)
INT_MAX = 2**63 - 1


def frame_issues(frame: object, required: tuple[str, ...], name: str) -> list[ValidationIssue]:
    if not isinstance(frame, pd.DataFrame):
        return [ValidationIssue("invalid_type", f"{name} must be a pandas DataFrame.")]
    duplicates = frame.columns[frame.columns.duplicated()].tolist()
    if duplicates:
        return [ValidationIssue("duplicate_columns", f"{name} has duplicate columns: {duplicates}.")]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        return [ValidationIssue("missing_columns", f"{name} is missing required columns: {', '.join(missing)}.")]
    return []


def exact_integer(value: object) -> int:
    """Accept finite integral numbers/decimal strings representable as signed int64."""
    if isinstance(value, bool):
        raise ValueError("must be an integer, not a boolean")
    if isinstance(value, Integral):
        number = int(value)
    else:
        if isinstance(value, Decimal):
            decimal = value
        elif isinstance(value, str):
            try:
                decimal = Decimal(value.strip())
            except InvalidOperation as exc:
                raise ValueError("must be an integer") from exc
        elif isinstance(value, Real):
            decimal = Decimal.from_float(float(value))
        else:
            raise ValueError("has an unsupported integer type")
        if not decimal.is_finite() or decimal != decimal.to_integral_value():
            raise ValueError("must be a finite integer")
        if not INT_MIN <= decimal <= INT_MAX:
            raise ValueError("must fit a signed 64-bit integer")
        number = int(decimal)
    if not INT_MIN <= number <= INT_MAX:
        raise ValueError("must fit a signed 64-bit integer")
    return number


def team_name(value: object) -> str | None:
    """Only nonblank strings are team names; never invent names from nulls/objects."""
    return value.strip() if isinstance(value, str) else None
