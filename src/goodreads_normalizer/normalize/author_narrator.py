def normalize_author_name(value: str | None) -> str:
    if value is None:
        return ""

    return " ".join(value.split()).strip()
