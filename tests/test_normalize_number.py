from goodreads_normalizer.normalize.books import normalize_number


def test_rating_preserved():
    assert normalize_number("3") == 3


def test_rating_missing_is_zero():
    assert normalize_number(None) == 0


def test_rating_blank_is_zero():
    assert normalize_number("") == 0


def test_rating_whitespace_is_zero():
    assert normalize_number("   ") == 0


def test_rating_invalid_is_zero():
    assert normalize_number("abc") == 0
