# tests/test_goodreads_parser.py
import datetime
from io import StringIO

from goodreads_normalizer.models.narrator import Narrator
from goodreads_normalizer.parsers.goodreads_csv import parse_goodreads_csv

CSV_DATA = """Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Publisher,Binding,Year Published
226152904,"Crystal Core 3: Crystal Core, Book 3",David Burke,"Burke, David",,1234567891,"",0,Podium Audio,Audible Audio,2025
226146301,"Crystal Core: Crystal Core, Book 1",David  Burke,"Burke, David",,,"1234567891234",3,"",Kindle,2025
"""


def test_parse_books():
    books = parse_goodreads_csv(StringIO(CSV_DATA))

    assert len(books) == 2

    assert books[0].title == "Crystal Core 3"
    assert books[0].series[0].name == "Crystal Core"
    assert books[0].series[0].numbers == ["3"]
    assert books[0].authors[0].name == "David Burke"
    assert books[0].authors[0].last_first_name == "Burke, David"
    assert books[0].authors[0].pen_name is None
    assert books[0].narrators == []

    assert books[0].isbn == "1234567891"
    assert books[0].isbn13 is None
    assert books[0].rating == 0
    assert books[0].book_id == "226152904"
    assert books[0].publisher == "Podium Audio"
    assert books[0].binding == "Audible Audio"
    assert books[0].year_published == "2025"

    assert books[0].authors[0].name == "David Burke"
    assert books[0].authors[0].last_first_name == "Burke, David"
    assert books[1].rating == 3
    assert books[1].isbn is None
    assert books[1].isbn13 == "1234567891234"
    assert books[1].book_id == "226146301"
    assert books[1].publisher == ""
    assert books[1].binding == "Kindle"


CSV_DATA2 = (
    "Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Publisher,Binding,Number of Pages,Year Published,Original Publication Year,Date Read,Date Added,Bookshelves,Bookshelves with positions,Exclusive Shelf,My Review,Spoiler,Private Notes,Read Count,Owned Copies\n"
    '247447878,Unchained: A Litrpg Apocalypse (Welcome to the Multiverse Book 11),Sean Oswald,"Oswald, Sean",Joshua Mason,"=""""", "=""""",4,,Kindle Edition,906,2026,,2026/05/13,2026/05/06,,,read,,,,1,0\n'
    '226152904,"Crystal Core 3: Crystal Core, Book 3",David    Burke,"Burke, David","Daniel Wisniewski, Rebecca Woods","=""""","=""""",0,Podium Audio,Audible Audio,,2024,,,2026/05/19,currently-reading,currently-reading (#5),currently-reading,,,,1,0\n'
    '226146301,"Crystal Core: Crystal Core, Book 1",David    Burke,"Burke, David","Daniel Wisniewski, Rebecca Woods","=""""","=""""",3,Podium Audio,Audible Audio,,2024,2023,2026/05/07,2026/05/06,,,read,,,,1,0\n'
    '131942335,Awakening (Book of the Dead #1),RinoZ,"RinoZ, RinoZ",,"=""""","=""""",0,Aethon Books,Kindle Edition,542,2023,2021,,2023/11/13,"not-yet-finished, unable-to-finish","not-yet-finished (#2), unable-to-finish (#2)",unable-to-finish,,,,1,0\n'
    '55680505,"Seaborn (The Seaborn Cycle, #1)",Michael Livingston,"Livingston, Michael",,"=""""","=""""",0,Audible,Audible Audio,,2020,2020,,2025/08/15,"not-yet-finished, unable-to-finish","not-yet-finished (#5), unable-to-finish (#1)",unable-to-finish,,,,1,0\n'
)


def test_parse_books2():
    books = parse_goodreads_csv(StringIO(CSV_DATA2))
    assert len(books) == 5
    assert books[0].book_id == "247447878"
    assert books[0].title == "Unchained: A Litrpg Apocalypse"
    assert books[0].series[0].name == "Welcome to the Multiverse"
    assert books[0].series[0].numbers == ["11"]
    assert books[0].authors[0].name == "Sean Oswald"
    assert books[0].narrators == []
    assert books[0].isbn is None
    assert books[0].isbn13 is None
    assert books[0].rating == 4
    assert books[0].publisher == ""
    assert books[0].binding == "Kindle Edition"
    assert books[0].pages == 0
    assert books[0].year_published == "2026"
    assert books[0].original_publication_year == ""
    assert books[0].date_read == datetime.date(2026, 5, 13)
    assert books[0].date_added == datetime.date(2026, 5, 6)
    assert books[0].book_shelves == []
    assert books[0].book_shelves_with_positions == []
    assert books[0].exclusive_shelf == "read"
    assert books[0].my_review == ""
    assert books[0].spoiler == ""
    assert books[0].private_notes == ""
    assert books[0].read_count == 1
    assert books[0].owned_copies == 0

    assert books[1].book_id == "226152904"
    assert books[1].title == "Crystal Core 3"
    assert books[1].series[0].name == "Crystal Core"
    assert books[1].series[0].numbers == ["3"]
    assert books[1].authors[0].name == "David Burke"
    assert books[1].narrators == [
        Narrator(name="Daniel Wisniewski"),
        Narrator(name="Rebecca Woods"),
    ]
    assert books[1].isbn is None
    assert books[1].isbn13 is None
    assert books[1].rating == 0
    assert books[1].publisher == "Podium Audio"
    assert books[1].binding == "Audible Audio"
    assert books[1].pages == 0
    assert books[1].year_published == "2024"
    assert books[1].original_publication_year == ""
    assert books[1].date_read is None
    assert books[1].date_added == datetime.date(2026, 5, 19)
    assert books[1].book_shelves == ["currently-reading"]
    assert books[1].book_shelves_with_positions == ["currently-reading (#5)"]
    assert books[1].exclusive_shelf == "currently-reading"
    assert books[1].my_review == ""
    assert books[1].spoiler == ""
    assert books[1].private_notes == ""
    assert books[1].read_count == 1
    assert books[1].owned_copies == 0

    assert books[2].book_id == "226146301"
    assert books[2].title == "Crystal Core"
    assert books[2].series[0].name == "Crystal Core"
    assert books[2].series[0].numbers == ["1"]
    assert books[2].authors[0].name == "David Burke"
    assert books[2].narrators == [
        Narrator(name="Daniel Wisniewski"),
        Narrator(name="Rebecca Woods"),
    ]
    assert books[2].isbn is None
    assert books[2].isbn13 is None
    assert books[2].rating == 3
    assert books[2].publisher == "Podium Audio"
    assert books[2].binding == "Audible Audio"
    assert books[2].pages == 0
    assert books[2].year_published == "2024"
    assert books[2].original_publication_year == "2023"
    assert books[2].date_read == datetime.date(2026, 5, 7)
    assert books[2].date_added == datetime.date(2026, 5, 6)
    assert books[2].book_shelves == []
    assert books[2].book_shelves_with_positions == []
    assert books[2].exclusive_shelf == "read"
    assert books[2].my_review == ""
    assert books[2].spoiler == ""
    assert books[2].private_notes == ""
    assert books[2].read_count == 1
    assert books[2].owned_copies == 0

    assert books[3].book_shelves == ["not-yet-finished", "unable-to-finish"]
    assert books[3].book_shelves_with_positions == [
        "not-yet-finished (#2)",
        "unable-to-finish (#2)",
    ]

    assert books[4].book_shelves_with_positions == [
        "not-yet-finished (#5)",
        "unable-to-finish (#1)",
    ]
