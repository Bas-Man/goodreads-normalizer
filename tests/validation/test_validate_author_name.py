import pytest

from goodreads_normalizer.validation.author import validate_author_name

TEST_AUTHOR_NAME = [
    "Jim Butcher",
    "Sean Oswald",
    "My Self",  # Used to confirm that a name that is not in either KNOWN_AUTHORS or KNOWN_NARRATORS is valid
]

TEST_INVALID_AUTHORS = ["en-IN-PrabhatNeural"]

TEST_AUTHOR_NARRATORS = [
    "Travis Baltree",  # Know as Narrator. He also has written some books, meaning he can appear in the KNOWN_NARRATOR list
]


@pytest.mark.parametrize("input_name", TEST_AUTHOR_NAME)
def test_validate_author_name(input_name: str) -> None:
    assert validate_author_name(input_name) == input_name


@pytest.mark.parametrize("input_author", TEST_INVALID_AUTHORS)
def test_invalid_authors(input_author: str):
    with pytest.raises(ValueError):
        validate_author_name(input_author)


@pytest.mark.parametrize("input_author", TEST_AUTHOR_NARRATORS)
def test_valid_author_and_narrator(input_author: str):
    assert validate_author_name(input_author) == input_author
