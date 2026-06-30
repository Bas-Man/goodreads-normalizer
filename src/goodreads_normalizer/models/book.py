# src/goodreads_normalizer/models/book.py
import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from goodreads_normalizer.models.author import Author
from goodreads_normalizer.models.book_title import BookTitleData
from goodreads_normalizer.models.narrator import Narrator
from goodreads_normalizer.transform.additional_author_field import (
    transform_author_additional_authors,
)
from goodreads_normalizer.transform.books import transform_book_title


class Book(BaseModel):
    """
    This model stores row data from goodreads_export.csv file
    """

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

    @model_validator(mode="before")
    @classmethod
    def _build_authors_narrators(cls, data: dict) -> dict:
        if isinstance(data, dict) and "authors" not in data:
            authors, narrators = transform_author_additional_authors(
                data.get("Author", ""),
                data.get("Additional Authors", ""),
                data.get("Binding", ""),
            )
            data["authors"] = authors
            data["narrators"] = narrators
        return data

    @field_validator("title_data", mode="before")
    @classmethod
    def _build_title_data(cls, value: str) -> BookTitleData:
        return transform_book_title(value)

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
    def parse_book_shelves(cls, value: str) -> list[str]:
        """
        Converts the single string into its parts, creating a list of shelves

        Args:
            value (str):

        Returns:
            list[str]: The list of shelves associated with this book
        """
        if value is None or len(value) == 0:
            return []
        return value.split(", ")

    @field_validator("read_count")
    @classmethod
    def adjust_read_count(cls, value: int, info: ValidationInfo) -> int:
        """
        If the book is on the "unable-to-finish" shelf, ensure that read_count is 0
        Goodreads csv export tends to set the read_count to 1 even of the book is not finishedh

        Args:
            value (int):
            info (str):

        Returns:
            int: The read_count for this book
        """
        shelf = info.data.get("exclusive_shelf")
        if shelf is None or shelf == "unable-to-finish":
            return 0
        return value

    @property
    def title(self) -> str:
        """
        Returns: Normalized title of the book
            str:
        """
        return self.title_data.title

    @property
    def original_title(self) -> str:
        """
        Returns: Original title of the book
        """
        return self.title_data.original_title

    @property
    def series(self):
        """
        Gives access to the Series Object
        Returns: Series Object
        """
        return self.title_data.series

    @property
    def is_a_crossover(self) -> bool:
        """Belongs to multiple distinct series."""
        return len(self.title_data.series) > 1

    @property
    def is_series_collection(self) -> bool:
        """Belongs to 1 series, but spans multiple book numbers."""
        return (
            len(self.title_data.series) == 1
            and len(self.title_data.series[0].numbers) > 1
        )

    @property
    def is_single_book(self) -> bool:
        """Belongs to 1 series, and is just a single entry."""

        return (
            len(self.title_data.series) == 1
            and len(self.title_data.series[0].numbers) == 1
        )

    @property
    def is_a_stand_alone_book(self) -> bool:
        """Belongs to 0 series."""
        return len(self.title_data.series) == 0
