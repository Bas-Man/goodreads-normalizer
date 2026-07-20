import pytest

from goodreads_normalizer.parsers.author_narrator import parse_additional_author

NARRATORS = [
    ("Travis Baltree, Lee lu (Translator)", ["Travis Baltree"]),
    ("Joshua Mason - editor", []),
    ("Travis Baltree, OppaTranslations - translator", ["Travis Baltree"]),
    ("Joshua Mason - editor, Heath Miller", ["Heath Miller"]),
    (
        "Joshua Mason - editor, Heath Miller, Travis Baltree",
        ["Heath Miller", "Travis Baltree"],
    ),
    ("G.D. Penman", ["G.D. Penman"]),
    ("Hye Young Im, J. Torres", ["Hye Young Im", "J. Torres"]),
    ("Robert J. Ransisi", ["Robert J. Ransisi"]),
    ("Travis Baltree (Narrator)", ["Travis Baltree"]),
]


@pytest.mark.parametrize("input_string, expected_narrators", NARRATORS)
def test_additional_authors(input_string: str, expected_narrators: list[str]):
    additional_authors = parse_additional_author(input_string)
    assert additional_authors == expected_narrators
