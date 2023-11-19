from __future__ import annotations

import os
import secrets
import shutil
import sys
import zipfile
from pathlib import Path

import httpx
from fuzzy_couscous.utils import download_archive


try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


APP_NAME = "fuzzy-couscous"


def _posixify(name: str) -> str:
    return "-".join(name.split()).lower()


class Branch(StrEnum):
    main = "main"
    tailwind = "tailwind"
    bootstrap = "bootstrap"


def _get_project_template_folder(root_folder: Path) -> str:
    # the structure of the repo folder we expect is as follows:
    # root / templates / project_name / ...
    # root in the case of my template is fuzzy-couscous, project_name must be two levels deep
    return str((root_folder / "templates" / "project_name").resolve(strict=True))


def get_app_dir(app_name: str, roaming: bool = True, force_posix: bool = False) -> str:
    r"""Returns the config folder for the application.  The default behavior
    is to return whatever is most appropriate for the operating system.

    To give you an idea, for an app called ``"Foo Bar"``, something like
    the following folders could be returned:

    Mac OS X:
      ``~/Library/Application Support/Foo Bar``
    Mac OS X (POSIX):
      ``~/.foo-bar``
    Unix:
      ``~/.config/foo-bar``
    Unix (POSIX):
      ``~/.foo-bar``
    Windows (roaming):
      ``C:\Users\<user>\AppData\Roaming\Foo Bar``
    Windows (not roaming):
      ``C:\Users\<user>\AppData\Local\Foo Bar``

    .. versionadded:: 2.0

    :param app_name: the application name.  This should be properly capitalized
                     and can contain whitespace.
    :param roaming: controls if the folder should be roaming or not on Windows.
                    Has no effect otherwise.
    :param force_posix: if this is set to `True` then on any POSIX system the
                        folder will be stored in the home folder with a leading
                        dot instead of the XDG config home or darwin's
                        application support folder.
    """
    if sys.platform.startswith("win"):
        key = "APPDATA" if roaming else "LOCALAPPDATA"
        folder = os.environ.get(key)
        if folder is None:
            folder = os.path.expanduser("~")
        return os.path.join(folder, app_name)
    if force_posix:
        return os.path.join(os.path.expanduser(f"~/.{_posixify(app_name)}"))
    if sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~/Library/Application Support"), app_name)
    return os.path.join(
        os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
        _posixify(app_name),
    )


def get_template_dir(branch: Branch) -> str | None:
    app_dir = Path(get_app_dir(APP_NAME))
    app_dir.mkdir(exist_ok=True, parents=True)
    # check if connection is available
    # use existing folder if it exists, if not quit
    # if connexion is available
    # download the archive, extract it, save it and return back the path

    repo = "Tobi-De/fuzzy-couscous"
    username, repository = repo.split("/")

    # for each user we save their templates in a folder named after their username
    templates_dir = app_dir / username
    templates_dir.mkdir(exist_ok=True, parents=True)

    template_dir = templates_dir / f"{repo}-{branch}"

    try:
        # download the archive
        archive_url = "https://github.com/tobi-de/fuzzy-couscous/archive/main.zip"
        archive_path = app_dir / f"{secrets.token_urlsafe(32)}.zip"
        download_archive(archive_url, archive_path)
    except httpx.ConnectError:
        # if we can't connect to github and a folder for the repo and branch specified doesn't
        # exist, we can't do anything
        if not template_dir.exists():
            return None
    else:
        # remove old folder to avoid reusing old files
        shutil.rmtree(template_dir, ignore_errors=True)
        # extract the archive in the folder matching the username
        zipfile.ZipFile(archive_path).extractall(app_dir / username)

        # we delete the archive after extraction since we don't need it anymore
        archive_path.unlink()

    return _get_project_template_folder(templates_dir / f"{repository}-{branch}")
