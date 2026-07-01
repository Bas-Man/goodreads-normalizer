# src/goodreads_normalizer/normalize/books.py


def normalize_number(value: str | None) -> int:
    if value is None:
        return 0

    if not value:
        return 0

    try:
        return int(value)
    except ValueError:
        return 0
