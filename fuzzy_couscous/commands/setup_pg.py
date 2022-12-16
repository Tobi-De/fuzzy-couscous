import subprocess

import typer

from ..utils import get_current_dir_as_project_name


def setup_postgres(
    db_name: str = typer.Argument(get_current_dir_as_project_name),
    user: str = typer.Option("postgres", "-u", "--user", help="The postgres username"),
    password: str = typer.Option(
        "",
        "-p",
        "--postgres-pass",
        prompt=True,
        prompt_required=False,
        hide_input=True,
        help="The postgres password.",
    ),
):
    """
    Create a new postgresql database that matches the name of the current directory,
    write a .env file and run migrations
    """
    # todo: save the details somewhere and reuse them
    #   ask to run this on the make command

    # run create db
    subprocess.run(["createdb", db_name, "-U", user], input=password)

    # write-env
    # run manage.py migrate
