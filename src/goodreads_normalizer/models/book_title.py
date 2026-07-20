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
    This model stores information extracted from the "Title" row in the goodreads csv.

    Attributes:
        original_title (str): raw title
        title (str): parsed title
        series (Series): Series Model
    """

    original_title: str
    title: str
    # A book can belong to 0, 1, or many series
    series: list[Series] = Field(default_factory=list)

    @property
    def is_a_crossover(self) -> bool:
        """
        Check if the book belongs to more than one series. E.G: Will Trent and Jack
        Reacher
        """
        return len(self.series) > 1

    @property
    def is_part_of_series(self) -> bool:
        """
        Check if the book belongs to a series and not standalone book
        """
        return len(self.series) > 0

    @property
    def is_stand_alone(self) -> bool:
        """
        This is the inverse of is_part_of_series
        """
        return len(self.series) == 0

    @property
    def is_collection(self) -> bool:
        """
        This indicates if the book is a collection or more that one book in a series
        """
        return len(self.series) == 1 and len(self.series[0].numbers) > 1
