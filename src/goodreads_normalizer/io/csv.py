from enum import Enum
from pathlib import Path

from goodreads_normalizer import Book, Author, Narrator
from goodreads_normalizer.parsers.goodreads_csv import parse_goodreads_csv

import csv
from typer import FileTextWrite


class NameFormatter(str, Enum):
    """
    This Enum helps control the formatting of Narrator names.

    Attributes:
        name: Return Narrator name without any tag.
        short: Return Narrator name with (N) as the tag.
        long: Return Narrator name with (Narrator) tag.
    """

    name = "name"
    short = "name_with_short_tag"
    long = "name_with_long_tag"


class GoodreadsImportError(Exception):
    """Custom exception for fatal Goodreads CSV processing errors."""

    pass


def load_csv(file_path: Path) -> list[Book]:
    """
    Loads and parses a Goodreads CSV file return a list of Books

    Args:
        file_path: GoodReads source csv file

    Returns:
        list[Book]: A list of Book models

    Raises:
        GoodreadsImportError: If there is an issue reading the csv source data
    """
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            return parse_goodreads_csv(file)

    except FileNotFoundError as e:
        raise GoodreadsImportError(
            f"Fatal Error: The export file could not be found at '{file_path}'. "
            "Please check the path and try again."
        ) from e

    except PermissionError as e:
        raise GoodreadsImportError(
            f"Fatal Error: Permission denied for '{file_path}'. "
            "Make sure the file isn't open in Excel or locked by another app."
        ) from e

    except (OSError, IOError) as e:
        raise GoodreadsImportError(
            f"Fatal Error: A system error occurred while reading '{file_path}': {e}"
        ) from e


def additional_authors(
    authors: list[Author],
    additional_authors_list: list[Narrator],
    name_format: NameFormatter = NameFormatter.name,
) -> str:
    author_list: list[Author] = authors[1:]

    remaining_author_list: list[str] = []
    narrators_name_list: list[str] = []
    method_name = name_format.value

    if author_list:
        remaining_author_list = [author.name for author in author_list]
    if additional_authors_list:
        narrators_name_list = [
            getattr(narrator, method_name) for narrator in additional_authors_list
        ]

    names = remaining_author_list + narrators_name_list
    return f"{', '.join(names) if names else ''}"


def export_to_stream(
    books: list[Book], stream: FileTextWrite, name_format: NameFormatter
) -> None:
    """
    Writes the book data directly into an open file-like stream (file or stdout).

    Format is managed by [NameFormatter](`NameFormatter`).

    Args:
        books: List of books to export.
        stream: An open, writable file-like object (e.g. a file handle
            opened in text mode, or ``sys.stdout``) that the formatted
            book data is written to. The stream is not closed by this
            function.
        name_format: NameFormatter controlling how author and narrator names
            are rendered in the output.

    Returns:
        Data is written to `stream` as a side effect.
    """
    headers = [
        "Book Id",
        "Title",
        "Author",
        "Additional Authors",
        "ISBN",
        "ISBN13",
        "My Rating",
        "Publisher",
        "Year Published",
        "Original Publication Year",
        "Date Read",
        "Date Added",
        "Bookshelves",
        "Bookshelves with positions",
        "Exclusive Shelf",
        "My Review",
        "Spoiler",
        "Private Notes",
        "Read Count",
        "Owned Copies",
    ]

    # Notice we DO NOT use 'with open()' here because Typer handles the stream lifecycle
    writer = csv.DictWriter(stream, fieldnames=headers)
    writer.writeheader()

    for book in books:
        author_name = (
            book.authors[0].pen_name
            if book.authors[0].pen_name
            else book.authors[0].name
        )
        additional_author_names = additional_authors(
            book.authors, book.narrators, name_format
        )  # type: ignore[call-arg]
        row = {
            "Book Id": book.book_id,
            "Title": book.original_title,
            "Author": author_name,
            "Additional Authors": additional_author_names,
            "ISBN": book.isbn,
            "ISBN13": book.isbn13,
            "My Rating": book.rating,
            "Publisher": book.publisher,
            "Year Published": book.year_published,
            "Original Publication Year": book.original_publication_year,
            "Date Read": book.date_read,
            "Date Added": book.date_added,
            "Bookshelves": ", ".join(book.book_shelves),
            "Bookshelves with positions": ", ".join(book.book_shelves_with_positions),
            "Exclusive Shelf": book.exclusive_shelf,
            "My Review": book.my_review,
            "Spoiler": book.spoiler,
            "Private Notes": book.private_notes,
            "Read Count": book.read_count,
            "Owned Copies": book.owned_copies,
        }
        writer.writerow(row)
