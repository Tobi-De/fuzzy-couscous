# Falco

<img align="right" width="170" height="170" src="https://res.cloudinary.com/dgugjkmqg/image/upload/v1702502731/Logo_2_zfg43u.svg">

[![CD](https://github.com/Tobi-De/falco/actions/workflows/deploy.yml/badge.svg)](https://github.com/Tobi-De/falco/actions/workflows/deploy.yml)
[![CI](https://github.com/Tobi-De/falco/actions/workflows/test.yml/badge.svg)](https://github.com/Tobi-De/falco/actions/workflows/test.yml)
[![pypi](https://badge.fury.io/py/falco.svg)](https://pypi.org/project/falco/)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Tobi-De/falco/blob/main/LICENSE)


✨📚✨ [Read the full documentation](https://tobi-de.github.io/falco)

A cli tool based on [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject) to bootstrap
your django projects with a modern stack. The project template is heavily inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) but is meant to be a simpler version.
The cli also comes with [additional commands](https://tobi-de.github.io/falco/usage/#cuzzy) to hopefully improve your django development experience.

![showcase gif](https://raw.githubusercontent.com/Tobi-De/falco/main/docs/assets/cuzzy_demo.gif)


## How to use this project


Fist of all take the habit to [skimm through the documentation](a blog post here), so take a few minutes, to skimm through this one when you are done with this readme.

The cli
The guides


very opinionated stuff

choice are already made, give options but already pick something to start with.

## Features

- Django 4+
- Python 3.10+
- Frontend: [htmx](https://htmx.org/) with [editor support](https://oluwatobi.dev/blog/posts/htmx-support-in-pycharm/) using [web-types](https://github.com/JetBrains/web-types#web-types)
- Template fragment with [django-template-partials](https://github.com/carltongibson/django-template-partials)
- Secure production settings, https only.
- Settings using [django-environ](https://github.com/joke2k/django-environ)
- Login / signup via [django-allauth](https://github.com/pennersr/django-allauth)
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
- Dependency management using [poetry](https://github.com/python-poetry/poetry) (can be replaced by [virtualenv](https://github.com/pypa/virtualenv) using the [`remove-poetry` command](https://tobi-de.github.io/falco/usage/#cuzzy-remove-poetry))

## Templates

I use github branches to create variations of the base template.

- [main](https://github.com/Tobi-De/falco): The base template
- [tailwind](https://github.com/Tobi-De/falco/tree/tailwind): The base template + [tailwindcss](https://github.com/timonweb/pytailwindcss)  via [pytailwindcss](https://github.com/timonweb/pytailwindcss)
- [bootstrap](https://github.com/Tobi-De/falco/tree/bootstrap): The base template + [bootstrap5](https://getbootstrap.com/) via [django-bootstrap5](https://github.com/zostera/django-bootstrap5)

> **Note**: If some of my decisions about the project template don't make sense to you, read [this section](https://tobi-de.github.io/falco/project/) of the documentation.

## Quickstart

Install the latest version of the package

```shell
pip install falco --upgrade
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

## Acknowledgements

Falco is inspired by (and borrows elements from) some excellent starter templates:

- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [django-hatch-startproject](https://github.com/oliverandrich/django-hatch-startproject)
- [django-unicorn](https://github.com/adamghill/django-unicorn) - Inspiration for the logo

## Feedback

If you have any feedback, please reach out to me at tobidegnon@proton.me or [open a discussion](https://github.com/Tobi-De/falco/discussions/new).

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
