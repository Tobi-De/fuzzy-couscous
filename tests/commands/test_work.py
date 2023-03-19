from pathlib import Path

from fuzzy_couscous.main import cli
from typer.testing import CliRunner

runner = CliRunner()

PYPROJECT_FILE = """
[tool.cuzzy]
work = ["poe r", "poe t"]
"""


# def test_work(tmp_path: Path):
#     result = runner.invoke(cli, ["work", "-c", "poe r"])
#
#     assert "poe r" in result.output
#
#
# def test_work_from_pyproject(tmp_path: Path):
#     pyproject_toml = tmp_path / "pyproject.toml"
#     pyproject_toml.write_text(PYPROJECT_FILE)
#     result = runner.invoke(cli, ["work"])
#
#     assert "poe r" in result.output
#     assert "poe t" in result.output
#
#
# def test_work_with_command(tmp_path: Path):
#     result = runner.invoke(cli, ["work", "-c", "python script.py"])
#
#     assert "python script.py" in result.output


# def test_work_with_venv(tmp_path: Path):
#     (tmp_path / "venv/bin/").mkdir(parents=True)
#     (tmp_path / "venv/bin/python").write_text("")
#     (tmp_path / "venv/bin/python").chmod(mode=777)
#
#     result = runner.invoke(cli, ["work", "-c", "python script.py"])
#
#     print(result.output)
#
#     assert "venv/bin/python script.py" in result.output
