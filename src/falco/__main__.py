import cappa

from falco.commands import (
    Htmx,
    HtmxExtension,
    StartProject,
    RmMigrations,
    Work,
    WriteEnv,
)


@cappa.command(
    help="Initialize a new django project using the falco project template.",
    description="""This is a wrapper around the django-admin startproject command using my custom project template at
    https://github.com/Tobi-De/falco. This cli also includes some additional commands to make setting up
    a new project faster.
    """,
)
class Cuzzy:
    subcommand: cappa.Subcommands[
        StartProject | Htmx | HtmxExtension | RmMigrations | Work | WriteEnv
    ]


def main():
    cappa.invoke(Cuzzy)


if __name__ == "__main__":
    main()
