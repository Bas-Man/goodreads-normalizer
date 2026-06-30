from pydantic import (
    BaseModel,
    model_validator,
    computed_field,
    field_validator,
    PrivateAttr,
)
from goodreads_normalizer.parsers.regex_patterns import AUTHOR_NAME
from goodreads_normalizer.normalize.author_narrator import normalize_author_name
from typing import Self


class Narrator(BaseModel):
    name: str
    _first_name: str = PrivateAttr(default="")
    _last_name: str = PrivateAttr(default="")

    @field_validator("name")
    @classmethod
    def _normalize_name(cls, v) -> str:
        return normalize_author_name(v)

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
        Gives access to the Narrator's first name if available, else ""
        Returns:
            str:
        """
        return self._first_name or ""

    @computed_field
    @property
    def last_name(self) -> str:
        """
        Gives access to the Narrator's last name if available, else their nom deplume
        Returns:
            str:

        """
        return self._last_name

    @computed_field
    @property
    def slug(self) -> str:
        """

        Returns:
            str:
        """
        slug: str = (
            f"{self._last_name}-{self._first_name}"
            if self._first_name
            else self._last_name
        )
        return slug.replace(" ", "-").replace("'", "").lower()

    @model_validator(mode="after")
    def check_name(self) -> Self:
        """
        Checks that the name appear to be a Translator or Editor.
        I expect this will need some refactoring
        Returns:

        """
        if "- editor" in self.name.lower():
            raise ValueError("Narrator name contains '- editor'")
        elif "- translator" in self.name.lower():
            raise ValueError("Narrator name contains '- translator'")
        return self
