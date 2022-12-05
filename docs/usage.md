This page describe how to use the all available commands.

## Generate a new project

!!! Note
    `fuzzy-couscous` is the name of the cli installed when you install this package but since it's a bit annoying to
    type it every time, there is the short version `cuzzy` that you can use instead.
    The short version is the one that is used throughout the documentation for the examples.

Since this template uses [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject), you can
easily clone the project on your computer and generate a django project by using the command `django-admin` and specifying the `fuzzy-couscous/templates/project_name` folder as the template.
The final command is a bit long so I made a simple [cli](https://en.wikipedia.org/wiki/Command-line_interface) to simplify the process.
The cli command is installed together with the package.

??? Tip "Install the package"

    ```shell
    pip install fuzzy-couscous --upgrade
    ```

Initialize a new django project with the command below:

```shell
cuzzy make my_new_project
```

!!! Info
    Update the **authors** key in the `pyproject.toml` file in the `[tool.poetry]` section.

This command may take two optional arguments:

`--repo (-r)`: This template makes a lot of assumptions, if you like it but want to make some slight adjustments, make your own couscous by [forking this repo](https://github.com/Tobi-De/fuzzy-couscous/fork).
You can then use this option to specify your github repository with the format `username/repo`.

Example:

```python
cuzzy make my_new_site --repo "Tobi-De/fuzzy-couscous"
```

`--branch (-b)`: Specify the branch from which you want to create the template (e.g. **tailwind**), the default value being **main**.

Example:

```python
cuzzy make my_new_site -b tailwind
```

If you've read this far and still think this template doesn't work for you, feel free to [create your own template](https://www.valentinog.com/blog/django-project/)
and copy and paste what you want from other similar projects like I did.

Some examples of templates you can use as inspiration:

- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [wemake-django-template](https://github.com/wemake-services/wemake-django-template)
- [django-startproject-templates](https://github.com/adamchainz/django-startproject-templates)

## Additional commands

Some additional commands I added to automate some boring stuff. These commands should be run at the root of
your projects, most will work even in projects that have not been generated with this template.

Usage

```shell
fuzzy-couscous command
```

### write-env

!!! Example
    ```shell
    cuzzy write-env
    cuzzy write-env -f
    cuzzy write-env -o .test.env
    ```

Running this will create a new `.env` by filling the file with the keys and values from the following options:

1. a `env.template` file, used if it exists
2. a `DEFAULT_VALUES` dictionary, internal to the `fuzzy-couscous` package, contains some default for common keys, `DJANGO_DEBUG`, `DJANGO_SECRET_KEY`, etc.
3. a `.env` file, used if it exists

The order defines the priority of the values that are used, which means that the values contained in your original `.env` file are preserved if the file exists.

This command defines two additional optional options:

- `--fill-missing (-f)`: Prompt for missing values before the final `.env` file is generated
- `--output-file (-o)`: The output filename, default to `.env`

### work

run multiple command in parallel. When working with tailwind, I usually have to run the django `runserver` command and
the tailwind `compile` command, so I made this to run both in one command. This command use the python [subprocess](https://docs.python.org/3/library/subprocess.html) module to
run the commands in the same shell. By default it will try to run the two commands below:

- `poe r`: run the django development server
- `poe t`: Compile tailwind in watch mode, available if you create your project using the `tailwind` branch

To specify your own commands, use the `-c` option.

!!! Example

    ```shell
    cuzzy work -c "python manage.py runserver" -c "python -m http.server 9000"
    ```

### remove-poetry

!!! Example
    ```shell
    cuzzy remove-poetry
    ```
