from pathlib import Path
from typing import Annotated

import cappa
import httpx
from fuzzy_couscous.utils import RICH_ERROR_MARKER
from rich import print as rich_print

THIRD_PARTY_REGISTRY = {
    "htmx-template": {
        "download_url": "https://raw.githubusercontent.com/KatrinaKitten/htmx-template/master/htmx-template.min.js",
        "info": "https://github.com/KatrinaKitten/htmx-template",
    },
    "hx-take": {
        "download_url": "https://github.com/oriol-martinez/hx-take/blob/main/dist/hx-take.min.js",
        "info": "https://github.com/oriol-martinez/hx-take",
    },
}


@cappa.command(help="Download one of htmx extensions.")
class HtmxExtension:
    name: Annotated[
        str | None,
        cappa.Arg(
            None,
            help="The name of the extension to download.",
        ),
    ]
    version: str = cappa.Arg(
        "latest",
        short="-v",
        long="--version",
        help="The version of htmx to use to look for the extension.",
    )
    output: Path = cappa.Arg(
        default=Path.cwd(),
        help="The directory to write the downloaded file to.",
        short="-o",
        long="--output",
    )

    def __call__(self) -> None:
        if self.name:
            self.download()
        else:
            self.list_all()

    def download(self):
        metadata = self.registry().get(self.name, {})
        if not metadata:
            rich_print(f"{RICH_ERROR_MARKER} Could not find extension {self.name}.")
            raise cappa.Exit()

        download_url = metadata.get("download_url")
        response = httpx.get(download_url)
        if self.output.is_file():
            self.output.unlink(missing_ok=True)
            self.output.touch()
            self.output.write_text(response.text)
        else:
            self.output.mkdir(parents=True, exist_ok=True)
            (self.output / f"{self.name}.js").write_text(response.text)

    def list_all(self):
        all_extensions = list(self.registry().keys())
        rich_print("\n".join(all_extensions))

    def registry(self):
        return THIRD_PARTY_REGISTRY | self.official_registry(self.version)

    @classmethod
    def official_registry(cls, htmx_version: str):
        base_url = f"https://unpkg.com/htmx.org@{htmx_version}/dist/ext/"  # noqa
        # scrape the site to get the list of extensions
        return {}
