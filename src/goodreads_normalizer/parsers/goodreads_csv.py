# src/goodreads_normalizer/parsers/goodreads_csv.py

import csv

from goodreads_normalizer.models.book import Book
from goodreads_normalizer.normalize.books import (
    normalize_rating,
    normalize_author_name,
    normalize_book_title,
)


def parse_goodreads_csv(file_obj) -> list[Book]:
    reader = csv.DictReader(file_obj)

    books = []

    for row in reader:
        books.append(
            Book(
                title_data=normalize_book_title(row["Title"]),
                author=normalize_author_name(row["Author"]),
                rating=normalize_rating(row["My Rating"]),
                book_id=row["Book Id"]
            )
        )

    return books