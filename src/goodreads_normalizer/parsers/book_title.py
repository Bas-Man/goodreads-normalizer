from goodreads_normalizer.models.book_title import Series, BookTitleData
from goodreads_normalizer.parsers import regex_patterns


def parse_title(title: str) -> BookTitleData:
    raw_title = title
    clean_title = title.strip().replace("‘", "'").replace("’", "'").replace(",", ",")
    # Put your patterns here in order of priority
    patterns = [
        regex_patterns.RULE_1,
        regex_patterns.RULE_2,
        regex_patterns.RULE_3,
        regex_patterns.RULE_4,
    ]

    for pattern in patterns:
        match = pattern.match(clean_title)
        series_list: list[Series] = []
        if match:
            groups = match.groupdict()
            title = str(groups["Title"]).strip()
            if groups.get("SN1"):
                series_list = _get_series(groups)
            return BookTitleData(
                original_title=" ".join(raw_title.split()),
                title=title,
                series=series_list,
            )
    raise ValueError(f"Could not parse book title: {raw_title!r}")


def _get_series(groups: dict[str, str]) -> list[Series]:
    series_list: list[Series] = []

    if groups.get("SN1"):
        if groups.get("SN1N"):
            numbers = _get_single_series_number(groups, group_key="SN1N")
        else:
            numbers = _get_series_numbers(groups)

        series_list.append(Series(name=str(groups.get("SN1")), numbers=numbers))
    if groups.get("SN2"):
        if groups.get("SN2N"):
            numbers = _get_single_series_number(groups, group_key="SN2N")
        else:
            numbers = _get_series_numbers(groups)
        series_list.append(Series(name=str(groups.get("SN2")), numbers=numbers))

    return series_list


def _get_series_numbers(groups: dict[str, str]) -> list[str]:
    series_numbers: list[str] = []
    for i in range(1, 4):
        numbers = str(groups.get(f"N{i}")).strip() if groups.get(f"N{i}") else []
        # Deal with "1-2" type numbers to create a list ["1, "2"]. List also returned for a single value
        # such as "1". But only do this if numbers is not an empty list[] because groups.get() was successful
        if isinstance(numbers, str):
            numbers = numbers.split("-")
            series_numbers = series_numbers + numbers

    return series_numbers


def _get_single_series_number(groups: dict[str, str], group_key: str) -> list[str]:
    numbers: list[str] = str(groups.get(group_key)).split()
    return numbers
