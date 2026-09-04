import csv
from pathlib import Path

from goodreads_normalizer.models import Author, Narrator
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


def test_maps_authors_and_narrators():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert len(data["authors"]) == 2
    assert data["authors"][0].name == "Karin Slaughter"
    assert data["authors"][1].name == "Lee Child"

    assert len(data["narrators"]) == 2
    assert data["narrators"][0].name == "Eric Jason Martin"
    assert data["narrators"][1].name == "Jeff Harding"


def test_maps_book_id():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert data["book_id"] == row["Book Id"]


def test_maps_title():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert data["title_data"] == row["Title"]


def test_maps_isbn():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert data["isbn10"] == row["ISBN"]


def test_maps_isbn13():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert data["isbn13"] == row["ISBN13"]


def test_maps_my_rating():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["rating"] == row["My Rating"]


def test_maps_publisher():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert data["publisher"] == row["Publisher"]


def test_maps_binding():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["binding"] == row["Binding"]


def test_maps_year_published():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["year_published"] == row["Year Published"]


def test_maps_original_publication_year():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["original_publication_year"] == row["Original Publication Year"]


def test_maps_number_of_pages():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["pages"] == row["Number of Pages"]


def test_maps_date_read():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["date_read"] == row["Date Read"]


def test_maps_date_added():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["date_added"] == row["Date Added"]


def test_maps_bookshelves():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["book_shelves"] == row["Bookshelves"]


def test_maps_bookshelves_with_positions():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["book_shelves_with_positions"] == row["Bookshelves with positions"]


def test_maps_exclusive_shelf():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["exclusive_shelf"] == row["Exclusive Shelf"]


def test_maps_my_review():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["my_review"] == row["My Review"]


def test_maps_spoiler():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["spoiler"] == row["Spoiler"]


def test_maps_private_notes():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["private_notes"] == row["Private Notes"]


def test_maps_read_count():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["read_count"] == row["Read Count"]


def test_maps_owned_copies():
    row = first_row()
    data = GoodreadsBookMapper.to_book_input(row)
    assert data["owned_copies"] == row["Owned Copies"]


def test_maps_single_author():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert len(data["authors"]) == 2
    assert data["authors"] == [Author(name="Karin Slaughter"), Author(name="Lee Child")]


def test_maps_audiobook_narrators():
    row = first_row()

    data = GoodreadsBookMapper.to_book_input(row)

    assert len(data["narrators"]) == 2
    assert data["narrators"] == [
        Narrator(name="Eric Jason Martin"),
        Narrator(name="Jeff Harding"),
    ]
