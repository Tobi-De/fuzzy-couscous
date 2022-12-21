# fuzzy-couscous

[![pypi](https://badge.fury.io/py/fuzzy-couscous.svg)](https://pypi.org/project/fuzzy-couscous/)
[![Docs: Mkdocs](https://img.shields.io/badge/mkdocs-docs-blue.svg)](https://tobi-de.github.io/fuzzy-couscous)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/fuzzy-couscous/blob/master/LICENSE)
[![Code style: djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://www.djlint.com)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

✨📚✨ [Read the full documentation](https://tobi-de.github.io/fuzzy-couscous)

My highly opinionated django project template based on [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject).
This project is heavily inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) but is meant to be a lighter version.
This template also comes with a cli tool with [additional commands](https://tobi-de.github.io/fuzzy-couscous/usage/#cuzzy) to hopefully improve your django development experience.

![showcase gif](https://raw.githubusercontent.com/Tobi-De/fuzzy-couscous/main/docs/assets/cuzzy_demo.gif)

## Features

- Django 4+
- Python 3.10+
- Frontend: [htmx](https://htmx.org/) with [editor support](https://oluwatobi.dev/blog/posts/htmx-support-in-pycharm/) using [web-types](https://github.com/JetBrains/web-types#web-types)
- Template fragment with [django-render-block](https://github.com/clokep/django-render-block)
- Secure production settings, https only.
- Settings using [django-environ](https://github.com/joke2k/django-environ)
- Login / signup via [django-allauth](https://github.com/pennersr/django-allauth)
- Custom user model based on [django-improved-user](https://github.com/jambonsw/django-improved-user)
- Login using email instead of username
- Automatically reload your browser in development via [django-browser-reload](https://github.com/adamchainz/django-browser-reload)
- Better development experience with [django-fastdev](https://github.com/boxed/django-fastdev)
- [Amazon SES](https://aws.amazon.com/ses/?nc1=h_ls) for production email via [Anymail](https://github.com/anymail/django-anymail)
- [Docker](https://www.docker.com/) ready for production
- Optional production cache settings using the `CACHE_URL` or `REDIS_URL` environment variables.
- `captain-definition` for deploying to [caprover](https://caprover.com/)
- [Sentry](https://sentry.io/welcome/) for performance/error monitoring
- Serve static files with [Whitenoise](https://whitenoise.evans.io/en/latest/)
- Default integration with [pre-commit](https://github.com/pre-commit/pre-commit) for identifying simple issues before submission to code review
- Integrated task runner with [poethepoet](https://github.com/nat-n/poethepoet)
- Dependency management using [poetry](https://github.com/python-poetry/poetry) (can be replaced by [virtualenv](https://github.com/pypa/virtualenv) using the [`remove-poetry` command](https://tobi-de.github.io/fuzzy-couscous/usage/#cuzzy-remove-poetry))

## Templates

I use github branches to create variations of the base template.

- [main](https://github.com/Tobi-De/fuzzy-couscous): The base template
- [tailwind](https://github.com/Tobi-De/fuzzy-couscous/tree/tailwind): The base template + [tailwindcss](https://github.com/timonweb/pytailwindcss)  via [pytailwindcss](https://github.com/timonweb/pytailwindcss)
- [bootstrap](https://github.com/Tobi-De/fuzzy-couscous/tree/bootstrap): The base template + [bootstrap5](https://getbootstrap.com/) via [django-bootstrap5](https://github.com/zostera/django-bootstrap5)

## Quickstart

Install the latest version of the package

```shell
pip install fuzzy-couscous --upgrade
```

Initialize a new project

```shell
cuzzy make project_name
```

## Development

Poetry is required (not really, you can set up the environment however you want and install the requirements
manually) to set up a virtualenv, install it then run the following:

```sh
pre-commit install --install-hooks
```

Tests can then be run quickly in that environment:

```sh
pytest
```

## Feedback

If you have any feedback, please reach out to me at tobidegnon@proton.me or [open a discussion](https://github.com/Tobi-De/fuzzy-couscous/discussions/new).

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
