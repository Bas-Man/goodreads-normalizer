# src/goodreads_exporter/models/goodreads_row.py

from pydantic import BaseModel


class GoodreadsRow(BaseModel):
    book_id: str
    title: str
    author: str
    rating: int