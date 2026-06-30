from goodreads_normalizer.models.book_title import BookTitleData
from goodreads_normalizer.parsers.book_title import parse_title


def transform_book_title(raw_title: str) -> BookTitleData:
    if not raw_title or not raw_title.strip():
        raise ValueError(f"Cannot parse book title from empty input: {raw_title!r}")
    return parse_title(raw_title)
