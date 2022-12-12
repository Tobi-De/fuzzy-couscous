from __future__ import annotations

import secrets
from pathlib import Path

import typer
from dotenv import dotenv_values
from dotenv import set_key
from rich import print as rich_print
from rich.prompt import Prompt

from ..utils import get_current_dir_as_project_name
from ..utils import RICH_SUCCESS_MARKER

__all__ = ["write_env_file"]


def write_env_file(
    fill_missing: bool = typer.Option(
        False,
        "-f",
        "--fill-missing",
        help="Prompt to fill missing values.",
        is_flag=True,
    ),
    output_file: Path = typer.Option(
        ".env", "-o", "--output-file", help="The output file path.", dir_okay=False
    ),
    postgres_pass: str = typer.Option(
        "",
        "-p",
        "--postgres-pass",
        prompt=True,
        prompt_required=False,
        hide_input=True,
        help="Prompt for the postgres password to use to build the DATABASE_URL.",
    ),
    project_name: str = typer.Argument(
        "", callback=get_current_dir_as_project_name, hidden=True
    ),
):
    """Update or create a .env file from a .env.template file."""

    default_values = {
        "DJANGO_DEBUG": True,
        "DJANGO_SECRET_KEY": secrets.token_urlsafe(64),
        "DJANGO_ALLOWED_HOSTS": "*",
        "DATABASE_URL": f"postgres:///{project_name}",
        "DJANGO_SUPERUSER_EMAIL": "",
        "DJANGO_SUPERUSER_PASSWORD": "",
    }
    if postgres_pass:
        default_values[
            "DATABASE_URL"
        ] = f"postgres://postgres:{postgres_pass}@localhost/{project_name}"

    config = {
        **dotenv_values(".env.template"),
        **default_values,
        **dotenv_values(".env"),
    }

    if fill_missing:
        for key, value in config.items():
            if not value:
                config[key] = Prompt.ask(f"{key}")

    # create .env file
    env_file = Path(output_file)
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
    rich_print(f"{RICH_SUCCESS_MARKER} {env_file} file generated")
