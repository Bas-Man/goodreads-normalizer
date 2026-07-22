import csv
from pathlib import Path

from goodreads_normalizer.parsers.goodreads_mapper import GoodreadsBookMapper

TEST_DATA = Path(__file__).parent.parent / "data" / "test_data3.csv"


def first_row() -> dict[str, str]:
    with TEST_DATA.open(newline="", encoding="utf-8") as f:
        return next(csv.DictReader(f))


def test_maps_required_fields():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert data["book_id"] == "45447539"
    assert (
        data["title_data"]
        == "Cleaning the Gold (Will Trent, #8.5; Jack Reacher, #23.6)"
    )
    assert data["rating"] == "4"
    assert data["publisher"] == "HarperAudio"
    assert data["binding"] == "Audible Audio"


def test_preserves_goodreads_fields():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert data["Author"] == "Karin Slaughter"
    assert data["Author l-f"] == "Slaughter, Karin"
    assert data["Additional Authors"] == "Lee Child, Eric Jason Martin, Jeff Harding"


def test_maps_optional_fields():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert data["year_published"] == "2019"
    assert data["original_publication_year"] == "2019"
    assert data["read_count"] == "1"
    assert data["owned_copies"] == "0"
