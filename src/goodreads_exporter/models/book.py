# src/goodreads_exporter/models/book.py
from pydantic import BaseModel, Field


class Book(BaseModel):
    title_data: BookTitleData
    author: str
    rating: int
    book_id: str

    @property
    def title(self):
        return self.title_data.title

    @property
    def series(self):
        return self.title_data.series

    def is_a_crossover(self) -> bool:
        """Belongs to multiple distinct series."""
        return len(self.series) > 1

    def is_series_collection(self) -> bool:
        """Belongs to 1 series, but spans multiple book numbers."""
        return len(self.series) == 1 and len(self.series[0].numbers) > 1

    def is_single_book(self) -> bool:
        """Belongs to 1 series, and is just a single entry."""
        return len(self.series) == 1 and len(self.series[0].numbers) == 1

    def is_a_stand_alone_book(self) -> bool:
        """Belongs to 0 series."""
        return len(self.series) == 0


class Series(BaseModel):
    name: str
    numbers: list[str] = Field(default_factory=list)

class BookTitleData(BaseModel):
    title: str
    # A book can belong to 0, 1, or many series
    series: list[Series] = Field(default_factory=list)

    def is_a_crossover(self) -> bool:
        return len(self.series) > 0