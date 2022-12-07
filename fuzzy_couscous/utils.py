from copy import deepcopy
from pathlib import Path

import tomli
import tomli_w

RICH_SUCCESS_MARKER = "[green]SUCCESS:"
RICH_ERROR_MARKER = "[red]ERROR:"
RICH_INFO_MARKER = "[blue]INFO:"
RICH_COMMAND_MARKER = "[yellow]"
RICH_COMMAND_MARKER_END = "[/yellow]"


def clean_project_name(val: str) -> str:
    return val.strip().replace(" ", "_").replace("-", "_")


def get_current_dir_as_project_name():
    current_dir = Path().resolve(strict=True).stem
    return clean_project_name(current_dir)


def read_toml(file: Path) -> dict:
    return tomli.loads(file.read_text())


def write_toml(file: Path, data: dict) -> None:
    remove_empty_top_level_table(data)
    sorted_data = sort_config(data)
    file.write_text(tomli_w.dumps(sorted_data))


def sort_config(config: dict) -> dict:
    return dict(sorted(config.items()))


def remove_empty_top_level_table(config: dict) -> None:
    # removing values from a dictionary while iterating through it is not a good idea, hence this copy
    config_copy = deepcopy(config)
    for key, value in config_copy.items():
        if not value:
            config.pop(key)
