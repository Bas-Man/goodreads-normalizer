import pytest

from goodreads_normalizer.exceptions.base import NoBookTitleError
from goodreads_normalizer.models import BookTitleData
from goodreads_normalizer.transform.books import transform_book_title


# Test expected exception handling
def test_transform_book_title_empty_raises_error():
    with pytest.raises(NoBookTitleError):
        transform_book_title("")


def test_transform_book_title_whitespace_raises_error():
    with pytest.raises(NoBookTitleError):
        transform_book_title("   ")


def test_transform_book_title_valid():
    title = "The Great Gatsby"
    result = transform_book_title(title)

    assert isinstance(result, BookTitleData)
    assert result.title == "The Great Gatsby"
