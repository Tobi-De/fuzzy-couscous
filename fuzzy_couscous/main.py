import argparse

from .commands import make_project, remove_poetry, work, write_env_file


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

    subparsers = parser.add_subparsers()

    # sub-command to generate a new project
    parser_make = subparsers.add_parser("make", help="Initialize a new project")
    parser_make.add_argument("project_name")
    parser_make.add_argument(
        "-b", "--branch", default="main", choices=["main", "tailwind", "bootstrap"]
    )
    parser_make.add_argument("-r", "--repo", default="Tobi-De/fuzzy-couscous")
    parser_make.set_defaults(handler=make_project)

    # sub-command to create .env
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

    # sub-command to run multiple command at the same time
    parser_work = subparsers.add_parser(
        "work", help="run multiple commands in parallel"
    )
    parser_work.add_argument("-c", "--command", action="append")
    parser_work.set_defaults(handler=work)

    # sub-command to remove poetry as a dependency
    parser_rm_poetry = subparsers.add_parser(
        "remove-poetry", help="Remove poetry as a dependencies"
    )
    parser_rm_poetry.add_argument(
        "-c",
        "--create-virtualenv",
        action="store_true",
        help="Create an environment using virtualenv",
    )
    parser_rm_poetry.set_defaults(handler=remove_poetry)

    args = parser.parse_args()

    try:
        args.handler(args)
    except AttributeError:
        parser.print_help()
