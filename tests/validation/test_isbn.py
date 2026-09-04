import pytest

from goodreads_normalizer.exceptions.base import NoISBNError, NoISBNWarning
from goodreads_normalizer.validation.isbn import (
    format_only_check,
    is_valid_isbn_10,
    is_valid_isbn_13,
)
from goodreads_normalizer.validation.severity import Severity


def test_format_only_check_blank_paperback():
    with pytest.raises(NoISBNError) as exc_info:
        format_only_check("", "Paperback")

    assert exc_info.value.severity == Severity.ERROR


def test_format_only_check_blank_kindle():
    with pytest.raises(NoISBNWarning) as exc_info:
        format_only_check("", "Kindle")

    assert exc_info.value.severity == Severity.WARNING


def test_format_only_check_under_10():
    assert not format_only_check("123456", "Kindle")


def test_format_only_check_over_13():
    assert not format_only_check("12345678910123", "Kindle")


def test_format_only_check_10():
    data = "1234567891"
    assert format_only_check(data, "Kindle")


def test_format_only_check_13():
    data = "1234567891123"
    assert format_only_check(data, "Kindle")


def test_is_valid_isbn_10():
    data = "0765325624"
    assert is_valid_isbn_10(data)


def test_is_valid_isbn_10_invalid():
    data = "0765325623"
    assert not is_valid_isbn_10(data)


def test_is_valid_isbn_13():
    data = "9780345522481"
    assert is_valid_isbn_13(data)


def test_is_valid_isbn_13_invalid():
    data = "9780345522482"
    assert not is_valid_isbn_13(data)
