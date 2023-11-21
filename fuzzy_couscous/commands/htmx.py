from __future__ import annotations

from pathlib import Path
from typing import Annotated

import cappa
import httpx
from rich import print as rich_print
from rich.panel import Panel
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
                progress.add_task(f"Downloading htmx version {version}", total=None)
                response = httpx.get(url)
        except httpx.ConnectError as e:
            raise cappa.Exit(f"Connection error, {url} is not reachable.", code=1) from e

        if response.status_code == 404:
            raise cappa.Exit(f"Could not find htmx version {version}.", code=1)

        filepath = self.output if str(self.output).endswith(".js") else self.output / "htmx.min.js"
        filepath.write_text(response.content.decode("utf-8"))

        subtitle = (
            "You are using the latest version of htmx."
            if version == latest_version
            else f"The latest version available is {latest_version}"
        )
        rich_print(
            Panel(
                f"[green]htmx version {version} downloaded successfully to {filepath} ![/green]",
                subtitle=subtitle,
            )
        )

    @staticmethod
    def get_latest_tag() -> str:
        response = httpx.get("https://api.github.com/repos/bigskysoftware/htmx/releases/latest")
        return response.json()["tag_name"][1:]
