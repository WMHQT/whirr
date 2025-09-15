import click

from __init__ import __version__
from capture import setup_capture
from logger import setup_logging
from utils.configure_mics import (
    list_microphones,
    set_microphones,
)
from utils.draw_logo import draw_logo


@click.group(invoke_without_command=True)
@click.version_option(__version__)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Real-time road sounds inference app."""
    if ctx.invoked_subcommand is None:
        click.echo(draw_logo())
        click.echo(cli.get_help(ctx))


@cli.command()
def start() -> None:
    """Start recording."""
    click.echo("Start recording...")
    setup_logging()
    setup_capture()


@cli.group()
def mics() -> None:
    """Microphones settings."""
    pass


@click.command("list")
def list_mics() -> None:
    """List available microphones."""
    click.echo("Available microphones:")
    click.echo(list_microphones())


@click.command("set")
@click.argument("device_index", type=int, nargs=-1)
def set_mics(device_index: int) -> None:
    """Set active microphones."""
    click.echo("Active microphones:")
    click.echo(set_microphones(device_index))


mics.add_command(list_mics)
mics.add_command(set_mics)

cli.add_command(start)
