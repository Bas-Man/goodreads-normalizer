from pydantic import BaseModel, computed_field, field_validator
from goodreads_normalizer.normalize.books import normalize_author_name
from goodreads_normalizer.validation.author import validate_author_name

class Author(BaseModel):
    name: str = ""

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = normalize_author_name(value)
        value = validate_author_name(value)
        return value
    
    @computed_field
    @property
    def first_name(self) -> str:
        return self.name.split(" ", 1)[0]

    @computed_field
    @property
    def last_name(self) -> str:
        return self.name.split(" ", 1)[1]

    @computed_field
    @property
    def slug(self) -> str:
        return (self.last_name + "-" + self.first_name).lower()
