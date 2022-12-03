import subprocess


def work(args):
    # todo: make this configurable via pyproject.toml
    processes = []
    commands = args.command or ["poe r", "poe t"]
    for cmd in commands:
        process = subprocess.Popen(cmd, shell=True)
        processes.append(process)

    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        pass
