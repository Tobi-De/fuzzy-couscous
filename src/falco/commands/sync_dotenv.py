from __future__ import annotations

import secrets
from pathlib import Path
from typing import Annotated

import cappa
from dotenv import dotenv_values, set_key
from rich import print as rich_print
from rich.prompt import Prompt

from falco.utils import get_current_dir_as_project_name


@cappa.command(help="Synchronize the .env file with the .env.template file")
class SyncDotenv:
    fill_missing: Annotated[
        bool,
        cappa.Arg(
            False,
            short="-f",
            long="--fill-missing",
            help="Prompt to fill missing values.",
        ),
    ]

    def __call__(
        self, project_name: Annotated[str, cappa.Dep(get_current_dir_as_project_name)]
    ):
        dotenv_file = Path(".env")
        dotenv_template_file = Path(".env.template")

        default_values = {
            "DJANGO_DEBUG": True,
            "DJANGO_SECRET_KEY": secrets.token_urlsafe(64),
            "DJANGO_ALLOWED_HOSTS": "*",
            "DATABASE_URL": f"postgres:///{project_name}",
            "DJANGO_SUPERUSER_EMAIL": "",
            "DJANGO_SUPERUSER_PASSWORD": "",
        }

        config = {
            **dotenv_values(dotenv_template_file),
            **default_values,
            **dotenv_values(dotenv_file),
        }

        if self.fill_missing:
            for key, value in config.items():
                if not value:
                    config[key] = Prompt.ask(f"{key}")

        sorted_config = dict(sorted(config.items(), key=lambda x: str(x[0])))

        # empty .env and write values
        dotenv_file.write_text("")
        for key, value in sorted_config.items():
            set_key(
                dotenv_file,
                key,
                value,
                quote_mode="never",
                export=False,
                encoding="utf-8",
            )

        # empty and write to .env.template file
        original_values = dotenv_values(dotenv_template_file)
        dotenv_template_file.write_text("")
        for key, value in sorted_config.items():
            set_key(
                dotenv_template_file,
                key,
                original_values.get(key, ""),
                quote_mode="never",
                export=False,
                encoding="utf-8",
            )

        rich_print(
            f"[green] {dotenv_file} and {dotenv_template_file} synchronised [/green]"
        )
