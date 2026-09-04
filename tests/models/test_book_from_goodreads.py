import csv
import datetime
from pathlib import Path

from goodreads_normalizer.models import Book

TEST_DATA = Path(__file__).parent.parent / "data" / "test_data3.csv"


def first_row() -> dict[str, str]:
    with TEST_DATA.open(newline="", encoding="utf-8") as f:
        return next(csv.DictReader(f))


def test_creates_book_from_goodreads_row():
    row = first_row()

    book = Book.from_goodreads(row)

    assert book.book_id == "45447539"
    assert book.title == "Cleaning the Gold"
    assert book.series[0].name == "Will Trent"
    assert book.series[0].numbers == ["8.5"]
    assert book.series[1].name == "Jack Reacher"
    assert len(book.authors) == 2
    assert book.authors[0].name == "Karin Slaughter"
    assert book.authors[1].name == "Lee Child"
    assert len(book.narrators) == 2
    assert book.narrators[0].name == "Eric Jason Martin"
    assert book.narrators[1].name == "Jeff Harding"
    assert book.isbn10 is None
    assert book.isbn13 is None
    assert book.rating == 4
    assert book.publisher == "HarperAudio"
    assert book.binding == "Audible Audio"
    assert book.pages == 0
    assert book.year_published == "2019"
    assert book.original_publication_year == "2019"
    assert book.date_read == datetime.date(2022, 7, 25)
    assert book.date_added == datetime.date(2022, 7, 24)
    assert book.book_shelves == []
    assert book.book_shelves_with_positions == []
    assert book.exclusive_shelf == "read"
    assert book.my_review == ""
    assert book.spoiler == ""
    assert book.private_notes == ""
    assert book.read_count == 1
    assert book.owned_copies == 0
