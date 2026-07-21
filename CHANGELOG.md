## v0.1.1 (2026-07-21)

### Fix

- **ruff**: Ruff fixes
- **ruff**: Fixes requested by ruff

## v0.1.0 (2026-07-15)

### Feat

- **cli**: Cli now supports -s -l flags
- **csv**: Update import/exports of csv
- **main**: Work on normalizer cli
- **model:Narrator**: Add tagging after name
- **Series**: Add is_collection property
- **model**: Add access to original_title
- **model**: Add original_title data
- **model**: converts the shelves into lists
- **model**: Add read_count valiation
- **model**: add additional csv fields and update Author/Narrator
- **transform**: Transform Author and Additional_Authors
- **book**: change author from str to authors: list[Author]
- **book**: Add ISBN ISBN13 and year_published data
- **book**: Add Binding data to Book
- **model**: Add Publisher data from goodreads csv
- **model**: Update Narrator Object and tests
- **model**: Add features to Author Object
- **data**: Add FIX_STRANGE_NAMES
- **model**: Add pen name suppport for Author
- **data**: Add PEN_NAME_TO_NAME mapping
- **model**: Add Author model
- **validation**: Add author name validation and tests
- **data**: Add known Author and Narrator data lists
- **data**: Add google and microsoft virual narration voices
- **parser**: Add regex and parser code for handing "Title"
- **model**: add normalisation for author with extra whitespace
- **parser/model**: Add book_id from "Book Id" as this will be useful later as part of the yaml file creation
- **models**: Add basic models which will be expanded upon
- **Add-goodreads-parser**: Add an initial parser for goodreads CSV data
- **rating**: add rating normalization

### Fix

- **data**: Update the Author/Narrator data
- **great-docs**: Switch from numpy to google docstrings
- **docs**: Fixes so that cli command appears
- **tests**: oiginal_title_name
- **data**: Remove invalid name from English Author list
- **data**: remove Lee Child from narrator list
- **data**: Sort known_* lists and add a Translators list
- **models**: move normalize_author_name prevent circular import
- **normalize**: Improve author normalization
- **scripts**: add scripts for checking data against regex patterns
- **pyproject**: Remove pandas not required
- **pyproject**: Update the pyproject files to include "black" and update versions and build

### Refactor

- **data**: Refactor data imports
- **BookTitleData**: make use of Series @props
- **Series**: Simple refactor value check
- **model**: Use field_validation numbers
- **model:Book**: Refactor title processing
- **parser**: rename normalize_title
- **scripts**: Update classify_titles to use standard regexes
- **parsers**: Improve "Title" processing
- **data**: 🎨 simplify virtual narrator import
- **name**: 🚧 Rename Project to goodreads-normalizer
- **models**: Rename BookTitle -> BookTitleData
