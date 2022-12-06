import subprocess


def new_virtualenv():
    commands = [
        "python -m pip install virtualenv",
        "python -m virtualenv --prompt . venv",
        "venv/bin/python -m pip install pip-tools hatch",
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
