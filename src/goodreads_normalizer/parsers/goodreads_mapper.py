"""Map Goodreads data to Book model input."""

from collections.abc import Mapping
from typing import Any

type GoodreadsRow = Mapping[str, Any]
type BookInput = dict[str, Any]


class GoodreadsBookMapper:
    """Map Goodreads export rows into Book model input."""

    @staticmethod
    def to_book_input(row: GoodreadsRow) -> BookInput:
        """Return input suitable for Book.model_validate()."""
        return {
            **row,
            "book_id": row["Book Id"],
            "title_data": row["Title"],
            "isbn": row.get("ISBN", ""),
            "isbn13": row.get("ISBN13", ""),
            "rating": row["My Rating"],
            "publisher": row.get("Publisher", "Unknown"),
            "binding": row["Binding"],
            "pages": row.get("Pages", 0),
            "year_published": row.get("Year Published", ""),
            "original_publication_year": row.get("Original Publication Year", ""),
            "date_read": row.get("Date Read"),
            "date_added": row.get("Date Added"),
            "book_shelves": row.get("Bookshelves"),
            "book_shelves_with_positions": row.get("Bookshelves with positions"),
            "exclusive_shelf": row.get("Exclusive Shelf", ""),
            "my_review": row.get("My Review", ""),
            "spoiler": row.get("Spoiler", ""),
            "private_notes": row.get("Private Notes", ""),
            "read_count": row.get("Read Count", 0),
            "owned_copies": row.get("Owned Copies", 0),
        }
