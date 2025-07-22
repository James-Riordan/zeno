import typer
import webbrowser

app: typer.Typer = typer.Typer(help="🖼️ Zeno Viewer commands")

@app.command()
def open() -> None:
    """Open the Zeno Viewer in the browser."""
    url = "http://localhost:5173"
    typer.echo(f"🌐 Opening viewer at {url}...")
    webbrowser.open(url)

@app.command()
def status() -> None:
    """Check if viewer is up (placeholder)."""
    typer.echo("📡 Viewer status: (not implemented)")
