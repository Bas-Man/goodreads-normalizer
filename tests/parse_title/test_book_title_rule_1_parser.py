from goodreads_normalizer.models.book import BookTitleData, Series
from goodreads_normalizer.parsers.book_title import parse_title

import pytest

"""
Test data for RULE_1: This tests the case for the most common data returned by a goodreads export.
"""
TEST_TITLES = [
    ( "All The Skills 5 (All The Skills #5)", "All The Skills 5", [Series(name="All The Skills", numbers=["5"])], ),
    ( "A Better World (Brilliance Saga, #2)", "A Better World", [Series(name="Brilliance Saga", numbers=["2"])], ),
    ( "Not a Drill (Jack Reacher, #18.5)", "Not a Drill", [Series(name="Jack Reacher", numbers=["18.5"])], ),
    ("Two Tales of the Iron Druid Chronicles (The Iron Druid Chronicles, #0.6, 3.5)", "Two Tales of the Iron Druid Chronicles", [Series(name="The Iron Druid Chronicles", numbers=["0.6", "3.5"])],),
    ("The Great Bazaar and Other Stories (Demon Cycle, #1.6)", "The Great Bazaar and Other Stories",[Series(name="Demon Cycle", numbers=["1.6"]) ]),
    ("Black Blade", "Black Blade", []),
    ("English Grammar Boot Camp", "English Grammar Boot Camp", []),
    ("Firstborn", "Firstborn", []),
    ("It", "It", []),
    ("James Moriarty, Consulting Criminal", "James Moriarty, Consulting Criminal", []),
    ("Middlebridge Mysteries", "Middlebridge Mysteries", []),
    ("Morningstar", "Morningstar", []),
    ("Nightmare Realm Summoner 2", "Nightmare Realm Summoner 2", []),
    ("Nightmare Realm Summoner 3", "Nightmare Realm Summoner 3", []),
    ("Legend of the Arch Magus: Publisher's Pack 1 (Legend of the Arch Magus, #1-2)", "Legend of the Arch Magus: Publisher's Pack 1",
     [Series(name="Legend of the Arch Magus", numbers=["1","2"])]),
]


@pytest.mark.parametrize("input_title, expected_title, expected_series", TEST_TITLES)
def test_parse_titles_only(input_title: str, expected_title: str, expected_series: list):
        this_book: BookTitleData = parse_title(input_title)
        assert this_book.title == expected_title
        assert this_book.series == expected_series