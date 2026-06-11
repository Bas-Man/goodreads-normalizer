# src/goodreads_exporter/models/book.py

from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    rating: int