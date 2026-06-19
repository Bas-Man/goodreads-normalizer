import typer

app = typer.Typer()


@app.command()
def version():
    print("0.1.0")


@app.command()
def export():
    print("exporting")


if __name__ == "__main__":
    app()
