import argparse
import subprocess
from pathlib import Path
import shutil
import secrets
from dotenv import dotenv_values, set_key


SUCCESS = "\x1b[1;32m [SUCCESS]: "
INFO = "\x1b[1;33m [INFO]: "
TERMINATOR = "\x1b[0m"


def clean_project_name(val):
    return val.strip().replace(" ", "_").replace("-", "_")


def make_project(args):
    project_name = clean_project_name(args.project_name)

    # run the django-admin command
    subprocess.run(
        [
            "django-admin",
            "startproject",
            project_name,
            "--template",
            f"https://github.com/{args.repo}/archive/{args.branch}.zip",
            "-e=py,html,toml,md,json,js,sh",
        ]
    )

    # since the root dir and the real project dir have the same name, rename the root to avoid conflict
    project_root_dir = Path() / project_name
    project_root_new_dir = Path() / f"_root_{project_root_dir}"
    project_root_dir.rename(str(project_root_new_dir))

    # move the real project dir to the current working directory
    project_dir = project_root_new_dir / project_name
    new_project_dir = Path() / project_name
    shutil.move(project_dir, new_project_dir)

    # delete the root dir
    shutil.rmtree(project_root_new_dir)

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)
    print(
        INFO
        + "If you like the project consider dropping a star at https://github.com/Tobi-De/fuzzy-couscous"
        + TERMINATOR
    )


def write_env_file(args):
    current_dir = Path().resolve(strict=True).stem
    project_name = clean_project_name(current_dir)
    defaul_values = {
        "DJANGO_DEBUG": True,
        "DJANGO_SECRET_KEY": secrets.token_urlsafe(64),
        "DJANGO_ALLOWED_HOSTS": "*",
        "DATABASE_URL": f"postgres:///{project_name}",
        "DJANGO_SUPERUSER_EMAIL": "",
        "DJANGO_SUPERUSER_PASSWORD": "",
    }

    config = {
        **dotenv_values(".env.template"),
        **defaul_values,
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


def cli():
    """
    A basic script that initializes a django project from my fuzzy-couscous project template.
    The purpose of this script is to remove unnecessary folders and files from the generated template.
    It is also a shortcut to avoid typing the full django-admin command with all the options.
    """
    parser = argparse.ArgumentParser(
        prog="fuzzy-couscous",
        description="Initialize a new django project using the fuzzy-couscous project template.",
    )

    subparsers = parser.add_subparsers(help="sub-command help")

    parser_make = subparsers.add_parser("make", help="Initialize a new project")
    parser_make.add_argument("project_name")
    parser_make.add_argument("-b", "--branch", default="main")
    parser_make.add_argument("-r", "--repo", default="Tobi-De/fuzzy-couscous")
    parser_make.set_defaults(handler=make_project)

    parser_env = subparsers.add_parser(
        "write-env", help="Update or create a .env file from a .env.template file"
    )
    parser_env.add_argument(
        "-f", "--fill-missing", action="store_true", help="Fill missing values"
    )
    parser_env.add_argument(
        "-o",
        "--output-file",
        default=".env",
        help="The output filename, default to .env",
    )
    parser_env.set_defaults(handler=write_env_file)

    args = parser.parse_args()
    args.handler(args)
