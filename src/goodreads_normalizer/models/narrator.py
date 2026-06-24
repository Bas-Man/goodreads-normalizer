from pydantic import BaseModel, model_validator, computed_field
from typing import Self


class Narrator(BaseModel):
    name: str

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
        return self.name.lower().replace(" ", "-")

    @model_validator(mode="after")
    def check_name(self) -> Self:
        if "- editor" in self.name:
            raise ValueError("Narrator name contains '- editor'")
        return self
