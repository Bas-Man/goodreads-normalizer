import pytest

from goodreads_normalizer.models.author import Author
from goodreads_normalizer.models.narrator import Narrator
from goodreads_normalizer.transform.additional_author_field import (
    transform_author_additional_authors,
)

TEST_DATA = [
    (
        "Sean Oswald",
        "Travis Baldree",
        "Audiobook",
        [Author(name="Sean Oswald")],
        [Narrator(name="Travis Baldree")],
    ),
    (
        "Sean Oswald",
        "Travis Baldree, Joshua Mason - editor",
        "Audible Audio",
        [Author(name="Sean Oswald")],
        [Narrator(name="Travis Baldree")],
    ),
    (
        "Andy Weir",
        "Jonathan        Davis, Christy Romano, R.C. Bray",
        "Audible Audio",
        [Author(name="Andy Weir")],
        [
            Narrator(name="Jonathan Davis"),
            Narrator(name="Christy Romano"),
            Narrator(name="R.C. Bray"),
        ],
    ),
    (
        "Matthew Costello",
        "Neil Richards",
        "Audible Audio",
        [Author(name="Matthew Costello"), Author(name="Neil Richards")],
        [],
    ),
    (
        "Matthew Costello",
        "Neil Richards, Neil Dudgeon",
        "Audible Audio",
        [Author(name="Matthew Costello"), Author(name="Neil Richards")],
        [Narrator(name="Neil Dudgeon")],
    ),
    (
        "Chugong",
        "Hye Young Im, J. Torres",  # Tranlators
        "Audible Audio",
        [Author(name="Chugong")],
        [],
    ),
    (
        "Matthew Costello",
        "Neil Richards",
        "Kindle Edition",
        [Author(name="Matthew Costello"), Author(name="Neil Richards")],
        [],
    ),
]


@pytest.mark.parametrize(
    "author_field, additional_author_field, binding, expected_author_list, expected_narrator_list",
    TEST_DATA,
)
def test_transform_author_additional_authors(
    author_field: str,
    additional_author_field: str | None,
    binding: str | None,
    expected_author_list: list[Author],
    expected_narrator_list: list[Narrator],
):
    authors, narrators = transform_author_additional_authors(
        author_field, additional_author_field, binding
    )
    assert narrators is not None
    assert authors is not None
    assert authors == expected_author_list
    assert narrators == expected_narrator_list
