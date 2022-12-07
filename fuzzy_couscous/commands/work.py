from __future__ import annotations

import subprocess
from pathlib import Path

import typer
from rich import print as rich_print

from ..utils import RICH_COMMAND_MARKER
from ..utils import RICH_INFO_MARKER

__all__ = ["work"]


def __get_venv_directory() -> str | None:
    patterns = ["venv", ".venv"]
    for p in patterns:
        if Path(p).exists() and (Path(p) / "bin/python").exists():
            return p


def work(
    commands: list[str] = typer.Option(
        ["poe r", "poe t"],
        "-c",
        "--command",
        help="The command to run.",
    )
):
    """Run multiple commands in parallel."""

    venv_directory = __get_venv_directory()

    msg = ""

    if venv_directory:
        msg += (
            f"{RICH_INFO_MARKER} A <{venv_directory}> directory has been found in the current working directory, "
            f"the interpreter at <{venv_directory}/bin/python> will automatically be used for python commands\n"
        )
        for c in commands.copy():
            if c.startswith("python"):
                script = c.replace("python", "")
                commands.remove(c)
                commands.append(f"{venv_directory}/bin/python {script}")

    commands_display = ", ".join(commands)

    msg += f"{RICH_INFO_MARKER} work with {RICH_COMMAND_MARKER}{commands_display}"

    rich_print(msg)

    processes = []
    for cmd in commands:
        process = subprocess.Popen(cmd, shell=True)
        processes.append(process)

    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        pass
