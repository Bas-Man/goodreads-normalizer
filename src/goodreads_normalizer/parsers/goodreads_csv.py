# src/goodreads_normalizer/parsers/goodreads_csv.py

import csv

from goodreads_normalizer.models.book import Book
from goodreads_normalizer.normalize.books import (
    normalize_rating,
    normalize_book_title,
)
from goodreads_normalizer.transform.additional_author_field import (
    transform_author_additional_authors,
)


def parse_goodreads_csv(file_obj) -> list[Book]:
    reader = csv.DictReader(file_obj)

    books = []

    for row in reader:
        authors, narrators = transform_author_additional_authors(
            row["Author"], row["Additional Authors"], row["Binding"]
        )
        books.append(
            Book(
                book_id=row["Book Id"],
                title_data=normalize_book_title(row["Title"]),
                authors=authors,
                narrators=narrators,
                isbn=row.get("ISBN", ""),
                isbn13=row.get("ISBN13", ""),
                rating=normalize_rating(row["My Rating"]),
                publisher=row.get("Publisher", "Unknown"),
                binding=row["Binding"],
                pages=int(row.get("Pages", 0)),
                year_published=row.get("Year Published", ""),
                original_publication_year=row.get("Original Publication Year", ""),
                date_read=row.get("Date Read"),  # type: ignore
                date_added=row.get("Date Added"),  # type: ignore
                book_shelves=row.get("Bookshelves"),  # type: ignore
                book_shelves_with_positions=row.get("Bookshelves with positions"),  # type: ignore
                exclusive_shelf=row.get("Exclusive Shelf", ""),
                my_review=row.get("My Review", ""),
                spoiler=row.get("Spoiler", ""),
                private_notes=row.get("Private Notes", ""),
                read_count=int(row.get("Read Count", 0)),
                owned_copies=int(row.get("Owned Copies", 0)),
            )
        )

    return books
