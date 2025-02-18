import typer

app = typer.Typer()

@app.command()
def summarize():
    """Prints Hello World"""
    print("Hello World")

if __name__ == "__main__":
    app()
