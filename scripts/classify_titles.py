import csv
import re
from collections import Counter
from pathlib import Path

# This is the primary Patter that handles book numbers using the '#' character
# It should be run first
PATTERN_1 = re.compile(
    r"^(?P<Title>[\w\s',.:-]+?)(?:$|(?P<HasSeries>\s\()(?(HasSeries)(?:(?P<SeriesName>[\w\s'&:0-9-]+?)(?:(?:,?\s#|,?\sBook\s)(?P<SeriesNumber1>\w+(?:-\d)?(?:\.\d)?)?(?:(,\s(?P<SeriesNumber2>\d+(?:\.\d)?))?,\s(?P<SeriesNumber3>\d+(?:\.\d)?))?)?[)])))",
    flags=re.MULTILINE | re.IGNORECASE,
)
PATTERN_1_OLD = re.compile(
    r"^(?P<Title>[\w\s'.,-]+)(?P<HasSeries>\s\()(?(HasSeries)((?P<SeriesName>[\w\s'&:0-9-]+)((?:,)?\s#(?P<SeriesNumber1>\d+(\-\d)?(?:\.\d)?)?(,\s(?P<SeriesNumber2>\d+(?:\.\d)?),\s(?P<SeriesNumber3>\d+(?:\.\d)?))?)?[)])$|$)",
    flags=re.MULTILINE | re.IGNORECASE,
)

PATTERN_11 = re.compile(
    r"^(?P<Title>[\w\s'.,:-]+)(?P<HasSeries>\s\()(?(HasSeries)((?P<SeriesName>[\w\s'&:0-9-]+)((?:,)?\s#(?P<SeriesNumber1>\d+(\-\d)?(?:\.\d)?)?(,\s(?P<SeriesNumber2>\d+(?:\.\d)?),\s(?P<SeriesNumber3>\d+(?:\.\d)?))?)?[)])$|$)",
    flags=re.MULTILINE | re.IGNORECASE,
)

# Forgotten Realms:
FORGOTTEN_REALMS = re.compile(
    r"(?=.*\s\(Forgotten Realms)(?P<Title>[\w'\s]+)\s"
    r"\((?P<MainSeries>Forgotten\sRealms):\s(?P<SeriesOneName>[\w\s]+),\s#"
    r"(?P<SeriesOneNumber>\d)(?:;\s(?P<SeriesTwoName>[\w\s]+),\s#"
    r"(?P<SeriesTwoNumber>\d))?\)",
    flags=re.MULTILINE | re.IGNORECASE,
)

PATTERN_3 = re.compile(
    r"(?P<Title>.*) \((?P<SeriesOne>.*), #(?P<SeriesNumberOne>\d(?:.\d));\s(?P<SeriesTwo>.*),\s#(?P<SeriesNumberTwo>\d+(?:.\d+)?)\)",
    flags=re.MULTILINE | re.IGNORECASE,
)

PATTERN_4 = re.compile(
    r"^(?P<Title>[\w\s]+:{1}\sPublisher's Pack(?::\s|\s)(?:\d|[\w\s]+))(?:\s\((?P<SeriesName>[\w\s]+),|,)\s#(?P<SeriesNumber>\d-\d)",
    flags=re.MULTILINE | re.IGNORECASE,
)

PATTERN_5 = re.compile(
    r"^(?P<Title>[\w\s-]+):{1}\s(?P<SeriesName>['\w\s-]+)(?:$|,)(?:\sbook\s(?P<SeriesNumber>\d+))?$",
    flags=re.MULTILINE | re.IGNORECASE,
)

PATTERN_6 = re.compile(
    r"^(?!Path of the Dragon Mage)(?P<Title>[\w\s-]+):\s(?P<SeriesName>[\w\s',-]+?)(?=\s*,\s*book\b|\s+\d+$|\s*$)(?:(?:\s*,\s*book\s+|\s+)(?P<SeriesNumber>\d+))?$",
    flags=re.IGNORECASE | re.MULTILINE,
)

BOOK_NUMBER = re.compile(
    r"^(?!.*novellas)(?P<Title>.*):\s(books)?(?(2)\s|(?P<SeriesName>[\w\s,]+))"
    r"(?P<SeriesNumber1>\d+-\d+)?(?(4)|,\s)(book )?(?(5)(?P<SeriesNumber2>.*|)|#"
    r"(?P<SeriesNumber3>\d+(?:-\d+)?))",
    flags=re.IGNORECASE | re.MULTILINE,
)

# Collection Range 1-2, 3-4 and so on.
COLLECTION_RANGE = re.compile(
    r"^(?P<Title>[\w\s']+(?:[^(])+)[(](?P<SeriesTitle>[\w\s']+),\s#"
    r"(?P<SeriesNumber1>\d+(?:-|\.)\d)\)",
    flags=re.MULTILINE,
)

# Collection: Book with multiple stories and positions within the main Series
COLLECTION_NUMBER = re.compile(
    r"^(?P<Title>[\w\s']+(?:[^(])+)[(](?P<SeriesTitle>[\w\s']+),\s#"
    r"(?P<SeriesNumber1>\d+(?:-|.)\d),\s(?P<SeriesNumber2>\d+.\d)?(?:,\s"
    r"(?P<SeriesNumber3>\d+.\d)?)?[)]",
    flags=re.MULTILINE,
)

EXCEPTION_BOOK = re.compile(
    r"^(?!Path of the Dragon Mage)(?P<Title>[\w\s':-]+)\s\((?P<SeriesName>[\w\s',-]+),(\s#|\sbook\s)\w+(\)$|;\s(?P<SeriesName2>[\w\s]+),\s#(?P<SeriesNumber2>\w+)\)$)",
    flags=re.IGNORECASE | re.MULTILINE,
)

TITLE_ONLY = re.compile(r"^(?!.*[:#()]).*$", flags=re.IGNORECASE | re.MULTILINE)


def classify_title(title: str) -> str:

    #    if PATTERN_1.match(title):
    #    return "Pattern One"

    if PATTERN_1.match(title):
        return "Pattern 11"

    if FORGOTTEN_REALMS.match(title):
        return "Forgotten Realms"

    if PATTERN_3.match(title):
        return "Will Trent/Jack Reacher"

    if PATTERN_4.match(title):
        return "Publisher Pack"

    if PATTERN_5.match(title):
        return "Single : and Book"

    if PATTERN_6.match(title):
        return "Something"

    if BOOK_NUMBER.match(title):
        return "Book with Number"

    if COLLECTION_RANGE.match(title):
        return "Collection by Range"

    if COLLECTION_NUMBER.match(title):
        return "Collection #"

    if EXCEPTION_BOOK.match(title):
        return "Exception Books"

    if TITLE_ONLY.match(title):
        return "Title Only"

    return "UNKNOWN"


def main() -> None:
    csv_path = Path("goodreads_library_export.csv")

    counts = Counter()
    unknown_titles = []
    titles_only = []

    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        processed_rows: int = 0
        for row in reader:
            processed_rows += 1
            title = (
                row["Title"]
                .strip()
                .replace("‘", "'")
                .replace("’", "'")
                .replace(",", ",")
            )

            category = classify_title(title)

            counts[category] += 1

            if category == "UNKNOWN":
                unknown_titles.append(title)

            if category == "Title Only":
                titles_only.append(title)

    print(f"\nRows Processed: {processed_rows}")
    print("\n=== Categories ===")

    for category, count in counts.most_common():
        print(f"{category:20} {count}")

    # print("\n=== Titles Only ===")
    # for title in sorted(set(titles_only)):
    # print(title)

    print("\n=== UNKNOWN TITLES ===")

    for title in sorted(set(unknown_titles)):
        print(title)


if __name__ == "__main__":
    main()
