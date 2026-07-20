import pytest

from goodreads_normalizer.models.author import Author

TEST_VALID_AUTHORS = [
    ("Jim Butcher", "Jim Butcher", "Jim", "Butcher", None, "butcher-jim"),
    ("Dakota Krout", "Dakota Krout", "Dakota", "Krout", None, "krout-dakota"),
    ("Bob  Smith", "Bob Smith", "Bob", "Smith", None, "smith-bob"),
    ("Shirtaloon", "Shirtaloon", "Travis", "Deverell", "Shirtaloon", "shirtaloon"),
    (
        "Always RollsAOne",
        "Always RollsAOne",
        "Erick",
        "Thiemke",
        "Always RollsAOne",
        "rollsaone-always",
    ),
    ("Homer", "Homer", "", "Homer", None, "homer"),
]


@pytest.mark.parametrize(
    "input_author, expected_author, expect_first, expected_last, pen, slug",
    TEST_VALID_AUTHORS,
)
def test_valid_authors(
    input_author: str,
    expected_author: str,
    expect_first: str,
    expected_last: str,
    pen: str | None,
    slug: str,
):
    author: Author = Author(name=input_author)
    assert author.display_name == expected_author
    assert author.first_name == expect_first
    assert author.last_name == expected_last
    assert author.slug == slug


TEST_THREE_PARTS_NAME = [
    ("James A. Hunter", "James A. Hunter", "James A.", "Hunter", "hunter-james-a"),
    (
        "L.E. Modesitt Jr.",
        "L.E. Modesitt Jr.",
        "L.E.",
        "Modesitt Jr.",
        "modesitt-jr-l-e",
    ),
]


@pytest.mark.parametrize(
    "input_name, expected_name, first_name, last_name, slug", TEST_THREE_PARTS_NAME
)
def test_three_parts_name(
    input_name: str, expected_name: str, first_name: str, last_name: str, slug: str
):
    author: Author = Author(name=input_name)
    assert author.display_name == expected_name
    assert author.first_name == first_name
    assert author.last_name == last_name
    assert author.slug == slug
