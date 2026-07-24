from enum import Flag, auto

from goodreads_normalizer.data import AUTHORS, NARRATORS, TRANSLATORS


class ContributorRole(Flag):
    UNKNOWN = 0
    AUTHOR = auto()
    NARRATOR = auto()
    TRANSLATOR = auto()
    EDITOR = auto()
    ILLUSTRATOR = auto()


def classify_person(name: str) -> ContributorRole:
    role = ContributorRole.UNKNOWN

    if name in AUTHORS:
        role |= ContributorRole.AUTHOR

    if name in NARRATORS:
        role |= ContributorRole.NARRATOR

    if name in TRANSLATORS:
        role |= ContributorRole.TRANSLATOR

    # if name in EDITORS:
    #    role |= ContributorRole.EDITOR

    # if Name in ILLUSTRATORS:
    #    role |= ContributorRole.ILLUSTRATOR

    return role
