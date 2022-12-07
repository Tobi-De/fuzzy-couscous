from pathlib import Path

from dotenv import dotenv_values
from fuzzy_couscous.main import cli
from typer.testing import CliRunner

runner = CliRunner()


def test_write_env(tmp_path: Path):
    result = runner.invoke(cli, ["write-env"])

    assert "SUCCESS" in result.output
    assert (tmp_path / ".env").exists()


def test_write_env_with_template(tmp_path: Path):
    env_template = tmp_path / ".env.template"
    env_template.write_text("DJANGO_SPECIAL_KEY=")
    result = runner.invoke(cli, ["write-env"])

    env_file_content = dotenv_values(".env")

    assert "SUCCESS" in result.output
    assert "DJANGO_SPECIAL_KEY" in env_file_content


def test_write_env_to_output(tmp_path: Path):
    result = runner.invoke(cli, ["write-env", "-o", "output.env"])
    output_env = tmp_path / "output.env"

    output_env_file_content = dotenv_values(output_env)

    assert "SUCCESS" in result.output
    assert output_env.exists()
    assert "DJANGO_SECRET_KEY" in output_env_file_content


def test_write_env_priority_order(tmp_path: Path):
    original_env = tmp_path / ".env"
    original_env.write_text("DJANGO_SPECIAL_KEY=my_special_key")

    env_template = tmp_path / ".env.template"
    env_template.write_text("DJANGO_SPECIAL_KEY=")

    result = runner.invoke(cli, ["write-env"])

    env_file_content = dotenv_values(".env")

    assert "SUCCESS" in result.output
    assert "DJANGO_SECRET_KEY" in env_file_content
    assert env_file_content["DJANGO_SPECIAL_KEY"] == "my_special_key"


def test_write_env_postgres_pass(tmp_path: Path):
    runner.invoke(cli, ["write-env", "-p"], input="password")

    env_file_content = dotenv_values(".env")

    assert "password" in env_file_content["DATABASE_URL"]
