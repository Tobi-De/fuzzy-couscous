from pathlib import Path

from dict_deep import deep_get
from fuzzy_couscous.main import cli
from fuzzy_couscous.utils import read_toml
from typer.testing import CliRunner

runner = CliRunner()

basic_files_and_folder = [
    "manage.py",
    "pyproject.toml",
    "docker",
    "config",
    "config/settings.py",
]


def test_make(tmp_path):
    result = runner.invoke(cli, ["make", "couscous"])
    project_path = tmp_path / "couscous"

    assert "SUCCESS" in result.stdout
    for f in basic_files_and_folder:
        assert (project_path / f).exists()


def test_make_tailwind(tmp_path: Path):
    result = runner.invoke(cli, ["make", "couscous", "-b", "tailwind"])
    project_path = tmp_path / "couscous"
    toml_config = read_toml(project_path / "pyproject.toml")
    deps = deep_get(toml_config, "tool.poetry.dependencies")

    assert "SUCCESS" in result.stdout
    assert "pytailwindcss" in deps
    tailwind_config_file = project_path / "tailwind.config.js"
    assert tailwind_config_file.exists()
    for f in basic_files_and_folder:
        assert (project_path / f).exists()


def test_make_bootstrap(tmp_path: Path):
    result = runner.invoke(cli, ["make", "couscous", "-b", "bootstrap"])
    project_path = tmp_path / "couscous"
    toml_config = read_toml(project_path / "pyproject.toml")
    deps = deep_get(toml_config, "tool.poetry.dependencies")

    assert "SUCCESS" in result.stdout
    assert "django-bootstrap5" in deps
    for f in basic_files_and_folder:
        assert (project_path / f).exists()
