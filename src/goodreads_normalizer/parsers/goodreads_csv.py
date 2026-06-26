# src/goodreads_normalizer/parsers/goodreads_csv.py

import csv

from goodreads_normalizer.models.book import Book
from goodreads_normalizer.normalize.books import (
    normalize_rating,
    normalize_book_title,
)
from goodreads_normalizer.normalize.author_narrator import normalize_author_name


def parse_goodreads_csv(file_obj) -> list[Book]:
    reader = csv.DictReader(file_obj)

    books = []

    for row in reader:
        # Get Authors
        # Get Additional_Authors/Narrators
        books.append(
            Book(
                book_id=row["Book Id"],
                title_data=normalize_book_title(row["Title"]),
                author=normalize_author_name(row["Author"]),
                isbn=row["ISBN"],
                isbn13=row["ISBN13"],
                rating=normalize_rating(row["My Rating"]),
                publisher=row["Publisher"],
                binding=row["Binding"],
                year_published=row["Year Published"],
            )
        )

    return books
