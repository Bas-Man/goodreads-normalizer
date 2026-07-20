from goodreads_normalizer.data import AUTHORS, NARRATORS


def validate_author_name(name: str) -> str:
    if name in NARRATORS and name not in AUTHORS:
        raise ValueError(f"{name} is a known narrator")

    return name
