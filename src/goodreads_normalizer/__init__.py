from importlib.metadata import version

from .io.csv import (
    NameFormatter as NameFormatter,
)
from .io.csv import (
    export_to_stream as export_to_stream,
)
from .io.csv import (
    load_csv as load_csv,
)
from .models.author import Author
from .models.book import Book
from .models.narrator import Narrator

__version__ = version("goodreads-normalizer")

__all__ = [
    "__version__",
    "Author",
    "Narrator",
    "Book",
    "load_csv",
    "export_to_stream",
    "NameFormatter",
]
