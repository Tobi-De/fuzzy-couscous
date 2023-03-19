from pathlib import Path

from fuzzy_couscous.main import cli
from typer.testing import CliRunner

runner = CliRunner()

PYPROJECT_FILE = """
[tool.cuzzy]
work = { server = "python manage.py runserver --nostatic", "tailwind" = "poe t" }
"""


# def test_work(tmp_path: Path):
#     result = runner.invoke(cli, ["work", "--dry-run"])
#
#     print(result.output)
#
#     assert (
#         "{'server' : 'python manage.py migrate && python manage.py runserver --nostatic'}"
#         in result.output
#     )
