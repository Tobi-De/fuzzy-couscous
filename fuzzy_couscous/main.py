import typer

from .commands import make_project
from .commands import remove_poetry
from .commands import rm_migrations
from .commands import work
from .commands import write_env_file
from .config import APP_NAME


def get_app():
    app = typer.Typer(
        name=APP_NAME,
        short_help="Initialize a new django project using the fuzzy-couscous project template.",
        help="""This is a wrapper around the django-admin startproject  command using my custom project template at
        https://github.com/Tobi-De/fuzzy-couscous. This cli also includes some additional commands to make setting up
        a new project faster.""",
    )

    app.command(name="make")(make_project)
    app.command(name="work")(work)
    app.command(name="remove-poetry")(remove_poetry)
    app.command(name="write-env")(write_env_file)
    app.command(name="rm-migrations")(rm_migrations)
    return app


cli = get_app()

if __name__ == "__main__":
    cli()
