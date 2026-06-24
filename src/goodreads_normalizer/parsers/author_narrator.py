from goodreads_normalizer.parsers.regex_patterns import ADDITIONAL_AUTHOR

def parse_additional_author(additional_author: str) -> list[str]:
    """
    This function parses the additional author field and returns it as a list.
    Args:
        additional_author (str):

    Returns:
        list[str]: List of additional author names for easier processing.
    """
    names: list[str] = additional_author.split(", ")
    # Filter out Editors and translators
    for name in names:
        match = ADDITIONAL_AUTHOR.match(name)
        if match.groupdict()["type"]:
            names.remove(name)
        elif match.groupdict()["narrator"]:
            names.remove(name)
            names.append(match.groupdict()["name"])
    return names