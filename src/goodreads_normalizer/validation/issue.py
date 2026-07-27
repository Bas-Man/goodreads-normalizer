from goodreads_normalizer.validation.serverity import Severity


class ValidationIssue:
    severity: Severity
    row_number: int
    book_id: str
    title: str
    message: str
    recommendation: str | None

    def __repr__(self) -> str:
        return f"Book({self.book_id}, {self.title})"

    def __str__(self) -> str:
        return f"Book({self.book_id}, {self.title})"
