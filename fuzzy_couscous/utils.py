from pathlib import Path

import tomli
import tomli_w


def clean_project_name(val: str) -> str:
    return val.strip().replace(" ", "_").replace("-", "_")


def get_current_dir_as_project_name():
    current_dir = Path().resolve(strict=True).stem
    return clean_project_name(current_dir)


def read_toml(file: Path) -> dict:
    return tomli.loads(file.read_text())


def write_toml(file: Path, data: dict) -> None:
    file.write_text(tomli_w.dumps(data))
