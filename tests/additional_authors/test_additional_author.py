from goodreads_normalizer.models.narrator import Narrator
import pytest

TEST_LIST = [
    (
        "Travis Baldree",
        "Travis Baldree",
        "Travis",
        "Baldree",
        "Travis Baldree (N)",
        "Travis Baldree (Narrator)",
        "baldree-travis",
    ),
]

TEST_FAIL_LIST = ["Exit - editor", "exit - translator"]


@pytest.mark.parametrize(
    "input_name, expected_name, expected_first, expected_last, short_tag, long_tag, slug",
    TEST_LIST,
)
def test_narrator(
    input_name: str,
    expected_name: str,
    expected_first: str,
    expected_last: str,
    short_tag: str,
    long_tag: str,
    slug: str,
):
    nar: Narrator = Narrator(name=input_name)
    assert nar.name == expected_name
    assert nar.last_name == expected_last
    assert nar.first_name == expected_first
    assert nar.name_with_short_tag == short_tag
    assert nar.name_with_long_tag == long_tag
    assert nar.slug == slug


@pytest.mark.parametrize("input_name", TEST_FAIL_LIST)
def test_bogus_narrator(input_name: str):
    with pytest.raises(ValueError):
        Narrator(name=input_name)
