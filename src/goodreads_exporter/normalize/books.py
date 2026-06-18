# src/goodreads_exporter/normalize/books.py

def normalize_rating(value: str | None) -> int:
    if value is None:
        return 0

    value = value.strip()

    if not value:
        return 0

    try:
        return int(value)
    except ValueError:
        return 0

def normalize_author_name(value: str | None) -> str:
    if value is None:
        return ""

    return " ".join(value.split())

def normalize_book_title(value: str | None) -> str:
    pass