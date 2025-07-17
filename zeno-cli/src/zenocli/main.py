import typer
from typing import Optional
from zenocli import engine, viewer, compose

app: typer.Typer = typer.Typer(help="🔧 Zeno CLI: Unified Control for Engine, Viewer, and Compose")

app.add_typer(engine.app, name="engine")
app.add_typer(viewer.app, name="viewer")
app.add_typer(compose.app, name="compose")


@app.command()
def run(
    scene: str = typer.Option("RTI_2D", help="Scene name"),
    steps: int = typer.Option(500),
    dim: int = typer.Option(2),
    grid: int = typer.Option(128),
    mode: str = typer.Option("symbolic", help="Simulation mode: symbolic or classical"),
) -> None:
    """Run simulation directly."""
    import subprocess

    cmd: list[str] = [
        "python", "src/main.py",
        "--scene", scene,
        "--steps", str(steps),
        "--dim", str(dim),
        "--grid", str(grid),
        "--mode", mode,
    ]
    typer.echo(f"🚀 Running simulation: {' '.join(cmd)}")
    subprocess.run(cmd)


@app.command()
def gui() -> None:
    """Launch GUI viewer (placeholder)."""
    typer.echo("🖥️ Launching GUI viewer (not yet implemented)")


if __name__ == "__main__":
    app()
