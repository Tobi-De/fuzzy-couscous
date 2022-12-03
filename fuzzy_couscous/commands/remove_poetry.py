import subprocess
from copy import deepcopy
from pathlib import Path


import rtoml
from dict_deep import deep_del, deep_get, deep_set

from ..utils import get_current_dir_as_project_name, print_success, print_info


def _get_author_name_from(poetry_author: str) -> str:
    less_than_index = poetry_author.index("<")
    greater_than_index = poetry_author.index(">")
    return poetry_author[less_than_index + 1 : greater_than_index]


def _get_author_email_from(poetry_author: str) -> str:
    name = _get_author_name_from(poetry_author)
    email = poetry_author.replace(f"<{name}>", "")
    return email.strip()


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
    # fixme: the format of this does not match the hatch one, don't know yet if this will
    #   be an issue
    poetry_authors = deep_get(config, "tool.poetry.authors")
    authors = [
        {
            "name": _get_author_name_from(p_author),
            "email": _get_author_email_from(p_author),
        }
        for p_author in poetry_authors
    ]
    authors.append({"name": "jean", "email": "max"})
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
    commands = [
        "python -m pip install --upgrade virtualenv",
        "python -m virtualenv --prompt . venv",
        "venv/bin/python -m pip install pip-tools hatch",
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)


def remove_poetry(args) -> None:
    project_name = get_current_dir_as_project_name()
    pyproject_toml = Path("pyproject.toml")
    config = rtoml.load(pyproject_toml)

    if not pyproject_toml.exists():
        print_info("Failure: No pyproject.toml file was found in the current directory")
        return

    is_poetry_project = bool(deep_get(config, "tool.poetry"))

    if not is_poetry_project:
        print_info("Failure: It seems that this is not a poetry project")
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
    deep_set(new_config, "project.dependencies", _project_deps_from(poetry_deps))

    # group / dev dependencies in poetry to optional dependencies
    _poetry_dep_group_to_project_optional_deps(new_config)

    # project.authors
    _poetry_authors_to_project_authors(new_config)

    if not new_config.get("tool"):
        new_config.pop("tool")

    # remove every config related to poetry
    deep_del(new_config, "tool.poetry")

    print_success(
        "Poetry was removed as a dependency of your project, "
        "see the updated pyproject.toml to see what has changed"
    )

    rtoml.dump(new_config, file=pyproject_toml, pretty=True)

    if not args.create_virtualenv:
        return

    _create_virtualenv()
    print_info(
        "A new environment was created using virtualenv, you activate it with this command:\n"
        "source venv/bin/activate"
    )
