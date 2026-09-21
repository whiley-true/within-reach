"""The ``within-reach`` command line.

``detect`` is real: it runs the same detection the IDE's "Verify System Settings" does (Tesseract on ``PATH``, the Steam
and Halo: MCC folders and everything derived from them). ``hot-reload`` and ``grab`` are placeholders for features that will
live here and are not written yet; they say plainly that they don't do anything.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import click

from within_reach import env_file, system_verify


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


def detect_all(*, which=None, home: Path | None = None, username: str | None = None, steam_default: Path | None = None) -> list[dict]:
    """Runs every step of the verification checklist against this machine and reports what each found, in order.

    Nothing of yours is read or written: the run works in a scratch ``.env``, accepting each step that resolved to a single
    answer so later steps derive from it (the Halo folders from the Steam one, and so on), as a full pass of the IDE's
    checklist does -- but without its side effects on the machine (see below). A step with several candidates is reported with them and not accepted (it is the user's pick); a
    step that found nothing says so, with where it looked.

    The keyword arguments are for tests, as on :class:`~within_reach.system_verify.VerifyRun`."""
    options = {k: v for k, v in (("which", which), ("home", home), ("username", username), ("steam_default", steam_default)) if v is not None}
    report = []
    with tempfile.TemporaryDirectory(prefix="within-reach-detect-") as scratch:
        run = system_verify.VerifyRun(Path(scratch), **options)
        for step in system_verify.STEPS:
            result = run.check(step)
            if result.outcome is system_verify.Outcome.FOUND:
                # Not run.accept(): that also has side effects on the real machine (accepting the personal gametype folder
                # creates Halo's matching maps folder). Storing the value in the scratch .env is all a later step needs to
                # derive from it.
                env_file.update_env_value(run.env_path, step.env_key, result.value)
            report.append(
                {
                    "key": step.env_key,
                    "label": step.label,
                    "outcome": result.outcome.value,
                    "value": result.value,
                    "detail": result.detail,
                    "choices": [{"value": c.value, "label": c.label} for c in result.choices],
                }
            )
    return report


@main.command(name="detect")
@click.option("--format", "fmt", type=click.Choice(["text", "json"]), default="text", show_default=True)
def detect(fmt: str) -> None:
    """Detect Tesseract and the Halo / Steam folders on this machine (nothing is written).

    Exits 1 if a step found nothing, so a script can tell whether the machine is ready."""
    report = detect_all()
    if fmt == "json":
        click.echo(json.dumps({"schema": 1, "steps": report}, indent=2))
    else:
        for row in report:
            mark = {"found": "ok ", "choice": "?? ", "missing": "-- "}[row["outcome"]]
            click.echo(f"{mark}{row['label']}: {row['value'] or row['detail'] or '(nothing found)'}")
            for choice in row["choices"]:
                click.echo(f"      candidate: {choice['label']}")
    if any(row["outcome"] == "missing" for row in report):
        raise click.exceptions.Exit(1)
