import csv
import re
from collections import Counter
from pathlib import Path


PAREN_SERIES = re.compile(
    r"^(.*?)\s+\((.*?)\s+#(\d+(?:\.\d+)?)\)$"
)

COLON_BOOK_SERIES = re.compile(
    r"^(.*?):\s*(.*?),\s*Book\s*(\d+(?:\.\d+)?)$"
)


def classify_title(title: str) -> str:
    if PAREN_SERIES.match(title):
        return "PAREN_SERIES"

    if COLON_BOOK_SERIES.match(title):
        return "COLON_BOOK_SERIES"

    if "(" not in title and ":" not in title:
        return "PLAIN_TITLE"

    return "UNKNOWN"


def main() -> None:
    csv_path = Path("goodreads_library_export.csv")

    counts = Counter()
    unknown_titles = []

    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            title = row["Title"].strip()

            category = classify_title(title)

            counts[category] += 1

            if category == "UNKNOWN":
                unknown_titles.append(title)

    print("\n=== Categories ===")

    for category, count in counts.most_common():
        print(f"{category:20} {count}")

    print("\n=== UNKNOWN TITLES ===")

    for title in sorted(set(unknown_titles)):
        print(title)


if __name__ == "__main__":
    main()