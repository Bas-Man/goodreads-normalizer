# Goodreads Normalizer

A Python library and command-line application for cleaning, validating, and normalizing Goodreads library exports.

Goodreads exports are an excellent way to back up your library, but the exported data is often inconsistent. Author names, series information, ISBNs, dates, shelves, and other metadata can vary significantly, making it difficult to analyse, migrate, or integrate with other cataloguing systems.

**Goodreads Normalizer** provides deterministic normalization using strongly typed Pydantic models, allowing your Goodreads data to be transformed into clean, validated, machine-readable records.

---

## Features

- 📚 Read Goodreads CSV exports
- ✨ Normalize author names
- 👤 Validate author metadata
- 📝 Normalize editors, translators, and narrators
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
- editors included as authors
- translators stored inconsistently
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

## Command Line Usage

Normalize a Goodreads export:

```bash
goodreads-normalizer \
    --file goodreads_export.csv \
    --output normalized.csv
```

or

```bash
goodreads-normalizer -f goodreads_export.csv -o normalized.csv
```

Display help:

```bash
goodreads-normalizer --help
```

---

## What Gets Normalized?

Current areas include:

- Author names
- Editors
- Translators
- Narrators
- Series names
- Series numbers
- ISBN values
- Empty values
- Date parsing
- Validation

The project deliberately avoids changing data that cannot be normalized with confidence.

---

## Development

Clone the repository:

```bash
git clone https://github.com/Bas-Man/goodreads-normalizer.git
cd goodreads-normalizer
```

Install dependencies:

```bash
uv sync
```

To update documentation:
```bash
uv sync --group great-docs
uv run great-docs build
uv run great-docs preview
```

Run the test suite:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check
```

Format the code:

```bash
uv run ruff format
```

---

## Supported Python Versions

The project supports modern versions of Python.

See `pyproject.toml` for the current minimum supported version.

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

Future work includes:

- additional author normalization datasets
- improved editor and translator normalization
- additional export formats

---

## Contributing

Bug reports, feature requests, and pull requests are welcome.

If you are planning a significant change, please open an issue first so the proposed approach can be discussed.

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

## License

MIT
