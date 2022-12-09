from __future__ import annotations

import subprocess


def new_virtualenv():
    commands = [
        "python -m pip install --upgrade pip virtualenv",
        "python -m virtualenv --prompt . venv",
        "venv/bin/python -m pip install pip-tools hatch",
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)


def compile_requirements(groups: list[str]):
    extras = " --extra " + " --extra ".join(groups) if groups else ""
    base_command = "venv/bin/python -m piptools compile -o requirements.txt pyproject.toml --resolver=backtracking"
    subprocess.run(
        [base_command + extras],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def install_dependencies():
    subprocess.run(
        ["venv/bin/python -m piptools sync"],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
