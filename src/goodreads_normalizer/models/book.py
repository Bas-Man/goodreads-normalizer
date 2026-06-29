# src/goodreads_normalizer/models/book.py
import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator
from goodreads_normalizer.models.author import Author
from goodreads_normalizer.models.narrator import Narrator


class Series(BaseModel):
    name: str
    numbers: list[str] = Field(default_factory=list)


class BookTitleData(BaseModel):
    title: str
    # A book can belong to 0, 1, or many series
    series: list[Series] = Field(default_factory=list)

    def is_a_crossover(self) -> bool:
        return len(self.series) > 0


class Book(BaseModel):
    book_id: str
    title_data: BookTitleData
    authors: list[Author] = Field(default_factory=list)
    narrators: list[Narrator] = Field(default_factory=list)
    isbn: str | None
    isbn13: str | None
    rating: int
    publisher: str
    binding: str
    pages: int
    year_published: str
    original_publication_year: str
    date_read: datetime.date | None = None
    date_added: datetime.date | None = None
    book_shelves: list[str] = []
    book_shelves_with_positions: list[str] = []
    exclusive_shelf: str
    my_review: str
    spoiler: str
    private_notes: str
    read_count: int
    owned_copies: int

    @field_validator("date_read", "date_added", mode="before")
    @classmethod
    def _parse_date(cls, value: Any) -> datetime.date | None:
        if not value:
            return None
        try:
            return datetime.date.fromisoformat(str(value).replace("/", "-"))
        except ValueError:
            return None

    @field_validator("isbn", "isbn13", mode="before")
    @classmethod
    def _parse_isbn(cls, value: Any) -> str | None:
        value = value.strip()
        if not value or (value == '=""' or value == '"="""""'):
            return None
        return str(value).strip("=")

    @field_validator("book_shelves", "book_shelves_with_positions", mode="before")
    @classmethod
    def _parse_book_shelves(cls, value: str) -> list[str]:
        if value is None or len(value) == 0:
            return []
        return value.split(", ")

    @property
    def title(self):
        return self.title_data.title

    @property
    def series(self):
        return self.title_data.series

    def is_a_crossover(self) -> bool:
        """Belongs to multiple distinct series."""
        return len(self.series) > 1

    def is_series_collection(self) -> bool:
        """Belongs to 1 series, but spans multiple book numbers."""

        return len(self.series) == 1 and len(self.series[0].numbers) > 1

    def is_single_book(self) -> bool:
        """Belongs to 1 series, and is just a single entry."""

        return len(self.series) == 1 and len(self.series[0].numbers) == 1

    def is_a_stand_alone_book(self) -> bool:
        """Belongs to 0 series."""
        return len(self.series) == 0
