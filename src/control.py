import click
import os
import json

from __init__ import __version__
from capture import setup_capture
from logger import setup_logging
from utils.configure_mics import (
    read_interface_config,
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
@click.option("--active", is_flag=True, help="Show only active interface")
def list_mics(active: bool) -> None:
    """List available microphones."""
    if active:
        config = read_interface_config()
        if config:
            active_interface_id = config["interface_id"]
            click.echo("Active interface:")
            click.echo(list_microphones(active_only=True, active_id=active_interface_id))
        else:
            click.echo("No active interface configured.")
    else:
        config = read_interface_config()
        active_interface_id = config.get("interface_id") if config else None
        click.echo("Available microphones:")
        click.echo(list_microphones(active_only=False, active_id=active_interface_id))

@mics.command("set")
@click.argument("device_index", type=int, nargs=-1)
def set_mics(device_index: int) -> None:
    """Set active microphones."""
    click.echo("Active microphones:")
    click.echo(set_microphones(device_index))

cli.add_command(start)
