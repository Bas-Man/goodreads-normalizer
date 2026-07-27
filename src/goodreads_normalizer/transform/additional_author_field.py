from goodreads_normalizer.data import AUTHORS, ILLUSTRATORS, NARRATORS, TRANSLATORS
from goodreads_normalizer.models.author import Author
from goodreads_normalizer.models.bindings import BindingFormat
from goodreads_normalizer.models.narrator import Narrator
from goodreads_normalizer.normalize.author_narrator import normalize_author_name
from goodreads_normalizer.parsers.author_narrator import parse_additional_author


def transform_author_additional_authors(
    author_field: str,
    additional_author_field: str | None = None,
    binding: str | None = None,
) -> tuple[list[Author], list[Narrator]]:
    """
    This function uses the csv fields "Author", "Additional Authors" and "Binding" to create
    Author and Narrator objects.
    Translators and Editors are ignored if it can be determined.

    Args:
        author_field (str):
        additional_author_field (str):
        binding (str):

    Returns:
        tuple[list[Author], list[Narrator]]:

    """
    authors: list[Author] = [Author(name=author_field)]
    narrators: list[Narrator] = []
    binding_format: BindingFormat = BindingFormat.from_str(binding)
    # primary_author comes from the "Author" column
    primary_author: Author = authors[0]

    if additional_author_field is not None and additional_author_field != "":
        additional_authors: list[str] = parse_additional_author(additional_author_field)
        for name in additional_authors:
            name = normalize_author_name(name)
            if not binding_format.is_audiobook:
                if name not in TRANSLATORS:
                    authors.append(Author(name=name))
            else:
                if (name in TRANSLATORS) or (name in ILLUSTRATORS):
                    continue

                # If Author name is in both Author and Additional_authors, then author narrated their own book
                elif name == primary_author.name:
                    narrators.append(Narrator(name=name))
                # if name is a known author, and they are the first name in the additional_authors they are an author?
                elif (
                    name in AUTHORS and name not in NARRATORS
                ) and additional_authors.index(name) == 0:
                    authors.append(Author(name=name))
                elif name in NARRATORS:
                    narrators.append(Narrator(name=name))

    return authors, narrators
