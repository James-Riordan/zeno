import typer
import subprocess

app: typer.Typer = typer.Typer(help="Docker Compose controls")


@app.command()
def up(dev: bool = typer.Option(False, "--dev")) -> None:
    """Start services via docker-compose."""
    file: str = "docker-compose.dev.yml" if dev else "docker-compose.yml"
    typer.echo(f"📦 Starting services from {file}")
    subprocess.run(["docker-compose", "-f", file, "up", "--build"])


@app.command()
def logs(service: str = typer.Argument(...)) -> None:
    """Stream logs for a given service."""
    subprocess.run(["docker-compose", "logs", "-f", service])
