from pydantic import BaseModel, Field


class Series(BaseModel):
    """
    This model stores information about the book series the book belongs to.
    It also stores the books series numbers
    Note: numbers is a list[str]
    ["1"] Book number 1 of series
    ["1", "2"] Books ond and two of series
    ["3", "5"] Books 3, 4 and 5 of series
    """

    name: str
    numbers: list[str] = Field(default_factory=list)


class BookTitleData(BaseModel):
    """
    This model stores information extract from the "Title" row in the goodreads csv.
    """

    original_title: str
    title: str
    # A book can belong to 0, 1, or many series
    series: list[Series] = Field(default_factory=list)

    @property
    def is_a_crossover(self) -> bool:
        return len(self.series) > 1

    @property
    def is_part_of_series(self) -> bool:
        return len(self.series) >= 1

    @property
    def is_stand_alone(self) -> bool:
        return len(self.series) == 0
