# src/goodreads_normalizer/parsers/goodreads_csv.py

import csv

from goodreads_normalizer.models.book import Book


def parse_goodreads_csv(file_obj) -> list[Book]:
    reader = csv.DictReader(file_obj)

    books = []

    for row in reader:
        books.append(Book.from_goodreads(row))

    # for row in reader:
    #    try:
    #       books.append(Book.from_goodreads(row))
    #    except Exception:
    #        print(row)
    #        raise
    return books
