from goodreads_exporter.models.book import BookTitleData, Series
from goodreads_exporter.parsers.book_title import parse_title

import pytest

"""
Test data for RULE_4: Books that are part of more than one series. Cross overs and such
"""
TEST_TITLES = [
    ("The Black Echo: Special Edition (Harry Bosch, #1; Harry Bosch Universe, #1)",
     "The Black Echo: Special Edition",
     [
        Series(name="Harry Bosch", numbers=["1"]),
        Series(name="Harry Bosch Universe", numbers=["1"])
     ]
     ),
    ("Cleaning the Gold (Will Trent, #8.5; Jack Reacher, #23.6)",
     "Cleaning the Gold",
     [
        Series(name="Will Trent", numbers=["8.5"]),
        Series(name="Jack Reacher", numbers=["23.6"])
     ]
     ),
    ("The Crystal Shard (Forgotten Realms: The Icewind Dale, #1; Legend of Drizzt, #4)",
     "The Crystal Shard",
     [
         Series(name="The Icewind Dale", numbers=["1"],),
         Series(name="Legend of Drizzt", numbers=["4"])
     ]
     ),
    ("The Halfling's Gem (Forgotten Realms: The Icewind Dale, #3; The Legend of Drizzt, #6)",
    "The Halfling's Gem",
     [Series(name="The Icewind Dale", numbers=["3"]),
      Series(name="The Legend of Drizzt", numbers=["6"])]),
]



@pytest.mark.parametrize("input_title, expected_title, expected_series", TEST_TITLES)
def test_parse_titles_only(input_title: str, expected_title: str, expected_series: list):
        this_book: BookTitleData = parse_title(input_title)
        assert this_book.title == expected_title
        assert this_book.series == expected_series