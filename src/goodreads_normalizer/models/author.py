"""
# Author: Bas-Man
# Created Date: 2026-06-24
# File: author.py
"""

from typing import Self

from pydantic import BaseModel, PrivateAttr, computed_field, model_validator

from goodreads_normalizer.data.known_en_authors import PEN_NAME_TO_NAME
from goodreads_normalizer.normalize.author_narrator import normalize_author_name
from goodreads_normalizer.parsers.regex_patterns import AUTHOR_NAME
from goodreads_normalizer.validation.author import validate_author_name


class Author(BaseModel):
    """
    This object stores the information about an author.
    The Author may have a nom de plume.

    Attributes:
        name (str):
        pen_name (str): Author's Nom de plume

    Examples:
        ```{python}
        from goodreads_normalizer import Author

        author = Author(name="Brandon Sanderson")
        print(f"Author: {author.display_name}")
        print(f"Slug: {author.slug}")

        author = Author(name="Shirtaloon")
        print(f"Display Name: {author.display_name}")
        print(f"Is Pen Name: {author.is_pen_name}")
        print(f"Slug: {author.slug}")
        print(f"Pen Name: {author.pen_name}")
        print(f"Name: {author.name}")
        ```

    If the Author name is in the NARRATORS list and is also *not* in the AUTHORS list,
    a ValueError will be raised, which is then transformed into a ValidationError by
    pydantic.
    """

    name: str = ""
    pen_name: str | None = None
    # _first_name may be None if the pen_name or Author's name is a single word. "Homer"
    _first_name: str | None = PrivateAttr(default=None)
    _last_name: str = PrivateAttr(default="")

    @computed_field
    @property
    def display_name(self) -> str:
        """
        Provides either the Author's full real name, or their nom de plume

        Returns:
            str: Author's nom de plume or their true full name if known
        """
        if self.pen_name:
            return self.pen_name
        return self.name

    @model_validator(mode="before")
    @classmethod
    def _resolve_pen_name(cls, data: dict) -> dict:
        """
        Correctly treats input name as a pen name to look up the  name.
        """
        if isinstance(data, dict):
            raw_name = data.get("name", "")

            clean_name = normalize_author_name(raw_name)
            clean_name = validate_author_name(clean_name)

            if clean_name in PEN_NAME_TO_NAME:
                data["pen_name"] = clean_name
                data["name"] = PEN_NAME_TO_NAME[clean_name]
            else:
                data["name"] = clean_name
                data["pen_name"] = None

        return data

    @model_validator(mode="after")
    def _split_name_parts(self) -> Self:
        match = AUTHOR_NAME.fullmatch(self.name)
        if match:
            self._first_name = match.group("first_name")
            self._last_name = match.group("last_name") or ""
        return self

    @computed_field
    @property
    def first_name(self) -> str:
        """
        Gives access to the Author's first name if available, else ""
        """
        return self._first_name or ""

    @computed_field
    @property
    def last_name(self) -> str:
        """
        Gives access to the Author's last name if available, else their nom deplume
        """
        if not self._last_name and self.pen_name:
            return self.pen_name
        return self._last_name

    @computed_field
    @property
    def last_first_name(self) -> str:
        """
        Generates the Author's name as "Last Name, First Name"
        """
        return (
            f"{self._last_name}, {self._first_name}"
            if self._first_name
            else self._last_name
        ).strip()

    @computed_field
    @property
    def is_pen_name(self) -> bool:
        return self.pen_name is not None

    @computed_field
    @property
    def real_name(self) -> str:
        if self.pen_name:
            return self.name
        return self.name

    @computed_field
    @property
    def slug(self) -> str:
        """
        Generates a slug string format: 'last-first' using active name.
        Active name will either be the Author's nom de plume or their real name

        Returns:
            str: The string will be formatted suitable for the web
        """
        if self.pen_name:
            parts: list[str] = self.pen_name.split()
            name_to_use: str = f"{parts[-1]}-{parts[0]}" if len(parts) > 1 else parts[0]
        else:
            l_n: str = self.last_name.replace(
                ".", ""
            )  # "." should only appear at end of string
            f_n: str | None = None
            if self.first_name:
                f_n = self.first_name.replace(".", " ").strip()
            name_to_use = f"{l_n}-{f_n}" if f_n else l_n
        return name_to_use.replace(" ", "-").replace("'", "").lower()
