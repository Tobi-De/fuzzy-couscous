import secrets
from pathlib import Path

from dotenv import dotenv_values, set_key

from ..utils import get_current_dir_as_project_name


def write_env_file(args):
    project_name = get_current_dir_as_project_name()
    default_values = {
        "DJANGO_DEBUG": True,
        "DJANGO_SECRET_KEY": secrets.token_urlsafe(64),
        "DJANGO_ALLOWED_HOSTS": "*",
        "DATABASE_URL": f"postgres:///{project_name}",
        "DJANGO_SUPERUSER_EMAIL": "",
        "DJANGO_SUPERUSER_PASSWORD": "",
    }

    config = {
        **dotenv_values(".env.template"),
        **default_values,
        **dotenv_values(".env"),
    }

    if args.fill_missing:
        for key, value in config.items():
            if not value:
                config[key] = input(f"{key}: ")

    # create .env file
    env_file = Path() / args.output_file
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
