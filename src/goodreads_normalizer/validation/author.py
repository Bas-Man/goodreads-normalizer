from goodreads_normalizer.data import NARRATORS
from goodreads_normalizer.data import AUTHORS


def validate_author_name(name: str) -> str:
    if name in NARRATORS and name not in AUTHORS:
        raise ValueError(f"{name} is a known narrator")

    return name
