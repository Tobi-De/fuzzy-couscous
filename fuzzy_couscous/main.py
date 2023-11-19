import cappa

from .commands import Htmx
from .commands import HtmxExtension
from .commands import Make
from .commands import RmMigrations
from .commands import RmPoetry
from .commands import Work
from .commands import WriteEnv


@cappa.command(
    help="Initialize a new django project using the fuzzy-couscous project template.",
    description="""This is a wrapper around the django-admin startproject command using my custom project template at
    https://github.com/Tobi-De/fuzzy-couscous. This cli also includes some additional commands to make setting up
    a new project faster.
    """,
)
class Cuzzy:
    subcommand: cappa.Subcommands[Make | Htmx | HtmxExtension | RmMigrations | RmPoetry | Work | WriteEnv]


def main():
    cappa.invoke(Cuzzy)


if __name__ == "__main__":
    main()
