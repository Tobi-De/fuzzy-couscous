from __future__ import annotations

from dict_deep import deep_get

from .utils import get_author_email_from
from .utils import get_author_name_from


def convert_build_backend() -> dict:
    # for now the backend is set to hatch
    return {
        "requires": ["hatchling"],
        "build-backend": "hatchling.build",
    }


def convert_project_details(config: dict, default_project_name: str) -> dict:
    """
    converts some of the base key found in too.poetry like name, version to project keys
    """
    too_poetry = deep_get(config, "tool.poetry")

    project = {
        "name": too_poetry.get("name", default_project_name),
        "version": too_poetry.get("version", "0.1.0"),
    }

    optional_same_type_keys = [
        "description",
        "readme",
        "license",
        "classifiers",
        "keywords",
    ]
    for key in optional_same_type_keys:
        value = too_poetry.get(key)
        if value:
            project[key] = value

    return project


def convert_project_urls(config: dict) -> dict:
    keys = ["homepage", "repository", "documentation"]
    urls = {}
    for key in keys:
        value = deep_get(config, f"tool.poetry.{key}")
        if value:
            urls[key.title()] = value
    return urls


def convert_project_scripts(config: dict) -> dict:
    scripts = deep_get(config, "tool.poetry.scripts") or {}
    return scripts


def convert_python_requirement(config: dict) -> str:
    poetry_deps = deep_get(config, "tool.poetry.dependencies")
    constraint = poetry_deps.pop("python")
    return convert_dependency_specification("python", constraint).replace("python", "")


def convert_authors(config: dict) -> list:
    poetry_authors = deep_get(config, "tool.poetry.authors") or []
    return [
        {
            "name": get_author_name_from(p_author),
            "email": get_author_email_from(p_author),
        }
        for p_author in poetry_authors
    ]


def convert_dependency_specification(package: str, constraint: str | dict) -> str:
    # todo: refactor
    if isinstance(constraint, dict):
        extras: list[str] = constraint.get("extras")
        extras_str = ",".join(extras)
        package = f"{package}[{extras_str}]"

        constraint = constraint.get("version")

    version = constraint.replace("^", "").replace("~", "")
    if constraint.startswith("^"):
        return f"{package}>={version}"
    if constraint.startswith("~"):
        return f"{package}~={version}"
    return f"{package}=={version}"


def convert_project_dependencies(config: dict) -> list:
    poetry_deps = deep_get(config, "tool.poetry.dependencies")
    deps = list(poetry_deps)
    # django-improved-user is a special case here, we need to fix it version at 2.0a2
    try:
        improved_user_index = deps.index("django-improved-user")
    except ValueError:
        return deps
    deps.remove("django-improved-user")
    deps.insert(improved_user_index, "django-improved-user==2.0a2")
    return deps


def convert_optional_dependencies(config: dict) -> dict:
    dev_deps = deep_get(config, "tool.poetry.group.dev.dependencies")
    groups = {}
    if not dev_deps:
        # try the old format:
        dev_deps = deep_get(config, "tool.poetry.dev-dependencies")

    if dev_deps:
        groups["dev"] = list(dev_deps)

    poetry_deps_groups = deep_get(config, "tool.poetry.group")
    for group in poetry_deps_groups:
        group_deps = poetry_deps_groups.get(group).get("dependencies")
        groups[group] = list(group_deps)

    return groups
