from pydantic import BaseModel, computed_field, field_validator, Field, model_validator
from goodreads_normalizer.normalize.books import normalize_author_name
from goodreads_normalizer.validation.author import validate_author_name
from goodreads_normalizer.data.known_en_authors import PEN_NAME_TO_NAME

class Author(BaseModel):
    name: str = ""
    pen_name: str | None = None

    @computed_field
    @property
    def display_name(self) -> str:
        if self.pen_name:
            return self.pen_name
        return self.name

    @model_validator(mode="before")
    @classmethod
    def resolve_pen_name(cls, data: dict) -> dict:
        """Correctly treats input name as a pen name to look up the  name."""
        if isinstance(data, dict):
            raw_name = data.get("name", "")

            clean_name = normalize_author_name(raw_name)
            clean_name = validate_author_name(clean_name)

            if clean_name in PEN_NAME_TO_NAME:
                data["pen_name"] = clean_name
                data["name"] = PEN_NAME_TO_NAME[clean_name]
            else:
                data["name"] = clean_name  # ← keep in sync
                data["pen_name"] = None

        return data

    @computed_field
    @property
    def first_name(self) -> str:
        return self.name.split(" ", 1)[0]

    @computed_field
    @property
    def last_name(self) -> str:
        parts = self.name.split(" ", 1)
        return parts[1] if len(parts) > 1 else ""

    @computed_field
    @property
    def slug(self) -> str:
        """Generates a slug string format: 'last-first' using active name."""
        name_to_use = self.name
        if self.pen_name:
            name_to_use = self.pen_name
        parts = name_to_use.split()
        if len(parts) == 1:
            return parts[0].lower()

        first = parts[0]
        last = parts[-1]

        return f"{last}-{first}".lower()