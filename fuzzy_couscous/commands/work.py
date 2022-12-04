import subprocess

import typer
from rich import print as rich_print


def work(
    commands: list[str] = typer.Option(
        ["poe r", "poe t"],
        "-c",
        "--command",
        help="The command to run.",
    )
):
    """run multiple commands in parallel."""

    commands_display = " ".join([f"<< {c} >>" for c in commands])
    rich_print(f"[blue]INFO: work started for [yellow]{commands_display}")
    processes = []
    for cmd in commands:
        process = subprocess.Popen(cmd, shell=True)
        processes.append(process)

    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        pass
