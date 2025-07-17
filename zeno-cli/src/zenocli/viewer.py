import typer
import subprocess

app: typer.Typer = typer.Typer(help="Viewer controls")


@app.command()
def dev() -> None:
    """Launch viewer in dev mode."""
    subprocess.run(["yarn", "dev", "--host"], cwd="../zeno-viewer")


@app.command()
def select(overlay: str) -> None:
    """Switch viewer overlay/chart/visual."""
    typer.echo(f"📈 Switching viewer overlay to: {overlay}")
