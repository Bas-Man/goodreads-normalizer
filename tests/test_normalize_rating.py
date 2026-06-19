# tests/test_normalize_rating.py

from goodreads_normalizer.normalize.books import normalize_rating


def test_rating_preserved():
    assert normalize_rating("3") == 3


def test_rating_missing_is_zero():
    assert normalize_rating(None) == 0


def test_rating_blank_is_zero():
    assert normalize_rating("") == 0


def test_rating_whitespace_is_zero():
    assert normalize_rating("   ") == 0


def test_rating_invalid_is_zero():
    assert normalize_rating("abc") == 0