"""The ``within-reach`` command line.

The package is a scaffold: the hot-reload and screen-capture features that will live here (and that ``in-reach`` and
``in-reach-ide`` will depend on) are not written yet. The commands exist so the entry point, packaging and release flow
are real from the start, and say plainly that they don't do anything yet.
"""

from __future__ import annotations

import click


@click.group()
@click.version_option(package_name="within-reach")
def main() -> None:
    """within-reach: hot reload and screen capture helpers."""


@main.command(name="hot-reload")
def hot_reload() -> None:
    """Push a rebuilt game variant into a running game (not implemented yet)."""
    click.echo("within-reach hot-reload: not implemented yet", err=True)
    raise click.exceptions.Exit(2)


@main.command(name="grab")
def grab() -> None:
    """Capture the game window and read its text (not implemented yet)."""
    click.echo("within-reach grab: not implemented yet", err=True)
    raise click.exceptions.Exit(2)
