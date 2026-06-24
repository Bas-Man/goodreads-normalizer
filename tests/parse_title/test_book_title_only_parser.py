from goodreads_normalizer.models.book import BookTitleData
from goodreads_normalizer.parsers.book_title import parse_title

import pytest

TEST_TITLES = [
    "10 Rules for the Perfect Murder",
    "Academy of Outcasts",
    "Assassin's Blade",
    "Battle Mage",
    "Black Blade",
    "Black Heart",
    "Christine",
    "Death Match",
    "English Grammar Boot Camp",
    "Firstborn",
    "It",
    "James Moriarty, Consulting Criminal",
    "Middlebridge Mysteries",
    "Morningstar",
    "Nightmare Realm Summoner 2",
    "Nightmare Realm Summoner 3",
    "Oracle",
    "Perfect State",
    "Project Hail Mary",
    "Rise of the Shadow Mage",
    "Rust Brain Teasers",
    "Shadows for Silence in the Forests of Hell",
    "Snapshot",
    "Solo",
]


@pytest.mark.parametrize("input_title", TEST_TITLES)
def test_parse_titles_only(input_title: str):
    this_title: BookTitleData = parse_title(input_title)
    assert this_title.title == input_title
    assert this_title.series == []
