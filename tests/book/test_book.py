import pytest

from goodreads_normalizer import Author, Book, Narrator
from goodreads_normalizer.models import Series

TEST_DATA = [
    (
        "1234",
        "Zero",
        "Zero",
        "Eric Van Lustbader",
        [Author(name="Eric Van Lustbader")],
        "Audible",
    ),
    ("1234", "Zero", "Zero", None, [], ""),
]


@pytest.mark.parametrize(
    "book_id, title, expected_title, author, expected_author_list,bindings", TEST_DATA
)
def test_basic_book(
    book_id, title, expected_title, author, expected_author_list, bindings
):
    book = Book.create(book_id=book_id, title=title, author=author, binding=bindings)
    assert book.title == expected_title
    assert book.book_id == book_id
    assert book.title == expected_title
    assert book.authors == expected_author_list
    assert book.binding == bindings


TEST_DATA_KNOWN_AUTHORS_NARRATORS = [
    (
        "1234",
        "He Who Fights With Monsters 1 (He Who Fights With Monsters #1)",
        "He Who Fights With Monsters 1",
        [Series(name="He Who Fights With Monsters", numbers=["1"])],
        [Author(name="Shirtaloon")],
        [Narrator(name="Travis Baldree")],
        "",
    ),
    (
        "1234",
        "He Who Fights With Monsters 2 (He Who Fights With Monsters #2)",
        "He Who Fights With Monsters 2",
        [Series(name="He Who Fights With Monsters", numbers=["2"])],
        [Author(name="Shirtaloon")],
        [Narrator(name="Maggie")],
        "",
    ),
]


@pytest.mark.parametrize(
    "book_id, title, expected_title, expected_series, authors_list, narrators_list,bindings",
    TEST_DATA_KNOWN_AUTHORS_NARRATORS,
)
def test_book_author_narrator(
    book_id,
    title,
    expected_title,
    expected_series,
    authors_list,
    narrators_list,
    bindings,
):
    book = Book.create(
        book_id=book_id, title=title, authors=authors_list, narrators=narrators_list
    )
    assert book.authors == authors_list
    assert book.title == expected_title
    assert book.series == expected_series
    assert book.narrators == narrators_list
    assert book.binding == bindings
