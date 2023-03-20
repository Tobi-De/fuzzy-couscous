from __future__ import annotations

import os
import sys
from collections import ChainMap
from pathlib import Path

import typer
from dict_deep import deep_get
from dotenv import dotenv_values
from fuzzy_couscous.utils import get_current_dir_as_project_name
from fuzzy_couscous.utils import read_toml
from fuzzy_couscous.utils import RICH_INFO_MARKER
from honcho.manager import Manager as HonchoManager
from rich import print as rich_print

__all__ = ["work"]


def _get_user_commands(file: Path) -> dict:
    try:
        config = read_toml(file)
    except FileNotFoundError:
        return {}
    return deep_get(config, "tool.cuzzy.work") or {}


def work(
    pyproject_file: Path = typer.Option(Path("pyproject.toml"), hidden=True),
    project_name: str = typer.Argument(
        "", callback=get_current_dir_as_project_name, hidden=True
    ),
    dry_run: bool = typer.Option(False),
):
    """Run multiple processes in parallel."""

    django_env = {
        **dotenv_values(".env"),
        **os.environ,
        "PYTHONPATH": Path().resolve(strict=True),
        "PYTHONUNBUFFERED": "true",
    }

    commands = {
        "server": "python manage.py migrate && python manage.py runserver --nostatic",
    }

    if "REDIS_URL" in django_env:
        redis_url = django_env["REDIS_URL"]
        if "localhost" in redis_url or "127.0.0.1" in redis_url:
            redis_port = redis_url.split(":")[-1]
            if "/" in redis_port:
                redis_port = redis_port.split("/")[0]
                commands["redis"] = f"redis-server --port {redis_port}"

    if pyproject_file.exists():
        config = read_toml(pyproject_file)["tool"]["poetry"][""]
        dependencies = deep_get(config, "tool.poetry.dependencies") or {}
        if "pytailwindcss" in dependencies:
            commands[
                "tailwind"
            ] = f"tailwindcss -i {project_name}/static/css/input.css -o {project_name}/static/css/output.css --watch"

        commands = ChainMap(_get_user_commands(pyproject_file), commands)

    if dry_run:
        rich_print(f"{RICH_INFO_MARKER} Work with:")
        rich_print(dict(commands))

        raise typer.Exit()

    manager = HonchoManager()

    for name, cmd in commands.items():
        manager.add_process(name, cmd, env=django_env)

    manager.loop()

    sys.exit(manager.returncode)
