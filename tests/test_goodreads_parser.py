# tests/test_goodreads_parser.py

from io import StringIO

from goodreads_normalizer.parsers.goodreads_csv import parse_goodreads_csv


CSV_DATA = """Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Publisher
226152904,"Crystal Core 3: Crystal Core, Book 3",David Burke,"Burke, David",,,"",0,Podium Audio
226146301,"Crystal Core: Crystal Core, Book 1",David  Burke,"Burke, David",,,"",3,Podium Audio
"""


def test_parse_books():
    books = parse_goodreads_csv(StringIO(CSV_DATA))

    assert len(books) == 2

    assert books[0].title == "Crystal Core 3"
    assert books[0].series[0].name == "Crystal Core"
    assert books[0].series[0].numbers == ["3"]
    assert books[0].author == "David Burke"
    assert books[0].rating == 0
    assert books[0].book_id == "226152904"
    assert books[0].publisher == "Podium Audio"

    assert books[1].rating == 3
    assert books[1].author == "David Burke"
    assert books[1].book_id == "226146301"
