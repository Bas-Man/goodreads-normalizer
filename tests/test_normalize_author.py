from goodreads_exporter.normalize.books import normalize_author_name

def test_author_whitespace_normalized():
    assert normalize_author_name("David    Burke") == "David Burke"
    assert normalize_author_name("") == ""
    assert normalize_author_name(None) == ""
    assert normalize_author_name("Sean Oswald") == "Sean Oswald"