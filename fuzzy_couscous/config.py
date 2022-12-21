from __future__ import annotations

import secrets
import zipfile
from pathlib import Path

import httpx
import typer
from fuzzy_couscous.utils import download_archive

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


APP_NAME = "fuzzy-couscous"


class Branch(StrEnum):
    main = "main"
    tailwind = "tailwind"
    bootstrap = "bootstrap"


def _get_project_template_folder(root_folder: Path) -> str:
    # the structure of the repo folder we expect is as follows:
    # root / templates / project_name / ...
    # root in the case of my template is fuzzy-couscous, project_name must be two levels deep
    return str((root_folder / "templates" / "project_name").resolve(strict=True))


def get_template_dir(repo: str, branch: Branch) -> str | None:
    app_dir = Path(typer.get_app_dir(APP_NAME))
    app_dir.mkdir(exist_ok=True, parents=True)
    # check if connection is available
    # use existing folder if it exists, if not quit
    # if connexion is available
    # download the archive, extract it, save it and return back the path

    username, repository = repo.split("/")

    # for each user we save their templates in a folder named after their username
    templates_folder = app_dir / username
    templates_folder.mkdir(exist_ok=True, parents=True)

    try:
        # download the archive
        archive_url = f"https://github.com/{repo}/archive/{branch}.zip"
        archive_path = app_dir / f"{secrets.token_urlsafe(32)}.zip"
        download_archive(archive_url, archive_path)
    except httpx.ConnectError:
        # if we can't connect to github and a folder for the repo and branch specified doesn't
        # exist, we can't do anything
        if not (templates_folder / f"{repository}-{branch}").exists():
            return None
    else:
        # extract the archive in the folder matching the username
        zipfile.ZipFile(archive_path).extractall(app_dir / username)

        # we delete the archive after extraction since we don't need it anymore
        archive_path.unlink()

    return _get_project_template_folder(templates_folder / f"{repository}-{branch}")
