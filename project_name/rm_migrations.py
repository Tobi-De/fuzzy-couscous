import sys
from pathlib import Path


def main():
    apps_dir = Path() / "{{project_name}}"
    excludes = ["__init__.py"]
    apps = set()
    for folder in apps_dir.iterdir():
        migration_dir = folder / "migrations"
        if not migration_dir.exists():
            continue
        for file in migration_dir.iterdir():
            if file.suffix == ".py" and file.name not in excludes:
                file.unlink()
                apps.add(str(folder))
                sys.stdout.write(f"{str(file)} deleted")
    res = "\n".join(apps)
    sys.stdout.write(f"\nRemoved migration files for apps: \n{res}")


if __name__ == "__main__":
    main()
