from dataclasses import dataclass, field
import cappa
from typing import Any, Literal
from typing_extensions import Annotated
import rich


from .commands import Make, HtmxExt

   


@cappa.command(help="Download the latest version of htmx.")
class Htmx:
    pass



@cappa.command(help="Clean up all migrations.")
class RmMigrations:
    pass


@cappa.command(help="Remove poetry from your project.")
class RmPoetry:
    pass


@cappa.command(help="Run multiple processes in parallel.")
class Work:
    pass


@cappa.command(help="Update or create a .env file from a .env.template file.")
class WriteEnv:
    pass


@cappa.command(
    help="Initialize a new django project using the fuzzy-couscous project template.",
    description="""This is a wrapper around the django-admin startproject command using my custom project template at
    https://github.com/Tobi-De/fuzzy-couscous. This cli also includes some additional commands to make setting up
    a new project faster.
    """,
)
class Toji:
    subcommand: cappa.Subcommands[
        Make | Htmx | HtmxExt | RmMigrations | RmPoetry | Work | WriteEnv
    ]


def main():
    cappa.invoke(Toji)


if __name__ == "__main__":
    main()
