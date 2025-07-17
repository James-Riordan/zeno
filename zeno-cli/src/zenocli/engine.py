import typer

app: typer.Typer = typer.Typer(help="Engine commands")


@app.command()
def attach(pid: int) -> None:
    """Attach to a running engine process."""
    typer.echo(f"🔗 Attaching to engine process {pid}")


@app.command()
def status() -> None:
    """Show engine status."""
    typer.echo("📊 Engine status: (not implemented)")
