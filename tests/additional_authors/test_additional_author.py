from goodreads_normalizer.models.narrator import Narrator
import pytest

TEST_LIST = [
    ("Travis Baltree", "Travis Baltree"),
]

TEST_FAIL_LIST = [
    "Exit - editor",
]


@pytest.mark.parametrize("input_name, expected_name", TEST_LIST)
def test_narrator(input_name: str, expected_name: str):
    nar: Narrator = Narrator(name=input_name)
    assert nar.name == expected_name


@pytest.mark.parametrize("input_name", TEST_FAIL_LIST)
def test_bogus_narrator(input_name: str):
    with pytest.raises(ValueError):
        Narrator(name=input_name)
