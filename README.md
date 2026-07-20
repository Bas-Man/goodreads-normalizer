# Goodreads Normalizer

[![CI](https://github.com/Bas-Man/goodreads-normalizer/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/Bas-Man/goodreads-normalizer/actions/workflows/ci.yml)
[![Documentation](https://github.com/Bas-Man/goodreads-normalizer/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/Bas-Man/goodreads-normalizer/actions/workflows/docs.yml)
<!--[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://bas-man.github.io/goodreads-normalizer)-->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/goodreads-normalizer)](https://pypi.org/project/goodreads-normalizer/)
[![Python](https://img.shields.io/pypi/pyversions/goodreads-normalizer)](https://pypi.org/project/goodreads-normalizer/)

A Python library and command-line application for cleaning, validating, and normalizing Goodreads library exports.

Goodreads exports are an excellent way to back up your library, but the exported data is often inconsistent. Author names, series information, ISBNs, dates, shelves, and other metadata can vary significantly, making it difficult to analyse, migrate, or integrate with other cataloguing systems.

**Goodreads Normalizer** provides deterministic normalization using strongly typed Pydantic models, allowing your Goodreads data to be transformed into clean, validated, machine-readable records.

---

## Features

- 📚 Read Goodreads CSV exports
- ✨ Normalize author names
- 👤 Validate author metadata
- 📝 Normalize audiobook narrator information
- 📖 Parse and normalize series information
- 🔢 Normalize ISBN values
- 📅 Consistent date handling
- 🗂 Typed Pydantic models
- 📄 Read and write CSV files
- 🖥 Command-line interface
- 🐍 Python library API

---

## Why This Project?

Goodreads has existed for many years, and its export format reflects that history.

Some common issues include:

- inconsistent author names
- additional contributor information stored inconsistently
- multiple spellings of the same person
- incomplete or malformed series data
- inconsistent ISBN formatting
- missing or duplicated values

This project aims to normalize these inconsistencies while preserving the original information wherever possible.

The goal is **predictable, repeatable normalization**, not automatic guessing.

---

## Installation

### Using pip

```bash
pip install goodreads-normalizer
```

### Using uv

```bash
uv add goodreads-normalizer
```

---

## Quick Start

Export your Goodreads library as a CSV file from Goodreads, then normalize it with a single command:

```bash
goodreads-normalizer \
    --file goodreads_export.csv \
    --output normalized.csv
```

This command:

- Reads the Goodreads export.
- Validates and normalizes the book metadata.
- Writes the normalized records to `normalized.csv`.
- Leaves the original export unchanged.

> **Tip:** Keep your original Goodreads export as a backup. The normalized CSV is intended for further processing, analysis, or import into other cataloguing tools.

---

## Command Line Usage

The example above uses the long option names for clarity. Once you're familiar with the tool, the equivalent short form is:

```bash
goodreads-normalizer \
    -f goodreads_export.csv \
    -o normalized.csv
```

To see all available options:

```bash
goodreads-normalizer --help
```

---

## Library Usage

In addition to the command-line interface, Goodreads Normalizer can be used as a Python library.

The `load_csv()` function reads a Goodreads export and returns a list of validated `Book` models.

```python
from goodreads_normalizer import load_csv

books = load_csv("goodreads_export.csv")

for book in books:
    print(book.title)
    print(book.authors)
    print(book.series)
```

Each `Book` is a fully validated Pydantic model. During model creation, Goodreads data is parsed and normalized automatically, including:

- author information
- narrator information
- book titles and series metadata
- ISBN values
- dates
- shelves
- numeric fields

Advanced users may also construct models directly when working with structured data.

```python
from goodreads_normalizer import Book

book = Book(
    book_id="123456",
    # ... remaining fields omitted for brevity
)
```

The package also exposes the core models for applications that need to inspect, validate, transform, or export Goodreads data programmatically.

```python
from goodreads_normalizer import (
    Author,
    Book,
    Narrator,
)
```
---

## What Gets Normalized?

Goodreads exports often contain inconsistent or difficult-to-process metadata. Goodreads Normalizer converts these values into structured, validated models while preserving the original information whenever possible.

| Goodreads export                      | Normalized                                                         |
| ------------------------------------- | ------------------------------------------------------------------ |
| `King, Stephen`                       | Structured `Author` model                                          |
| `The Colour of Magic (Discworld, #1)` | `BookTitleData` containing the title and structured `Series` model |
| `978-1-85723-138-9`                   | Normalized ISBN value                                              |
| `Fantasy, Owned, Audible`             | `["Fantasy", "Owned", "Audible"]`                                  |
| `2025/06/01`                          | `datetime.date(2025, 6, 1)`                                        |
| Empty or missing values               | Appropriate `None` or empty collections                            |

Normalization currently includes:

- author information
- audiobook narrator information
- book titles and series metadata
- ISBN and ISBN-13 values
- dates
- shelves
- numeric fields
- validation of Goodreads metadata

The project deliberately avoids changing data that cannot be normalized with confidence.

---

## Supported Python Versions

Goodreads Normalizer currently supports:

- Python 3.12
- Python 3.13
- Python 3.14

Support for newer Python releases will be added as they become available and are verified by the continuous integration (CI) workflow.

---

## Documentation

The full project documentation includes installation guides, API documentation, usage examples, and design notes.

The latest documentation is available on the
[project website](https://bas-man.github.io/goodreads-normalizer/).

---

## Project Goals

The project is designed to provide:

- deterministic normalization
- typed models
- reusable Python API
- command-line tooling
- validation of Goodreads data
- consistent output suitable for further processing

---

## Roadmap

Planned improvements include:

- editor detection and normalization
- translator detection and normalization
- additional author normalization datasets
- additional import and export formats
- convenience constructors such as `Book.from_goodreads()`

---

## Contributing

Bug reports, feature requests, and pull requests are welcome.

If you are planning a significant change, please open an issue first so the proposed approach can be discussed.

---

## Development

Clone the repository:

```bash
git clone https://github.com/Bas-Man/goodreads-normalizer.git
cd goodreads-normalizer
```

Install the project and development dependencies:

```bash
uv sync --locked
```

Install the Git hooks:

```bash
uv run pre-commit install
```

Run the same quality checks performed by the continuous integration (CI) workflow:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy src/goodreads_normalizer
uv run pytest
uv build
uv run twine check dist/*
```

### Documentation

Documentation is built using **Great Docs**, which depends on **Quarto**.

Before building the documentation, install Quarto by following the instructions at:

https://quarto.org/docs/get-started/

Then install the documentation dependencies:

```bash
uv sync --group great-docs
```

Build the documentation:

```bash
uv run great-docs build
```

Preview the documentation locally:

```bash
uv run great-docs preview
```

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

## Acknowledgements

This project would not be possible without the availability of Goodreads library exports and the work of the open-source Python community.

---
## Disclaimer

This project is an independent utility and is not affiliated with Goodreads or Amazon.

Users are responsible for ensuring they have the right to process any data used with this software.
