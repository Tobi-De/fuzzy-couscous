from pathlib import Path
from typing import Annotated

import cappa
from rich import print as rich_print


@cappa.command(help="Remove all migrations for the specified applications directory, intended only for development.")
class RmMigrations:
    apps_dir: Annotated[Path, cappa.Arg(help="The path to your django apps directory.")]

    def __call__(self):
        apps = set()
        for folder in self.apps_dir.iterdir():
            migration_dir = folder / "migrations"
            if not migration_dir.exists():
                continue
            apps.add(folder.stem)
            for file in migration_dir.iterdir():
                if file.suffix == ".py" and file.name not in ["__init__.py"]:
                    file.unlink()
        apps_ = ", ".join(apps)
        rich_print(f"[green] Removed migration files for apps: {apps_}")
