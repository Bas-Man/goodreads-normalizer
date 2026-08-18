from goodreads_normalizer.exceptions.base import NoBookTitleError
from goodreads_normalizer.models.book_title import BookTitleData
from goodreads_normalizer.parsers.book_title import parse_title


def transform_book_title(raw_title: str) -> BookTitleData:
    if not raw_title or not raw_title.strip():
        raise NoBookTitleError()
    return parse_title(raw_title)
