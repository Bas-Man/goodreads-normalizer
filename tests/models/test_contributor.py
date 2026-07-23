from goodreads_normalizer.models.contributor import (
    ContributorRole,
    classify_person,
)


def test_classify_person_author_only():
    role = classify_person("Brandon Sanderson")

    assert role == ContributorRole.AUTHOR


def test_classify_person_author_and_narrator():
    role = classify_person("Travis Baldree")

    assert role == (ContributorRole.AUTHOR | ContributorRole.NARRATOR)


def test_classify_person_unknown():
    role = classify_person("Someone Nobody Knows")

    assert role == ContributorRole.UNKNOWN


def test_classify_person_translator():
    role = classify_person("Hye Young Im")
    assert role == ContributorRole.TRANSLATOR
