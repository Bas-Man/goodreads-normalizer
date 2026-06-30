from goodreads_normalizer.parsers.book_title import parse_title

import pytest

TEST_TITLES = ["Zero [Paperback] Lustbader Eric V"]


@pytest.mark.parametrize("input_title", TEST_TITLES)
def test_parse_titles_only(input_title: str):
    with pytest.raises(ValueError):
        parse_title(input_title)
