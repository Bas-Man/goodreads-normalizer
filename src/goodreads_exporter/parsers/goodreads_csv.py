# src/goodreads_exporter/parsers/goodreads_csv.py

import csv

from goodreads_exporter.models.book import Book
from goodreads_exporter.normalize.books import normalize_rating, normalize_author_name


def parse_goodreads_csv(file_obj) -> list[Book]:
    reader = csv.DictReader(file_obj)

    books = []

    for row in reader:
        books.append(
            Book(
                title=row["Title"],
                author=normalize_author_name(row["Author"]),
                rating=normalize_rating(row["My Rating"]),
                book_id=row["Book Id"]
            )
        )

    return books