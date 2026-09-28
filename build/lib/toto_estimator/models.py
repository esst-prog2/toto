"""Shared result types for validation and prediction workflows."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    position: int | None = None
    row: int | None = None


class DataValidationError(ValueError):
    """Raised when a public input file does not satisfy its schema."""

    def __init__(self, issues: list[ValidationIssue]):
        self.issues = issues
        super().__init__("; ".join(issue.message for issue in issues))


@dataclass(frozen=True)
class Prediction:
    position: int
    home_team: str
    away_team: str
    prediction: str
    home_rating: float
    away_rating: float
    rating_difference: float


@dataclass(frozen=True)
class WorkflowResult:
    errors: tuple[ValidationIssue, ...] = field(default_factory=tuple)
    predictions: tuple[Prediction, ...] = field(default_factory=tuple)

    @property
    def success(self) -> bool:
        return not self.errors and len(self.predictions) > 0

