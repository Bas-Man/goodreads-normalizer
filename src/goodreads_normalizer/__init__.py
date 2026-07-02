from importlib.metadata import version

from .models.author import Author
from .models.narrator import Narrator
from .models.book import Book

__version__ = version("goodreads-normalizer")

__all__ = [
    "Author",
    "Narrator",
    "Book",
]
