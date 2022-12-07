from __future__ import annotations

import secrets
import shutil
import subprocess
from enum import Enum
from pathlib import Path

import typer
from dict_deep import deep_set
from rich import print as rich_print
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

from ..utils import clean_project_name
from ..utils import read_toml
from ..utils import RICH_ERROR_MARKER
from ..utils import RICH_INFO_MARKER
from ..utils import RICH_SUCCESS_MARKER
from ..utils import write_toml

__all__ = ["make_project"]


def _get_user_git_infos() -> tuple[str, str] | None:
    git_config_cmd = ["git", "config", "--global", "--get"]
    try:
        user_name_cmd = subprocess.run(
            git_config_cmd + ["user.name"], capture_output=True, text=True
        )
        user_email_cmd = subprocess.run(
            git_config_cmd + ["user.email"], capture_output=True, text=True
        )
    except FileNotFoundError:
        return None
    if user_email_cmd.returncode != 0 or user_email_cmd.returncode != 0:
        return None
    return (
        user_name_cmd.stdout.strip("\n"),
        user_email_cmd.stdout.strip("\n"),
    )


def _set_authors_in_pyproject(file: Path, name: str, email: str) -> None:
    config = read_toml(file)
    deep_set(config, "tool.poetry.authors", [f"{name} <{email}>"])
    write_toml(file, config)


class Branch(str, Enum):
    main = "main"
    tailwind = "tailwind"
    bootstrap = "bootstrap"


def make_project(
    project_name: str = typer.Argument(..., callback=clean_project_name),
    repo: str = typer.Option(
        "Tobi-De/fuzzy-couscous",
        "-r",
        "--repo",
        help="The github repository to pull the template from. The format to use is `username/repo`",
        formats=["username/repo"],
    ),
    branch: Branch = typer.Option(
        "main", "-b", "--branch", help="The github branch to use."
    ),
):
    """Initialize a new django project."""

    if Path(project_name).exists():
        rich_print(
            f"{RICH_ERROR_MARKER} A directory with the name {project_name} already exists in the current directory "
            f":disappointed_face:"
        )
        raise typer.Abort()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(
            description="Initializing your new django project... :sunglasses:",
            total=None,
        )

        # run the django-admin command
        subprocess.run(
            [
                "django-admin",
                "startproject",
                project_name,
                "--template",
                f"https://github.com/{repo}/archive/{branch}.zip",
                "-e=py,html,toml,md,json,js,sh",
                "--exclude=docs",
                "--exclude=fuzzy_couscous",
                "--exclude=.github",
                "--exclude=.idea",
            ]
        )

    # since the root dir and the real project dir have the same name, rename the root to avoid conflict
    project_root_dir = Path(project_name)
    project_root_dir = project_root_dir.rename(
        str(f"_{secrets.token_urlsafe(5)}_{project_root_dir}")
    )

    # move the real project dir to the current working directory
    project_dir = project_root_dir / "templates" / project_name
    new_project_dir = Path(project_name)
    shutil.move(project_dir, new_project_dir)

    # delete the root dir
    shutil.rmtree(project_root_dir)

    msg = f"{RICH_SUCCESS_MARKER} Project initialized, keep up the good work!\n"
    msg += (
        f"{RICH_INFO_MARKER} If you like the project consider dropping a star at "
        f"https://github.com/Tobi-De/fuzzy-couscous"
    )

    user_infos = _get_user_git_infos()
    if user_infos:
        name, email = user_infos
        _set_authors_in_pyproject(
            new_project_dir / "pyproject.toml", name=name, email=email
        )
        msg += (
            f"\n{RICH_INFO_MARKER} A git global user configuration was found and used to update the authors in your "
            f"pyproject.toml file."
        )

    rich_print(msg)
