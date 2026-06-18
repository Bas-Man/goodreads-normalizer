# src/goodreads_exporter/models/book.py
from pydantic import BaseModel, Field


class Book(BaseModel):
    title: BookTitle
    author: str
    rating: int
    book_id: str

    def is_a_crossover(self) -> bool:
        return len(self.title.series) > 0

    def is_series_collection(self) -> bool:
        return len(self.title.series) == 1 and len(self.title.series[0].numbers) > 1

    def is_single_book(self) -> bool:
        return len(self.title.series) == 1 and len(self.title.series[0].numbers) == 1

    def is_a_stand_alone_book(self) -> bool:
        return len(self.title.series) == []

class Series(BaseModel):
    name: str
    numbers: list[str] = Field(default_factory=list)

class BookTitle(BaseModel):
    title: str
    # A book can belong to 0, 1, or many series
    series: list[Series] = Field(default_factory=list)

    def is_a_crossover(self) -> bool:
        return len(self.series) > 0