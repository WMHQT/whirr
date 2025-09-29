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


@mics.command("list")
@click.option("--active", is_flag=True, help="Show only active interface.")
def list_mics(active: bool) -> None:
    """List available microphones."""
    if active:
        click.echo("Active interface:")
    else:
        click.echo("Available interfaces:")
    click.echo(list_microphones(active))


@mics.command("set")
@click.argument("device_index", type=int, nargs=1)
def set_mics(device_index: int) -> None:
    """Set active microphones."""
    click.echo("Active interface:")
    click.echo(set_microphones(device_index))


cli.add_command(start)