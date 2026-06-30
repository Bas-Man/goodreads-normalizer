from goodreads_normalizer.models.book import BookTitleData
from goodreads_normalizer.parsers.book_title import parse_title


def transform_book_title(value: str) -> BookTitleData:
    return parse_title(value)
