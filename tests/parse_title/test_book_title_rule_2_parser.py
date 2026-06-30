from goodreads_normalizer.models.book import BookTitleData, Series
from goodreads_normalizer.parsers.book_title import parse_title

import pytest

"""
Test data for RULE_1: This tests the case for the most common data returned by a goodreads export.
"""
TEST_TITLES = [
    (
        "Welcome to Hell: Tasmanian Special Forces Group, Book 1",
        "Welcome to Hell",
        [Series(name="Tasmanian Special Forces Group", numbers=["1"])],
    ),
    (
        "Werewolf Standoff!: A LitRPG Progression Fantasy: My Werewolf System, Book 6",
        "Werewolf Standoff!: A LitRPG Progression Fantasy",
        [Series(name="My Werewolf System", numbers=["6"])],
    ),
    (
        "The Solace of Hope: The Eternal Ephemera, Book Three)",
        "The Solace of Hope",
        [Series(name="The Eternal Ephemera", numbers=["Three"])],
    ),
]


@pytest.mark.parametrize("input_title, expected_title, expected_series", TEST_TITLES)
def test_parse_titles_only(
    input_title: str, expected_title: str, expected_series: list
):
    this_book: BookTitleData = parse_title(input_title)
    assert this_book.original_title == input_title
    assert this_book.title == expected_title
    assert this_book.series == expected_series
