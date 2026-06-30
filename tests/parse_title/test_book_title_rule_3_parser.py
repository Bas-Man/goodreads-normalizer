from goodreads_normalizer.models.book import BookTitleData, Series
from goodreads_normalizer.parsers.book_title import parse_title

import pytest

"""
Test data for RULE_3: This tests the case where titles contain ":" also supports "#1-3" in title.
"""
TEST_TITLES = [
    (
        "Three Jack Reacher Novellas: Deep Down, Second Son, High Heat, and Jack Reacher's Rules",
        "Three Jack Reacher Novellas: Deep Down, Second Son, High Heat, and Jack Reacher's Rules",
        [],
    ),
    (
        "Three More Jack Reacher Novellas: Too Much Time, Small Wars, Not a Drill and Bonus Jack Reacher Stories (Jack Reacher, #18.5, 19.5, 21.5)",
        "Three More Jack Reacher Novellas: Too Much Time, Small Wars, Not a Drill and Bonus Jack Reacher Stories",
        [Series(name="Jack Reacher", numbers=["18.5", "19.5", "21.5"])],
    ),
    ("Threshold: Stories from Cradle", "Threshold: Stories from Cradle", []),
    (
        "Artorian's Archives Omnibus #1-3  (Artorian's Archives, #1-3)",
        "Artorian's Archives Omnibus #1-3",
        [Series(name="Artorian's Archives", numbers=["1", "3"])],
    ),
    (
        "Artorian's Archives Omnibus Vol. 2 (Artorian's Archives, #4-6)",
        "Artorian's Archives Omnibus Vol. 2",
        [Series(name="Artorian's Archives", numbers=["4", "6"])],
    ),
    ("Mother of Learning: ARC 1", "Mother of Learning: ARC 1", []),
]


@pytest.mark.parametrize("input_title, expected_title, expected_series", TEST_TITLES)
def test_parse_titles_only(
    input_title: str, expected_title: str, expected_series: list
):
    this_book: BookTitleData = parse_title(input_title)
    assert this_book.original_title == input_title
    assert this_book.title == expected_title
    assert this_book.series == expected_series
