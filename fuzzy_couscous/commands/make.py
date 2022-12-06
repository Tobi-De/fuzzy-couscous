import secrets
import shutil
import subprocess
from enum import Enum
from pathlib import Path

import typer
from rich import print as rich_print
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

from ..utils import clean_project_name
from ..utils import RICH_INFO_MARKER
from ..utils import RICH_SUCCESS_MARKER

__all__ = ["make_project"]


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

    rich_print(msg)
