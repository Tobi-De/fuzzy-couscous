from __future__ import annotations

import os
import sys
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


def _get_venv_directory() -> str | None:
    patterns = ["venv", ".venv"]
    for p in patterns:
        path = Path(p)
        if path.exists() and (path / "bin/python").exists():
            return p


def _get_user_commands(file: Path) -> dict:
    try:
        config = read_toml(file)
        return deep_get(config, "tool.cuzzy.work") or {}
    except FileNotFoundError:
        return {}


def _get_redis_command(django_env: dict) -> str | None:
    redis_url = django_env["REDIS_URL"]
    if "localhost" in redis_url or "127.0.0.1" in redis_url:
        redis_port = redis_url.split(":")[-1]
        if "/" in redis_port:
            redis_port = redis_port.split("/")[0]
            return f"redis-server --port {redis_port}"


def _get_tailwind_command(pyproject_file: Path, project_name: str) -> str | None:
    config = read_toml(pyproject_file)
    dependencies = deep_get(config, "tool.poetry.dependencies") or {}
    if "pytailwindcss" in dependencies:
        return f"tailwindcss -i {project_name}/static/css/input.css -o {project_name}/static/css/output.css --watch"


def work(
    pyproject_file: Path = typer.Option(Path("pyproject.toml"), hidden=True),
    project_name: str = typer.Argument(
        "", callback=get_current_dir_as_project_name, hidden=True
    ),
    dry_run: bool = typer.Option(False),
) -> None:
    """Run multiple processes in parallel."""

    django_env = {
        **dotenv_values(".env"),
        **os.environ,
        "PYTHONPATH": Path().resolve(strict=True),
        "PYTHONUNBUFFERED": "true",
    }

    venv_dir = _get_venv_directory()

    if venv_dir:
        runserver_cmd = (
            f"{venv_dir}/bin/python manage.py migrate && "
            f"{venv_dir}/bin/python manage.py runserver --nostatic"
        )
    else:
        runserver_cmd = (
            "python manage.py migrate && python manage.py runserver --nostatic"
        )
    commands = {
        "server": runserver_cmd,
    }

    if redis_cmd := _get_redis_command(django_env):
        commands["redis"] = redis_cmd

    if pyproject_file.exists():
        if tailwind_cmd := _get_tailwind_command(pyproject_file, project_name):
            commands["tailwind"] = tailwind_cmd

    user_commands = _get_user_commands(pyproject_file)
    if venv_dir:
        for name, cmd in user_commands.items():
            if cmd.startswith("python"):
                user_commands[name] = f"{venv_dir}/bin/{cmd}"

    commands.update(user_commands)

    if dry_run:
        rich_print(f"{RICH_INFO_MARKER} Work with:")
        rich_print(dict(commands))

        raise typer.Exit()

    manager = HonchoManager()

    for name, cmd in commands.items():
        manager.add_process(name, cmd, env=django_env)

    manager.loop()

    sys.exit(manager.returncode)
