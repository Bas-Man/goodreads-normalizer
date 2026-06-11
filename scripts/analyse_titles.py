#!/usr/bin/env python3

import csv
import re
from collections import Counter
from pathlib import Path


def main() -> None:
    csv_path = Path("goodreads_library_export.csv")

    pattern_counts = Counter()

    titles_with_colon = []
    titles_with_parens = []
    titles_with_hash = []
    titles_with_book = []
    titles_with_volume = []

    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            title = row["Title"].strip()

            if ":" in title:
                titles_with_colon.append(title)
                pattern_counts["contains_colon"] += 1

            if "(" in title and ")" in title:
                titles_with_parens.append(title)
                pattern_counts["contains_parentheses"] += 1

            if "#" in title:
                titles_with_hash.append(title)
                pattern_counts["contains_hash"] += 1

            if re.search(r"\bBook\b", title, re.IGNORECASE):
                titles_with_book.append(title)
                pattern_counts["contains_book"] += 1

            if re.search(r"\bVolume\b|\bVol\.\b", title, re.IGNORECASE):
                titles_with_volume.append(title)
                pattern_counts["contains_volume"] += 1

    print("\n=== Pattern Counts ===")
    for name, count in pattern_counts.most_common():
        print(f"{name:25} {count}")

    print("\n=== Titles With Parentheses ===")
    for title in sorted(set(titles_with_parens)):
        print(title)

    print("\n=== Titles With Colon ===")
    for title in sorted(set(titles_with_colon)):
        print(title)

    print("\n=== Titles With # ===")
    for title in sorted(set(titles_with_hash)):
        print(title)

    print("\n=== Titles With 'Book' ===")
    for title in sorted(set(titles_with_book)):
        print(title)

    print("\n=== Titles With 'Volume' ===")
    for title in sorted(set(titles_with_volume)):
        print(title)


if __name__ == "__main__":
    main()