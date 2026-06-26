# tests/test_goodreads_parser.py

from io import StringIO

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

    assert books[0].isbn == "1234567891"
    assert books[0].isbn13 == ""
    assert books[0].rating == 0
    assert books[0].book_id == "226152904"
    assert books[0].publisher == "Podium Audio"
    assert books[0].binding == "Audible Audio"
    assert books[0].year_published == "2025"

    assert books[0].authors[0].name == "David Burke"
    assert books[0].authors[0].last_first_name == "Burke, David"
    assert books[1].rating == 3
    assert books[1].isbn == ""
    assert books[1].isbn13 == "1234567891234"
    assert books[1].book_id == "226146301"
    assert books[1].publisher == ""
    assert books[1].binding == "Kindle"
