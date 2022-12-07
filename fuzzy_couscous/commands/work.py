from __future__ import annotations

import subprocess
from pathlib import Path

import typer
from dict_deep import deep_get
from rich import print as rich_print

from ..utils import read_toml
from ..utils import RICH_COMMAND_MARKER
from ..utils import RICH_ERROR_MARKER
from ..utils import RICH_INFO_MARKER

__all__ = ["work"]


def __get_venv_directory() -> str | None:
    patterns = ["venv", ".venv"]
    for p in patterns:
        if Path(p).exists() and (Path(p) / "bin/python").exists():
            return p


def _get_commands_from_user_pyproject(file: Path) -> list:
    try:
        config = read_toml(file)
    except FileNotFoundError:
        return []
    commands = deep_get(config, "tool.cuzzy.work") or []
    return commands if isinstance(commands, list) else []


def work(
    commands: list[str] = typer.Option(
        list,
        "-c",
        "--command",
        help="The command to run.",
    ),
    pyproject_file: Path = typer.Option(Path("pyproject.toml"), hidden=True),
):
    """Run multiple commands in parallel."""

    if not commands:
        commands = _get_commands_from_user_pyproject(pyproject_file)

    if not commands:
        rich_print(
            f"{RICH_ERROR_MARKER} provide commands via the cli option or via your pyproject.toml file. "
            f"{RICH_INFO_MARKER}\ncuzzy work -c 'command 1' -c 'command 2'\n"
            f"OR\n"
            f"\[tool.cuzzy]\n"
            f"work = ['command 1', 'command 2']"
        )
        raise typer.Abort()

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
