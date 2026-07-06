from importlib.metadata import version

from .models.author import Author
from .models.narrator import Narrator
from .models.book import Book
from .io.csv import (
    load_csv as load_csv,
    export_to_stream as export_to_stream,
    NameFormatter as NameFormatter,
)

__version__ = version("goodreads-normalizer")

__all__ = [
    "Author",
    "Narrator",
    "Book",
    "load_csv",
    "export_to_stream",
    "NameFormatter",
]
