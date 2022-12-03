from pathlib import Path

SUCCESS = "\x1b[1;32m [SUCCESS]: "
INFO = "\x1b[1;33m [INFO]: "
TERMINATOR = "\x1b[0m"


def clean_project_name(val: str) -> str:
    return val.strip().replace(" ", "_").replace("-", "_")


def get_current_dir_as_project_name():
    current_dir = Path().resolve(strict=True).stem
    return clean_project_name(current_dir)


def print_success(msg: str) -> None:
    print(SUCCESS + msg + TERMINATOR)


def print_info(msg: str) -> None:
    print(INFO + msg + TERMINATOR)
