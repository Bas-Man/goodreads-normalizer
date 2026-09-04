import re

from goodreads_normalizer.exceptions.base import NoISBNError, NoISBNWarning


def is_valid_isbn(isbn: str) -> bool:
    """Convenience wrapper to check if a string is either ISBN-10 or ISBN-13."""
    return is_valid_isbn_10(isbn) or is_valid_isbn_13(isbn)


def format_only_check(s: str, binding: str) -> bool:
    if s == "":
        if (
            binding == "Kindle"
        ):  # Fix: logic wrong. Needs to deal with formats that do not require isbn
            raise NoISBNWarning
        raise NoISBNError
    clean = s.replace("-", "").replace(" ", "")
    return len(clean) in (10, 13) and clean.isalnum()


def calculate_isbn_10_check_digit(nine_digits: str) -> str:
    """Calculates the 10th check digit (0-9 or 'X') for a 9-digit string."""
    if not re.fullmatch(r"\d{9}", nine_digits):
        raise ValueError("Input must be exactly 9 numeric digits.")

    total = sum(int(digit) * (10 - i) for i, digit in enumerate(nine_digits))

    # Check digit is what needs to be added to reach the next multiple of 11
    remainder = (11 - (total % 11)) % 11
    return "X" if remainder == 10 else str(remainder)


def calculate_isbn_13_check_digit(twelve_digits: str) -> str:
    """Calculates the 13th check digit (0-9) for a 12-digit string."""
    if not re.fullmatch(r"\d{12}", twelve_digits):
        raise ValueError("Input must be exactly 12 numeric digits.")

    total = sum(
        int(digit) * (1 if i % 2 == 0 else 3) for i, digit in enumerate(twelve_digits)
    )

    # Check digit is what needs to be added to reach the next multiple of 10
    remainder = (10 - (total % 10)) % 10
    return str(remainder)


def is_valid_isbn_10(isbn: str) -> bool:
    """Validates an ISBN-10 by comparing its check digit against the calculated one."""
    clean = re.sub(r"[- ]", "", isbn.upper())

    if not re.fullmatch(r"\d{9}[\dX]", clean):
        return False

    expected_check_digit = calculate_isbn_10_check_digit(clean[:9])
    actual_check_digit = clean[9]

    return actual_check_digit == expected_check_digit


def is_valid_isbn_13(isbn: str) -> bool:
    """Validates an ISBN-13 by comparing its check digit against the calculated one."""
    clean = re.sub(r"[- ]", "", isbn)

    if not re.fullmatch(r"\d{13}", clean):
        return False

    expected_check_digit = calculate_isbn_13_check_digit(clean[:12])
    actual_check_digit = clean[12]

    return actual_check_digit == expected_check_digit
