from pathlib import Path

from fuzzy_couscous.main import cli
from typer.testing import CliRunner

runner = CliRunner()


def test_htmx_download(tmp_path: Path):
    result = runner.invoke(cli, ["htmx"])

    assert "SUCCESS" in result.output
    assert (tmp_path / "htmx.min.js").exists()


def test_htmx_download_with_extension(tmp_path: Path):
    result = runner.invoke(cli, ["htmx", "-e", "class-tools"])

    assert "SUCCESS" in result.output
    assert (tmp_path / "class-tools.js").exists()


def test_htmx_download_with_version(tmp_path: Path):
    result = runner.invoke(cli, ["htmx", "1.7.0"])

    assert "SUCCESS" in result.output
    assert (tmp_path / "htmx.min.js").exists()


def test_htmx_download_with_version_and_extension(tmp_path: Path):
    result = runner.invoke(cli, ["htmx", "1.7.0", "-e", "class-tools"])

    assert "SUCCESS" in result.output
    assert (tmp_path / "class-tools.js").exists()


def test_htmx_download_with_output_file(tmp_path: Path):
    result = runner.invoke(cli, ["htmx", "-f", "output.js"])

    assert "SUCCESS" in result.output
    assert (tmp_path / "output.js").exists()


def test_htmx_download_with_output_dir(tmp_path: Path):
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    result = runner.invoke(cli, ["htmx", "-d", "output_dir"])

    assert "SUCCESS" in result.output
    assert (output_dir / "htmx.min.js").exists()


def test_htmx_download_with_web_types(tmp_path: Path):
    result = runner.invoke(cli, ["htmx", "--web-types"])

    assert "SUCCESS" in result.output
    assert (tmp_path / "htmx.web-types.json").exists()
