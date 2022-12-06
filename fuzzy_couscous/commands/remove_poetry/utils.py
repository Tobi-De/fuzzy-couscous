from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from dict_deep import deep_get

from ...utils import read_toml
from ...utils import RICH_COMMAND_MARKER
from ...utils import RICH_COMMAND_MARKER_END
from ...utils import RICH_INFO_MARKER


def get_author_email_from(poetry_author: str) -> str:
    less_than_index = poetry_author.index("<")
    greater_than_index = poetry_author.index(">")
    return poetry_author[less_than_index + 1 : greater_than_index]


def get_author_name_from(poetry_author: str) -> str:
    email = get_author_email_from(poetry_author)
    name = poetry_author.replace(f"<{email}>", "")
    return name.strip()


def get_updated_poe_tasks(config: dict) -> dict:
    poe_tasks = deep_get(config, "tool.poe.tasks")
    if not poe_tasks:
        return {}
    poe_tasks["d"] = {
        "cmd": "pip-compile -o requirements.txt pyproject.toml --resolver=backtracking",
        "help": "Generate requirements.txt file",
    }
    return poe_tasks


def get_poe_message_for_compile_task() -> str:
    return (
        f"\n{RICH_INFO_MARKER} poethepoet was found in your pyproject.toml file, a task to generate the "
        f"requirements.txt file was added, run it with {RICH_COMMAND_MARKER} poe d"
    )


def remove_empty_top_level_table(config: dict) -> None:
    # removing values from a dictionary while iterating through it is not a good idea, hence this copy
    config_copy = deepcopy(config)
    for key, value in config_copy.items():
        if not value:
            config.pop(key)


def sort_config(config: dict) -> dict:
    return dict(sorted(config.items()))


def is_valid_poetry_project(pyproject_file: Path) -> tuple[dict, str | None]:
    if not pyproject_file.exists():
        return (
            {},
            "No pyproject.toml file was found in the current directory :disappointed_face:",
        )

    config = read_toml(pyproject_file)

    is_poetry_project = bool(deep_get(config, "tool.poetry"))
    if not is_poetry_project:
        return {}, "It seems that this is not a poetry project :disappointed_face:"

    return config, None


def get_message_for_optional_deps(config: dict) -> str:
    at_least_one_group_defined = bool(deep_get(config, "project.optional-dependencies"))

    if at_least_one_group_defined:
        return (
            f"\n{RICH_INFO_MARKER} Your project defines optional dependencies, to generate a requirements.txt file "
            f"that includes the dependencies of a group, add a "
            f"{RICH_COMMAND_MARKER}--extra <group_name>{RICH_COMMAND_MARKER_END} option to the pip-compile command"
        )


def get_message_for_new_virtualenv() -> str:
    msg = (
        f"{RICH_INFO_MARKER} A new environment has been created using virtualenv, "
        f"you activate it with the command {RICH_COMMAND_MARKER}source venv/bin/activate"
    )
    msg += (
        f"\n{RICH_INFO_MARKER} To install your dependencies you need to generated a "
        f"requirements.txt file with "
        f"{RICH_COMMAND_MARKER}pip-compile -o requirements.txt pyproject.toml --resolver=backtracking"
    )
    return msg
