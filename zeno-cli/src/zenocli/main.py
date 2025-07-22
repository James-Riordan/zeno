from __future__ import annotations
import subprocess
import typer
from typing import Optional
from zenocli import engine, viewer, compose

app: typer.Typer = typer.Typer(
    name="zeno",
    help="🔧 Zeno CLI: Unified Control for Engine, Viewer, and Compose",
    no_args_is_help=True,
    add_completion=False
)

# Subcommands
app.add_typer(engine.app, name="engine", help="Control the simulation engine")
app.add_typer(viewer.app, name="viewer", help="Control the GUI/web viewer")
app.add_typer(compose.app, name="compose", help="Manage Docker Compose environments")


@app.command()
def run(
    scene: str = typer.Option("RTI_2D", "--scene", "-s", help="Scene name"),
    steps: int = typer.Option(500, "--steps", "-n", help="Number of simulation steps"),
    dim: int = typer.Option(2, "--dim", "-d", help="Number of dimensions (1, 2, or 3)"),
    grid: int = typer.Option(128, "--grid", "-g", help="Grid resolution per axis"),
    mode: str = typer.Option("symbolic", "--mode", "-m", help="Simulation mode: symbolic or classical"),
    gui: bool = typer.Option(False, "--gui", "-g", help="Launch viewer GUI alongside simulation"),
) -> None:
    """
    Run simulation with given parameters. Optionally launch GUI.
    """
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

    if gui:
        typer.echo("🖥️ Launching viewer GUI...")
        subprocess.run(["zeno", "viewer", "open"])


@app.command()
def gui() -> None:
    """
    Shortcut to launch GUI viewer.
    """
    typer.echo("🖥️ Launching viewer GUI (not yet implemented)")
    subprocess.run(["zeno", "viewer", "open"])


if __name__ == "__main__":
    app()
