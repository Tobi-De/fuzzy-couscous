from pathlib import Path

from dict_deep import deep_get
from fuzzy_couscous.main import cli
from fuzzy_couscous.utils import read_toml
from typer.testing import CliRunner

runner = CliRunner()

PYPROJECT_FILE = """
[tool.poetry]
name = "couscous"
version = "0.1.0"
description = ""
authors = ["Tobi-De <tobidegnon@proton.me>"]
repository = "https://github.com/Tobi-De/couscous"
homepage = "https://tobi-de.github.io/couscous/"
documentation = "https://tobi-de.github.io/couscous"
license = ""
readme = "README.md"
packages = [{ include = "mark" }]

[tool.poetry.dependencies]
python = "^3.11"
Django = "^4.1.3"
django-environ = "^0.9.0"
django-anymail = {extras = ["amazon-ses"], version = "^8.6"}
django-improved-user = "2.0a2"

whitenoise = { extras = ["brotli"], version = "^6.2.0" }

[tool.poetry.group.dev.dependencies]
django-browser-reload = "^1.6.0"
django-debug-toolbar = "^3.7.0"

[tool.poetry.scripts]
fuzzy-couscous = "fuzzy_couscous.main:cli"
cuzzy = "fuzzy_couscous.main:cli"

[tool.poe.tasks]
r = { cmd = "python manage.py runserver --nostatic", help = "Start dev serve" }

line-length = 120
"""


def test_remove_poetry(tmp_path: Path, monkeypatch):
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text(PYPROJECT_FILE)
    result = runner.invoke(cli, ["remove-poetry"])

    assert "SUCCESS" in result.output

    pyproject_config = read_toml(tmp_path / pyproject_toml)

    deps = deep_get(pyproject_config, "project.dependencies")

    assert deep_get(pyproject_config, "tool.poetry") is None
    assert deep_get(pyproject_config, "build-system.build-backend") == "hatchling.build"
    assert deep_get(pyproject_config, "project.name") == "couscous"
    assert deep_get(pyproject_config, "project.requires-python") == ">=3.11"
    assert "dev" in deep_get(pyproject_config, "project.optional-dependencies")
    assert deep_get(pyproject_config, "project.authors")[0]["name"] == "Tobi-De"
    assert (
        deep_get(pyproject_config, "project.authors")[0]["email"]
        == "tobidegnon@proton.me"
    )
    assert "Django" in deps
    assert "django-improved-user==2.0a2" in deps

    projects_url = deep_get(pyproject_config, "project.urls")

    assert projects_url == {
        "Repository": "https://github.com/Tobi-De/couscous",
        "Homepage": "https://tobi-de.github.io/couscous/",
        "Documentation": "https://tobi-de.github.io/couscous",
    }

    scripts = deep_get(pyproject_config, "project.scripts")
    assert scripts == {
        "fuzzy-couscous": "fuzzy_couscous.main:cli",
        "cuzzy": "fuzzy_couscous.main:cli",
    }
