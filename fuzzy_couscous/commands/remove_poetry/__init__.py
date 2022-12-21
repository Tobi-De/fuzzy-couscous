from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import typer
from dict_deep import deep_del
from dict_deep import deep_get
from dict_deep import deep_set
from rich import print as rich_print
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

from . import config_converters
from ...utils import get_current_dir_as_project_name
from ...utils import RICH_COMMAND_MARKER
from ...utils import RICH_COMMAND_MARKER_END
from ...utils import RICH_ERROR_MARKER
from ...utils import RICH_INFO_MARKER
from ...utils import RICH_SUCCESS_MARKER
from ...utils import write_toml
from .utils import get_updated_poe_tasks
from .utils import is_valid_poetry_project
from .virtualenv_ import compile_requirements
from .virtualenv_ import install_dependencies
from .virtualenv_ import new_virtualenv

__all__ = ["remove_poetry"]


def remove_poetry(
    create_virtualenv: bool = typer.Option(
        False,
        "-c",
        "--create-virtualenv",
        is_flag=True,
        help="Create an environment using virtualenv",
    ),
    pyproject_file: Path = typer.Argument(Path("pyproject.toml"), hidden=True),
    project_name: str = typer.Argument(
        "", callback=get_current_dir_as_project_name, hidden=True
    ),
) -> None:
    """
    Run this command to remove poetry as a dependency from your project, it updates your pyproject.toml file
    to use HATCH as the build-system and can optionally create a virtual environment using virtualenv.
    """

    old_config, error_message = is_valid_poetry_project(pyproject_file)

    if error_message:
        rich_print(f"{RICH_ERROR_MARKER} {error_message}")
        raise typer.Abort()

    new_config = deepcopy(old_config)

    build_system = config_converters.convert_build_backend()
    new_config.update({"build-system": build_system})

    # project basic metadata, name, description, etc.
    project_details = config_converters.convert_project_details(
        new_config, default_project_name=project_name
    )
    new_config.update({"project": project_details})

    project_urls = config_converters.convert_project_urls(new_config)
    deep_set(new_config, "project.urls", project_urls)

    project_scripts = config_converters.convert_project_scripts(new_config)
    deep_set(new_config, "project.scripts", project_scripts)

    python_requirement = config_converters.convert_python_requirement(new_config)
    deep_set(new_config, "project.requires-python", python_requirement)

    authors = config_converters.convert_authors(new_config)
    deep_set(new_config, "project.authors", authors)

    project_dependencies = config_converters.convert_project_dependencies(new_config)
    deep_set(new_config, "project.dependencies", project_dependencies)

    optional_dependencies = config_converters.convert_optional_dependencies(new_config)
    deep_set(new_config, "project.optional-dependencies", optional_dependencies)

    # remove poetry config
    deep_del(new_config, "tool.poetry")

    # remove poetry.lock if is exists
    Path("poetry.lock").unlink(missing_ok=True)

    msg = (
        f"{RICH_SUCCESS_MARKER} Poetry has been removed as a dependency from your project, "
        f"check the updated pyproject.toml to see what has changed."
    )

    write_toml(pyproject_file, new_config)

    rich_print(msg)

    if not create_virtualenv:
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Creating virtualenv... :boom:", total=None)
        new_virtualenv()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(
            description="Compiling requirements.txt... :boom:", total=None
        )
        dev_group = deep_get(new_config, "project.optional-dependencies.dev")
        groups = ["dev"] if dev_group else []
        compile_requirements(groups=groups)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Installing dependencies... :boom:", total=None)
        install_dependencies()

    msg = (
        f"{RICH_INFO_MARKER} A new environment has been created using virtualenv, "
        f"you activate it with the command {RICH_COMMAND_MARKER}source venv/bin/activate"
    )
    msg += (
        f"\n{RICH_INFO_MARKER} To install your dependencies you need to generate a "
        f"requirements.txt file with \n"
        f"{RICH_COMMAND_MARKER}pip-compile -o requirements.txt pyproject.toml --resolver=backtracking"
    )

    at_least_one_group_defined = bool(
        deep_get(new_config, "project.optional-dependencies")
    )

    if at_least_one_group_defined:
        msg += (
            f"\n{RICH_INFO_MARKER} Your project defines optional dependencies, to generate a requirements.txt file "
            f"that includes the dependencies of a group, add a "
            f"{RICH_COMMAND_MARKER}--extra group_name{RICH_COMMAND_MARKER_END} option to the pip-compile command"
        )

    msg += f"\n{RICH_INFO_MARKER} For the first run, we have already compiled and installed the dependencies for you."

    poe_tasks = get_updated_poe_tasks(new_config)
    if poe_tasks:
        deep_set(new_config, "tool.poe.tasks", poe_tasks)
        msg += (
            f"\n{RICH_INFO_MARKER} poethepoet was found in your pyproject.toml file, a task to generate the "
            f"requirements.txt file was added, run it with {RICH_COMMAND_MARKER} poe d"
        )

    write_toml(pyproject_file, new_config)

    # a note on using pip-sync
    msg += (
        f"\n{RICH_INFO_MARKER} Run {RICH_COMMAND_MARKER}pip-sync{RICH_COMMAND_MARKER_END} to install the dependencies, "
        "more infos on pip-tools docs https://pip-tools.readthedocs.io/en/latest/"
    )

    rich_print(msg)
