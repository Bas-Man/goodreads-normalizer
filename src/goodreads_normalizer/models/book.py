"""
# Author: Bas-Man
# Created Date: 2025-6-24
# File: models/book.py
"""

import datetime

from pydantic import BaseModel, Field, computed_field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from goodreads_normalizer.models.author import Author
from goodreads_normalizer.models.book_title import BookTitleData, Series
from goodreads_normalizer.models.narrator import Narrator
from goodreads_normalizer.normalize.books import normalize_number
from goodreads_normalizer.transform.additional_author_field import (
    transform_author_additional_authors,
)
from goodreads_normalizer.transform.books import transform_book_title
from typing import Self


class Book(BaseModel):
    """
    This model stores all row data read from goodreads_export.csv file.
    As part of the book model creation. Validation and normalization is performed.

    BookTitleData:

        original_title (str):

        title (str): Book title only

        series (list[Series]): Series data for current Book.

    Attributes:
        book_id (str):
        title_data (BookTitleData):
        authors (list[Author]):
        narrators (list[Narrator]):
        isbn (str|None):
        isbn13 (str|None):
        rating (int):
        publisher (str):
        binding (str):
        pages (int):
        year_published (str):
        original_publication_year (str):
        date_read (datetime.date):
        date_added (datetime.date):
        book_shelves (list[str]):
        book_shelves_with_positions (list[str]):
        exclusive_shelf (str):
        my_review (str):
        spoiler (str):
        private_notes (str):
        read_count (int):
        owned_copies (int):
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

    @field_validator("rating", "pages", "owned_copies", mode="before")
    @classmethod
    def _normalize_rating_pages_owned(cls, raw_number: str) -> int:
        return normalize_number(raw_number)

    @field_validator("title_data", mode="before")
    @classmethod
    def _build_title_data(cls, raw_title: str) -> BookTitleData:
        return transform_book_title(raw_title)

    @field_validator("date_read", "date_added", mode="before")
    @classmethod
    def _parse_date(cls, date_str: str) -> datetime.date | None:
        if not date_str:
            return None
        try:
            return datetime.date.fromisoformat(str(date_str).replace("/", "-"))
        except ValueError:
            return None

    @field_validator("isbn", "isbn13", mode="before")
    @classmethod
    def _parse_isbn(cls, value: str) -> str | None:
        value = value.strip()
        if not value or (value == '=""' or value == '"="""""'):
            return None
        return str(value).strip("=")

    @field_validator("book_shelves", "book_shelves_with_positions", mode="before")
    @classmethod
    def _parse_book_shelves(cls, shelves: str) -> list[str]:
        """
        Converts the single string into its parts, creating a list of shelves

        Args:
            shelves (str):
        """
        if shelves is None or len(shelves) == 0:
            return []
        return shelves.split(", ")

    @field_validator("read_count")
    @classmethod
    def _adjust_read_count(cls, read_count: int, info: ValidationInfo) -> int:
        """
        If the book is on the "unable-to-finish" shelf, ensure that read_count is 0
        Goodreads csv export tends to set the read_count to 1 even of the book is not
        finished

        Args:
            read_count (int):
            info (str):

        Returns:
            int: The read_count for this book
        """
        shelf = info.data.get("exclusive_shelf")
        if shelf is None or shelf == "unable-to-finish":
            return 0
        return read_count

    @classmethod
    def create(
        cls,
        *,
        book_id: str,
        title: str,
        author: str | None = None,
        additional_authors: str | None = None,
        authors: list[Author] | list[str] | None = None,
        narrators: list[Narrator] | list[str] | None = None,
        isbn: str | None = None,
        isbn13: str | None = None,
        rating: int = 0,
        publisher: str = "",
        binding: str = "",
        pages: int = 0,
        year_published: str = "",
        original_publication_year: str = "",
        date_read: datetime.date | None = None,
        date_added: datetime.date | None = None,
        book_shelves: list[str] | None = None,
        book_shelves_with_positions: list[str] | None = None,
        exclusive_shelf: str = "to-read",
        my_review: str = "",
        spoiler: str = "",
        private_notes: str = "",
        read_count: int = 0,
        owned_copies: int = 1,
    ) -> Self:
        """
        Friendly factory for building a Book from ordinary Python values.

        Two ways to supply author/narrator data:

        1. Manual (authors=/narrators=): you've already decided who's an
           author and who's a narrator. Skips the CSV-style split logic.
        2. CSV-style (author=/additional_authors=): reproduces the exact
           same transform_author_additional_authors() split the Goodreads
           CSV path uses, based on `binding` (e.g. narrators get pulled
           out of "Additional Authors" for audiobook bindings).

        Mixing the two is not allowed — pick one.

        ```{python}
        from goodreads_normalizer import Book

        book = Book.create(book_id="123", title="He Who Fights with Monsters 12 (He Who Fights with Monsters #12)", author="Shirtaloon")
        print(f"Book Title: {book.title}")
        print(f"Series List: {book.series}")
        print(f"Author: {book.authors}")

        book2 = Book.create(book_id="456", title="Cleaning the Gold (Will Trent, #8.5; Jack Reacher, #23.6)",
                            authors=["Karin Slaughter", "Lee Child"])
        print(f"Book Title: {book2.title}")
        print(f"Author List: {book2.authors}")
        print(f"Series List: {book2.series}")
        ```
        """
        if (authors is not None or narrators is not None) and (
            author is not None or additional_authors is not None
        ):
            raise ValueError(
                "Provide either authors=/narrators= (manual) or "
                "author=/additional_authors= (CSV-style split), not both."
            )

        data: dict = {
            "book_id": book_id,
            "title_data": title,
            "isbn": isbn or "",
            "isbn13": isbn13 or "",
            "rating": rating,
            "publisher": publisher,
            "binding": binding,
            "pages": pages,
            "year_published": year_published,
            "original_publication_year": original_publication_year,
            "date_read": date_read,
            "date_added": date_added,
            "book_shelves": ", ".join(book_shelves) if book_shelves else "",
            "book_shelves_with_positions": (
                ", ".join(book_shelves_with_positions)
                if book_shelves_with_positions
                else ""
            ),
            "exclusive_shelf": exclusive_shelf,
            "my_review": my_review,
            "spoiler": spoiler,
            "private_notes": private_notes,
            "read_count": read_count,
            "owned_copies": owned_copies,
        }

        if author is not None or additional_authors is not None:
            # CSV-style: let _build_authors_narrators run the normal
            # transform_author_additional_authors split, same as a real row.
            data["Author"] = author or ""
            data["Additional Authors"] = additional_authors or ""
            data["Binding"] = binding
        else:
            # Manual: caller has already decided authors vs narrators.
            data["authors"] = [
                a if isinstance(a, Author) else Author(name=a) for a in (authors or [])
            ]
            data["narrators"] = [
                n if isinstance(n, Narrator) else Narrator(name=n)
                for n in (narrators or [])
            ]

        return cls.model_validate(data)

    @computed_field
    @property
    def title(self) -> str:
        """
        Gives the title of the book, excluding series name and position
        """
        return self.title_data.title

    @computed_field()
    @property
    def original_title(self) -> str:
        """
        Gives the original book title with additional spaces removed.
        """
        return self.title_data.original_title

    @computed_field()
    @property
    def series(self) -> list[Series]:
        """
        Gives access to the Series Model
        """
        return self.title_data.series

    @computed_field()
    @property
    def is_a_crossover(self) -> bool:
        """
        This is True if the book belongs to more than a single series.
        Example: "Cleaning the Gold" Belongs to both "Will Trent" and "Jack Reacher"
        """
        return self.title_data.is_a_crossover

    @computed_field()
    @property
    def is_series_collection(self) -> bool:
        """
        This is True if the book is a collection containing more than one book from a
        single series

        Note: Does not work for collection with multiple authors
        """
        return self.title_data.is_collection

    @computed_field()
    @property
    def is_single_book(self) -> bool:
        """
        This is True if the book is part of a single series and is not a collection.
        """
        return (
            len(self.title_data.series) == 1
            and len(self.title_data.series[0].numbers) == 1
        )

    @computed_field()
    @property
    def is_a_stand_alone_book(self) -> bool:
        """
        This is a standalone book. Does not belong to any series
        """
        return self.title_data.is_stand_alone
