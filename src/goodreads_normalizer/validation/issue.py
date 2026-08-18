from dataclasses import dataclass

from goodreads_normalizer.data.types import GoodreadsRow
from goodreads_normalizer.exceptions.base import GoodreadsValidationError
from goodreads_normalizer.validation.severity import Severity


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    severity: Severity
    row_number: int
    book_id: str
    title: str | None
    message: str
    recommendation: str | None

    def __str__(self) -> str:
        return f"Book({self.book_id}, {self.title})"


def goodreads_validation_issue(
    *, row_number: int, row: GoodreadsRow, error: GoodreadsValidationError
) -> ValidationIssue:
    return ValidationIssue(
        row_number=row_number,
        severity=error.severity,
        book_id=row["Book Id"],
        title=row.get("Title", None),
        message=str(error),
        recommendation=error.recommendation,
    )
