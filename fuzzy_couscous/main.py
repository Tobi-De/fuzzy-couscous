import typer

from fuzzy_couscous.commands import make_project, remove_poetry, work, write_env_file


def get_app():
    app = typer.Typer(
        name="fuzzy-couscous alias cuzzy",
        short_help="Initialize a new django project using the fuzzy-couscous project template.",
        help="""This is a wrapper around the django-admin startproject  command using my custom project template at 
        https://github.com/Tobi-De/fuzzy-couscous. This cli also includes some additional features to make setting up 
        a new project faster.""",
    )

    app.command(name="make")(make_project)
    app.command(name="work")(work)
    app.command(name="remove-poetry")(remove_poetry)
    app.command(name="write-env")(write_env_file)
    return app


cli = get_app()

if __name__ == "__main__":
    cli()
