import csv
from collections import Counter
from pathlib import Path
from goodreads_normalizer.parsers.regex_patterns import RULE_1, RULE_2, RULE_3, RULE_4

# This is the primary Patter that handles book numbers using the '#' character
# It should be run first


def classify_title(title: str) -> str:
    if RULE_1.match(title):
        return "Rule 1"

    elif RULE_2.match(title):
        return "Rule 2"

    elif RULE_3.match(title):
        return "Rule 3"

    elif RULE_4.match(title):
        return "Rule 4"

    return "UNKNOWN"


def main() -> None:
    csv_path = Path("goodreads_library_export.csv")

    counts: Counter[str] = Counter()
    unknown_titles: list[str] = []
    titles_only: list[str] = []

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
