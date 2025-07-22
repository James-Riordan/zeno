import typer
import subprocess

app: typer.Typer = typer.Typer(help="🧱 Docker Compose commands for Zeno")

@app.command()
def up(dev: bool = typer.Option(False, "--dev", "-d", help="Use docker-compose.dev.yml")) -> None:
    """Start Zeno services via docker-compose."""
    file = "docker-compose.dev.yml" if dev else "docker-compose.yml"
    typer.echo(f"📦 Starting services with {file}...")
    subprocess.run(["docker-compose", "-f", file, "up", "--build"], check=False)

@app.command()
def down(dev: bool = typer.Option(False, "--dev", "-d", help="Use docker-compose.dev.yml")) -> None:
    """Stop Zeno services via docker-compose."""
    file = "docker-compose.dev.yml" if dev else "docker-compose.yml"
    typer.echo(f"🧹 Stopping services with {file}...")
    subprocess.run(["docker-compose", "-f", file, "down"], check=False)

@app.command()
def logs(service: str = typer.Argument(None, help="Optional service name")) -> None:
    """View logs from docker-compose services."""
    cmd = ["docker-compose", "logs", "-f"]
    if service:
        cmd.append(service)
    typer.echo("📜 Streaming logs...")
    subprocess.run(cmd, check=False)
