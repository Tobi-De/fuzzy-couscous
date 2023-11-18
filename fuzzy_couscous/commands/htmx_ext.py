from typing import Any
import cappa

from pathlib import Path

THIRD_PARY_REGISTRY = {
    "htmx-template": {
        "file": "https://raw.githubusercontent.com/KatrinaKitten/htmx-template/master/htmx-template.min.js",
        "url": "https://github.com/KatrinaKitten/htmx-template",
    },
    "hx-take": {
        "file": "https://github.com/oriol-martinez/hx-take/blob/main/dist/hx-take.min.js",
        "url": "https://github.com/oriol-martinez/hx-take",
    },
}



@cappa.command(help="Download one of htmx extensions.")
class HtmxExt:
    name: str | None = cappa.Arg(
        None,
        help="The name of the extension to download.",
        choices=THIRD_PARY_REGISTRY.keys(),
    )
    version: str = cappa.Arg(
        "latest",
        short="-v",
        long="--version",
        help="The version of htmx to use to look for the extension.",
    )
    output : Path = cappa.Arg(default=Path.cwd(), help="The directory to write the downloaded file to.", short="-o", long="--output")


    def __call__(self) -> None:
        if self.name:
            self.download(self.name)
        else:
            self.list_all()

    
    def download(self):
        pass
    
    def list_all(self):
        pass

    @classmethod
    def official_regitry(cls, htmx_version: str):
        base_url = f"https://unpkg.com/htmx.org@{htmx_version}/dist/ext/"
        

