from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import typer
from dict_deep import deep_del
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
from .utils import get_message_for_new_virtualenv
from .utils import get_message_for_optional_deps
from .utils import get_poe_message_for_compile_task
from .utils import get_updated_poe_tasks
from .utils import is_valid_poetry_project
from .utils import remove_empty_top_level_table
from .utils import sort_config
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

    msg += get_message_for_optional_deps(new_config)

    remove_empty_top_level_table(new_config)
    new_config = sort_config(new_config)
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

    msg = get_message_for_new_virtualenv()

    poe_tasks = get_updated_poe_tasks(new_config)
    if poe_tasks:
        deep_set(new_config, "tool.poe.tasks", poe_tasks)
        msg += get_poe_message_for_compile_task()

    remove_empty_top_level_table(new_config)
    new_config = sort_config(new_config)
    write_toml(pyproject_file, new_config)

    # a note on using pip-sync
    msg += (
        f"\n{RICH_INFO_MARKER} Run {RICH_COMMAND_MARKER}pip-sync{RICH_COMMAND_MARKER_END} to install the dependencies, "
        "more infos on pip-tools docs https://pip-tools.readthedocs.io/en/latest/"
    )

    rich_print(msg)
