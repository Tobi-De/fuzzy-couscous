This page describe how to use the all available commands.

## Intro

!!! Note
    `fuzzy-couscous` is the name of the cli installed when you install this package but since it's a bit annoying to
    type it every time, there is the short version `cuzzy` that you can use instead.
    The short version is the one that is used throughout the documentation for the examples.

Since this template uses [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject), you can
easily clone the project on your computer and generate a django project by using the command `django-admin` and specifying the
`fuzzy-couscous/templates/project_name` folder as the template. The final command is a bit long, that's why I made this
[cli](https://en.wikipedia.org/wiki/Command-line_interface) to simplify the process. The cli command is installed together with the package.

??? Tip "Install the package"

    ```shell
    pip install fuzzy-couscous --upgrade
    ```

## `cuzzy`

**Usage**:

```console
$ cuzzy [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show the help message and exit.

**Commands**:

* `make`: Initialize a new django project.
* `remove-poetry`:  Run this command to remove poetry as a dependency from your project.
* `work`: Run multiple commands in parallel.
* `write-env`: Update or create a .env file from a .env.template file.

## `cuzzy make`

Initialize a new django project. This template makes a lot of assumptions, if you want to make some adjustments to the template
you can [fork the github repository](https://github.com/Tobi-De/fuzzy-couscous/fork) of this project and make your changes in the `templates` folder,
you can then use the `--repo` option to specify your Github repository.

??? Info "Custom repository"
    Actually you don't need to fork my repository, you can use this command on any github repository hosting a django project template
    as long as the template is defined in a `templates` folder in the root of the repository. Basically, the github repository
    structure would look something like this:

    ```shell
    .
    ├── templates
    │   └── project_name
    ```

**Usage**:

```console
$ cuzzy make [OPTIONS] PROJECT_NAME
```

!!! Info
    The **authors** key of the `[tool.poetry]` section in the `pyproject.toml` is set using your git global user configuration.
    If you haven't set it yet, [see this page](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup#_your_identity).

**Arguments**:

* `PROJECT_NAME`: [required]

**Options**:

* `-r, --repo TEXT`: The github repository to pull the template from. The format to use is `username/repo` [default: Tobi-De/fuzzy-couscous]
* `-b, --branch [main|tailwind|bootstrap]`: The github branch to use. [default: main]
* `-s, --skip-install`: Skip dependencies installation. [default: False]
* `--help`: Show the help message and exit.

## `cuzzy remove-poetry`

Run this command to remove poetry as a dependency from your project, it updates your pyproject.toml
file to use [hatch](https://hatch.pypa.io/latest/) as the build system and can optionally create a virtual environment using [virtualenv](https://github.com/pypa/virtualenv).
Hatch is a modern and extensible Python project manager, it can handle environment creation, package publishing, versioning, etc,
everything you need to manage a python project, but here I chose to use it only as a build backend.
If you add the `--create-virtualenv` option, [pip-tools](https://github.com/jazzband/pip-tools) will be installed in the created environment,
you can use it to manage your dependencies.
If you are familiar with hatch, you can easily complete the hatch configurations from the generated `pyproject.toml` file
and use it instead of virtualenv to manage your project.

!!! Info
    The virtualenv is created using your global python interpreter.

!!! Warning
    Be sure to commit your changes before running this command, that way you can undo the changes if something goes
    wrong or if you simply change your mind

**Usage**:

```console
$ cuzzy remove-poetry [OPTIONS]
```

**Options**:

* `-c, --create-virtualenv`: Create an environment using virtualenv. [default: False]
* `--help`: Show the help message and exit.

## `cuzzy work`

Run multiple commands in parallel. When working with tailwind, I usually have to run the django `runserver` command and
the tailwind `compile` command, so I made this to run both in one command. This command use the python [subprocess](https://docs.python.org/3/library/subprocess.html) module to
run the commands in the same shell. If you don't provide the commands via the `--command` option it will try to read them
from your `pyproject.toml` file.

!!! Example
    somewhere in your `pyproject.toml` file
    ```toml
    [tool.cuzzy]
    work = ["python manage.py runserver", "python manage.py run_worker"]
    ```

!!! Note
    By the way if you have a better option to do this instead of using the python subprocess module, please [open an issue](https://github.com/Tobi-De/fuzzy-couscous/issues/new)

**Usage**:

```console
$ cuzzy work [OPTIONS]
```

**Options**:

* `-c, --command TEXT`: The command to run. [default: poe r, poe t]
* `--help`: Show the help message and exit.

!!! Example
    ```shell
    cuzzy work -c "python manage.py runserver" -c "python manage.py run_worker"
    ```

## `cuzzy write-env`

Running this will create a new `.env` by filling the file with the keys and values from the following options:

1. a `env.template` file, used if it exists
2. a `DEFAULT_VALUES` dictionary, internal to the `fuzzy-couscous` package, contains some default for common keys, `DJANGO_DEBUG`, `DJANGO_SECRET_KEY`, etc.
3. a `.env` file, used if it exists

The order defines the priority of the values that are used, which means that the values contained in your original `.env` file are preserved if the file exists.

**Usage**:

```console
$ cuzzy write-env [OPTIONS]
```

**Options**:

* `-f, --fill-missing`: Prompt to fill missing values. [default: False]
* `-o, --output-file FILE`: The output file path. [default: .env]
* `-p, --postgres-pass`: Prompt for the postgres password to use to build the `DATABASE_URL`.
* `--help`: Show the help message and exit.

## `cuzzy rm-migrations`

!!! Note
    This command was previously part of the generated project as a django management command, but I decided to move it to the
    `fuzzy-couscous` package since I'm probably the only one using it and I don't want to pollute the generated project with
    unnecessary code.

Remove all migrations for the specified applications directory, intended only for development.

!!! Warning
    This command will delete all your migrations files, be sure to commit your changes before running this command.

**Usage**:

```console
$ cuzzy rm-migrations [OPTIONS] APPS_DIR
```

**Arguments**:

* `APPS_DIR`: The path to your django apps directory. [required]

**Options**:

* `-e, --exclude TEXT`: A file to exclude from the deletion. This option can be repeated.

## `cuzzy htmx`

Download the htmx javascript library or one of its extension if specified. You won't have to download htmx or its extensions
often but at least if you need it, I think this is an easy way to get the file available locally.

**Usage**:

```console
$ cuzzy htmx [OPTIONS] VERSION
```

**Arguments**:

* `VERSION`: The version of htmx to download. [default: latest]

**Options**:

* `-e, --extension TEXT`: The name of the extension to download.
* `-f, --output-file TEXT`: The filename for the htmx download. [default: htmx.min.js]
* `-d, --output-dir DIRECTORY`: The directory to write the downloaded file to, default to the current working directory.
* `-w, --web-types`: Download the web-types file.
* `--help`: Show the help message and exit.
