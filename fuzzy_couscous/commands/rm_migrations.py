from pathlib import Path

import typer
from rich import print as rich_print

from ..utils import RICH_INFO_MARKER


def rm_migrations(
    apps_dir: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        help="The path to your django apps directory.",
    ),
    exclude: list[str] = typer.Option(
        list,
        "-e",
        "--exc",
        help=".",
    ),
):
    """Remove all installed application migrations, intended only for development."""

    excludes = exclude or ["__init__.py"]
    apps = set()
    for folder in apps_dir.iterdir():
        migration_dir = folder / "migrations"
        if not migration_dir.exists():
            continue
        apps.add(folder.stem)
        for file in migration_dir.iterdir():
            if file.suffix == ".py" and file.name not in excludes:
                file.unlink()
    apps_ = ", ".join(apps)
    rich_print(f"{RICH_INFO_MARKER} Removed migration files for apps: {apps_}")
