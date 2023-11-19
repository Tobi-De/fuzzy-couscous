from __future__ import annotations

from pathlib import Path
from typing import Annotated

import cappa
import httpx
from fuzzy_couscous.utils import RICH_ERROR_MARKER
from fuzzy_couscous.utils import RICH_INFO_MARKER
from fuzzy_couscous.utils import RICH_SUCCESS_MARKER
from rich import print as rich_print
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn


@cappa.command(help="Download the latest version of htmx.")
class Htmx:
    version: Annotated[str, cappa.Arg(default="latest")]
    output: Annotated[Path, cappa.Arg(default=Path("htmx.min.js"), short="-o", long="--output")]

    def __call__(self):
        """Download the htmx javascript library or one of its extension if specified."""

        latest_version = self.get_latest_tag()
        version = self.version if self.version != "latest" else latest_version
        url = f"https://unpkg.com/htmx.org@{version}/dist/htmx.min.js"

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                msg = f"htmx version {version}"
                progress.add_task(f"Downloading {msg} :arrow_down:", total=None)
                response = httpx.get(url)
        except httpx.ConnectError as e:
            rich_print(f"{RICH_ERROR_MARKER} Could not connect to {url}")
            raise cappa.Exit() from e

        if response.status_code == 404:
            msg = f"Could not find {version} version of htmx."
            rich_print(f"{RICH_ERROR_MARKER} {msg}")
            raise cappa.Exit()

        if response.status_code != 200:
            rich_print(f"{RICH_ERROR_MARKER} Something went wrong :sad_face: .")
            raise cappa.Exit()

        # write file to disk

        filepath = self.output if self.output.is_file() else self.output / "htmx.min.js"
        filepath.write_text(response.content.decode("utf-8"))

        rich_print(
            f"{RICH_SUCCESS_MARKER} File downloaded successfully to {filepath.name}."
            f"\n{RICH_INFO_MARKER} htmx version: {version}"
        )
        if version != latest_version:
            rich_print(f"{RICH_INFO_MARKER} The latest version available of htmx version is {latest_version}")

    @staticmethod
    def get_latest_tag() -> str:
        response = httpx.get("https://api.github.com/repos/bigskysoftware/htmx/releases/latest")
        return response.json()["tag_name"][1:]
