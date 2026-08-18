from goodreads_normalizer.data import AUTHORS, NARRATORS
from goodreads_normalizer.exceptions.base import NarratorAsAuthorError


def validate_author_name(name: str) -> str:
    if name in NARRATORS and name not in AUTHORS:
        raise NarratorAsAuthorError(name)

    return name
