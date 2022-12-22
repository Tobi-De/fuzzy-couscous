from pathlib import Path

from dotenv import dotenv_values
from fuzzy_couscous.main import cli
from typer.testing import CliRunner

runner = CliRunner()


def create_fake_migrations_dir(tmp_path: Path) -> list[Path]:
    migrations_dir = tmp_path / "migrations"
    migrations_dir.mkdir()
    migrations_dir.joinpath("__init__.py").touch()
    migrations_dir.joinpath("0001_initial.py").touch()
    migrations_dir.joinpath("0002_initial.py").touch()
    return [file for file in migrations_dir.iterdir()]


def test_rm_migrations(tmp_path: Path):
    apps_dir = tmp_path / "apps"
    payments_app = apps_dir / "payments"
    payments_app.mkdir(parents=True)
    files = create_fake_migrations_dir(payments_app)

    result = runner.invoke(cli, ["rm-migrations", str(apps_dir)])

    assert "SUCCESS" in result.output
    for file in files:
        if file.name != "__init__.py":
            assert not file.exists()

    assert (payments_app / "migrations/__init__.py").exists()


def test_rm_migrations_with_excludes(tmp_path: Path):
    apps_dir = tmp_path / "apps"
    payments_app = apps_dir / "payments"
    payments_app.mkdir(parents=True)
    create_fake_migrations_dir(payments_app)
    excludes_files = [
        payments_app / "migrations/0010_exclude.py",
        payments_app / "migrations/0011_exclude.py",
    ]
    for f in excludes_files:
        f.touch()

    result = runner.invoke(
        cli,
        [
            "rm-migrations",
            str(apps_dir),
            "-e",
            "0010_exclude.py",
            "-e",
            "0011_exclude.py",
        ],
    )

    assert "SUCCESS" in result.output

    assert (payments_app / "migrations/__init__.py").exists()
    assert not (payments_app / "migrations/0001_initial.py").exists()

    for f in excludes_files:
        assert f.exists()
