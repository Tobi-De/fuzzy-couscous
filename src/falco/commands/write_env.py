from __future__ import annotations

import secrets
from pathlib import Path
from typing import Annotated

import cappa
from dotenv import dotenv_values, set_key
from rich import print as rich_print
from rich.prompt import Prompt

from falco.utils import get_current_dir_as_project_name


@cappa.command(help="Update or create a .env file from a .env.template file.")
class WriteEnv:
    fill_missing: Annotated[
        bool,
        cappa.Arg(
            False,
            short="-f",
            long="--fill-missing",
            help="Prompt to fill missing values.",
        ),
    ]
    project_name: Annotated[str, cappa.Arg(parse=get_current_dir_as_project_name, hidden=True)]

    def __call__(
        self,
    ):
        default_values = {
            "DJANGO_DEBUG": True,
            "DJANGO_SECRET_KEY": secrets.token_urlsafe(64),
            "DJANGO_ALLOWED_HOSTS": "*",
            "DATABASE_URL": f"postgres:///{self.project_name}",
            "DJANGO_SUPERUSER_EMAIL": "",
            "DJANGO_SUPERUSER_PASSWORD": "",
        }

        config = {
            **dotenv_values(".env.template"),
            **default_values,
            **dotenv_values(".env"),
        }

        if self.fill_missing:
            for key, value in config.items():
                if not value:
                    config[key] = Prompt.ask(f"{key}")

        # create .env file
        env_file = Path(".env")
        env_file.write_text("")

        # set env values
        for key, value in config.items():
            set_key(
                env_file,
                key,
                value,
                quote_mode="never",
                export=False,
                encoding="utf-8",
            )
        rich_print(f"[green] {env_file} file generated[/green]")
