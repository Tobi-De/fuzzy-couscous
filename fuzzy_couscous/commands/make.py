import shutil
import subprocess
from pathlib import Path

from ..utils import clean_project_name, print_info, print_success


def make_project(args):
    project_name = clean_project_name(args.project_name)

    # run the django-admin command
    subprocess.run(
        [
            "django-admin",
            "startproject",
            project_name,
            "--template",
            f"https://github.com/{args.repo}/archive/{args.branch}.zip",
            "-e=py,html,toml,md,json,js,sh",
        ]
    )

    # since the root dir and the real project dir have the same name, rename the root to avoid conflict
    project_root_dir = Path() / project_name
    project_root_new_dir = Path() / f"_root_{project_root_dir}"
    project_root_dir.rename(str(project_root_new_dir))

    # move the real project dir to the current working directory
    project_dir = project_root_new_dir / project_name
    new_project_dir = Path() / project_name
    shutil.move(project_dir, new_project_dir)

    # delete the root dir
    shutil.rmtree(project_root_new_dir)

    print_success("Project initialized, keep up the good work!")
    print_info(
        "If you like the project consider dropping a star at https://github.com/Tobi-De/fuzzy-couscous"
    )
