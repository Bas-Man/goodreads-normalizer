import pytest

from goodreads_normalizer.exceptions.base import NarratorAsAuthorError
from goodreads_normalizer.validation.author import validate_author_name

TEST_AUTHOR_NAME = [
    "Jim Butcher",
    "Sean Oswald",
    "My Self",  # Unknown name should be valid; No assumptions made about the name
]

TEST_INVALID_AUTHORS = ["en-IN-PrabhatNeural"]

TEST_AUTHOR_NARRATORS = [
    "Travis Baldree",  # Known as Narrator and Author. In both lists
]


@pytest.mark.parametrize("input_name", TEST_AUTHOR_NAME)
def test_validate_author_name(input_name: str) -> None:
    assert validate_author_name(input_name) == input_name


@pytest.mark.parametrize("input_author", TEST_INVALID_AUTHORS)
def test_invalid_authors(input_author: str):
    with pytest.raises(NarratorAsAuthorError) as exc_info:
        validate_author_name(input_author)
    error = exc_info.value

    assert isinstance(error, NarratorAsAuthorError)
    assert error.contributor == input_author


@pytest.mark.parametrize("input_author", TEST_AUTHOR_NARRATORS)
def test_valid_author_and_narrator(input_author: str):
    assert validate_author_name(input_author) == input_author
