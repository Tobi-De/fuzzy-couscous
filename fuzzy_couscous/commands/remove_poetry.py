from __future__ import annotations

import subprocess
from copy import deepcopy
from pathlib import Path

import typer
from dict_deep import deep_del, deep_get, deep_set
from rich import print as rich_print

from ..utils import (
    get_current_dir_as_project_name,
    read_toml,
    write_toml,
)


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
    """Remove poetry as a dependency of your project"""

    config = read_toml(pyproject_file)

    if not pyproject_file.exists():
        rich_print(
            "[red]ERROR: No pyproject.toml file was found in the current directory :sad:"
        )
        return

    is_poetry_project = bool(deep_get(config, "tool.poetry"))

    if not is_poetry_project:
        rich_print("[red]ERROR: It seems that this is not a poetry project :sad:")
        return

    new_config = deepcopy(config)

    # build-backend
    build_system = {
        "requires": ["hatchling"],
        "build-backend": "hatchling.build",
    }
    new_config.update({"build-system": build_system})

    # tool.poetry
    _poetry_base_metadata_to_project(new_config, project_name=project_name)

    # project dependencies
    poetry_deps = deep_get(new_config, "tool.poetry.dependencies")
    poetry_deps.pop("python")
    deep_set(new_config, "project.dependencies", _project_deps_from(poetry_deps))

    # group / dev dependencies in poetry to optional dependencies
    _poetry_dep_group_to_project_optional_deps(new_config)

    # project.authors
    _poetry_authors_to_project_authors(new_config)

    # remove every config related to poetry
    deep_del(new_config, "tool.poetry")

    if not new_config.get("tool"):
        new_config.pop("tool")

    msg = (
        "[green]SUCCESS: Poetry has been removed as a dependency from your project, check the updated pyproject.toml"
        " to see what has changed."
    )

    new_config = dict(sorted(new_config.items()))
    write_toml(pyproject_file, new_config)

    if not create_virtualenv:
        return

    _create_virtualenv()
    msg += (
        "\n[blue]INFO: A new environment has been created using virtualenv, "
        "you activate it with the command [yellow] source venv/bin/activate"
    )
    msg += (
        "\n[blue] To install your dependencies you need to generated a "
        "requirements.txt file with [yellow] pip-compile -o requirements.txt pyproject.toml --resolver=backtracking"
    )

    # add a poethepoet task if the tool was found in the config file
    result = _add_poe_requirements_compile_task(new_config)
    write_toml(pyproject_file, new_config)
    if result:
        msg += (
            "\n[blue]INFO: poethepoet was found in your pyproject.toml file, a task to generate the "
            "requirements.txt file was added, run it with [yellow] poe d"
        )

    msg += (
        "[blue]INFO: Then run [yellow]pip-sync [blue] to install the dependencies, "
        "more infos on pip-tools docs https://pip-tools.readthedocs.io/en/latest/"
    )

    # todo: give instructions for groups
    rich_print(msg)


def _get_author_email_from(poetry_author: str) -> str:
    less_than_index = poetry_author.index("<")
    greater_than_index = poetry_author.index(">")
    return poetry_author[less_than_index + 1 : greater_than_index]


def _get_author_name_from(poetry_author: str) -> str:
    email = _get_author_email_from(poetry_author)
    name = poetry_author.replace(f"<{email}>", "")
    return name.strip()


def _poetry_base_metadata_to_project(config: dict, project_name: str) -> None:
    """
    converts some of the base key found in too.poetry like name, version to project keys
    """
    too_poetry = deep_get(config, "tool.poetry")

    # basic metadata
    project = {
        "name": too_poetry.get("name", project_name),
        "version": too_poetry.get("version", "0.1.0"),
    }

    optional_same_type_keys = ["description", "license", "classifiers", "keywords"]
    for key in optional_same_type_keys:
        value = too_poetry.get(key)
        if value:
            project[key] = value

    # python requirements
    # todo: this is static now, update to convert from what is defined in the poetry config
    project["requires-python"] = ">=3.10"

    config.update({"project": project})


def _poetry_authors_to_project_authors(config: dict):
    poetry_authors = deep_get(config, "tool.poetry.authors")
    if not poetry_authors:
        return
    authors = [
        {
            "name": _get_author_name_from(p_author),
            "email": _get_author_email_from(p_author),
        }
        for p_author in poetry_authors
    ]
    deep_set(config, "project.authors", authors)


def _convert_poetry_deps_marker(package: str, constraint: str) -> str:
    version = constraint.replace("^", "").replace("~", "")
    if constraint.startswith("^"):
        return f"{package}>={version}"
    if constraint.startswith("~"):
        return f"{package}~={version}"
    return f"{package}=={version}"


def _project_deps_from(
    poetry_deps: dict,
) -> list:
    return [
        _convert_poetry_deps_marker(package, constraint)
        for package, constraint in poetry_deps.items()
    ]


def _poetry_dep_group_to_project_optional_deps(config: dict):
    dev_deps = deep_get(config, "tool.poetry.group.dev.dependencies")
    groups = {}
    if not dev_deps:
        # try the old format:
        dev_deps = deep_get(config, "tool.poetry.dev-dependencies")

    if dev_deps:
        groups["dev"] = _project_deps_from(dev_deps)

    poetry_deps_groups = deep_get(config, "tool.poetry.group")
    for group in poetry_deps_groups:
        group_deps = poetry_deps_groups.get(group).get("dependencies")
        groups[group] = _project_deps_from(group_deps)

    deep_set(config, "project.optional-dependencies", groups)


def _create_virtualenv():
    # specify command to compile and sync and point to docs for more infos
    commands = [
        "python -m pip install --upgrade virtualenv",
        "python -m virtualenv --prompt . venv",
        "venv/bin/python -m pip install pip-tools hatch",
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)


def _add_poe_requirements_compile_task(config: dict) -> dict | None:
    poe_tasks = deep_get(config, "tool.poe.tasks")
    if not poe_tasks:
        return
    poe_tasks["d"] = {
        "cmd": "pip-compile -o requirements.txt pyproject.toml --resolver=backtracking",
        "help": "Generate requirements.txt file",
    }
    deep_set(config, "tool.poe.tasks", poe_tasks)
    return dict(sorted(config.items()))
