from __future__ import annotations

from pathlib import Path

from dict_deep import deep_get

from ...utils import read_toml


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
