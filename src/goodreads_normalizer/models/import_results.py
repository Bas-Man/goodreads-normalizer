from dataclasses import dataclass

from goodreads_normalizer.models.book import Book
from goodreads_normalizer.validation.issue import ValidationIssue


@dataclass
class ImportResult:
    books: list[Book]
    issues: list[ValidationIssue]
