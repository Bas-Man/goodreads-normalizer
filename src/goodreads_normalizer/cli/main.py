from pathlib import Path
import typer

from goodreads_normalizer.io.csv import (
    GoodreadsImportError,
    load_csv,
    export_to_stream,
    NameFormatter,
)

app = typer.Typer(help="Goodreads CSV Cleaner and Formatter CLI")


@app.command()
def main(
    file_path: Path = typer.Option(
        ...,  # Use ... to make this argument required, or change to a default Path
        "-f",
        "--file",
        help="Path to the Goodreads CSV export file.",
        exists=True,  # Typer built-in check: ensures the file exists before running
        file_okay=True,  # Validates it's a file, not a directory
        readable=True,  # Validates permissions are readable
    ),
    output: typer.FileTextWrite = typer.Option(
        "-",  # "-" is the standard POSIX convention for stdout
        "-o",
        "--output",
        help="Output file path (defaults to standard output if omitted).",
        encoding="utf-8",
    ),
    short: bool = typer.Option(
        False,
        "-s",
        "--short",
        help="Run format with short behavior (custom logic to be defined).",
    ),
    long: bool = typer.Option(
        False,
        "-l",
        "--long",
        help="Run format with long behavior (custom logic to be defined).",
    ),
):
    """Cleans, normalizes, and rewrites a Goodreads CSV export.

    Reads a Goodreads CSV export, applies name-formatting rules, and
    writes the normalized result to the given output.

    \b
    Examples:
      normalize-goodreads -f export.csv
      normalize-goodreads -f export.csv -o clean.csv --short
      normalize-goodreads -f export.csv -o clean.csv -l

    Options:
        -s / --short (N)
        -l / --long (Narrator)
    """
    if short and long:
        typer.secho(
            "Error: Cannot specify both --short (-s) and --long (-l).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)
    try:
        typer.echo(f"Reading file: {file_path}")
        books = load_csv(file_path)

    except GoodreadsImportError as err:
        # Typer styling for error messages
        typer.secho(str(err), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    name_format: NameFormatter = NameFormatter.name
    if short:
        typer.echo("Applying short formatting rules...")
        name_format = NameFormatter.short
    elif long:
        typer.echo("Applying long formatting rules...")
        name_format = NameFormatter.long

    export_to_stream(books, output, name_format)

    typer.secho(f"Successfully processed {len(books)} books!", fg=typer.colors.GREEN)


click_app = typer.main.get_command(app)

if __name__ == "__main__":
    app()
