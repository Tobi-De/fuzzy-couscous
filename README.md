# fuzzy-couscous

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/fuzzy-couscous/blob/master/LICENSE)
[![Code style: djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://www.djlint.com)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

My highly opinionated django project template based on [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject). This project is heavily inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) but is meant to be a lighter version.

## Features

- django 4+
- python 3.10+
- [tailwindcss](https://github.com/timonweb/pytailwindcss) set-up via [pytailwindcss](https://github.com/timonweb/pytailwindcss)
- [htmx](https://htmx.org/) included
- [django-render-block](https://github.com/clokep/django-render-block) for template fragment rendering with htmx
- [django-environ](https://github.com/joke2k/django-environ) based settings
- login / signup via [django-allauth](https://github.com/pennersr/django-allauth)
- custom user model based on [django-improved-user](https://github.com/jambonsw/django-improved-user)
- login via email instead of username
- dev html livereload via [django-browser-reload](https://github.com/adamchainz/django-browser-reload)
- production amazon ses set-up via [Anymail](https://github.com/anymail/django-anymail)
- Dockerfile included for easy deployment
- `captain-definition` for deploying to [caprover](https://caprover.com/)
- [pre-commit](https://github.com/pre-commit/pre-commit) to identify issues before every commit
- [poethepoet](https://github.com/nat-n/poethepoet) for shortcuts to common commands
- [poetry](https://github.com/python-poetry/poetry) for dependency management

## Templates

- [main](https://github.com/Tobi-De/fuzzy-couscous): The base template
- [tailwind](https://github.com/Tobi-De/fuzzy-couscous/tree/tailwind): The base template + [tailwindcss](https://github.com/timonweb/pytailwindcss)  via [pytailwindcss](https://github.com/timonweb/pytailwindcss)

## Installation

Since this template uses [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject), you can
easily clone the project on your computer and generate a django project by using the command `django-admin` and specifying the `fuzzy-couscous/project_name` folder as the template.
The final command is a bit long so I made a simple [cli](https://en.wikipedia.org/wiki/Command-line_interface) to simplify the process, install it with the command below:

```shell
pip install fuzzy-couscous
```

now initialize a new django project with the command below:

```shell
fuzzy-couscous my_new_project
```

This command may take two optional arguments:

`--repo (-r)`: This set-up makes a lot of assumptions, if you like it but want to make some slight adjustments, make your own couscous by [forking this repo](https://github.com/Tobi-De/fuzzy-couscous/fork). 
You can then use this option to specify your github repository with the format `username/repo`.

Example:

```python
fuzzy-couscous my_new_site --repo "Tobi-De/fuzzy-couscous"
```

`--branch (-b)`: Specify the branch from which you want to create the template (e.g. **tailwind**), the default value being **main**.

Example:

```python
fuzzy-couscous my_new_site -b tailwind
```

If you've read this far and still think this template won't work for you, feel free to [create your own template](https://www.valentinog.com/blog/django-project/) 
and copy and paste what you want like I did :).
Some examples of templates you can use as inspiration:

- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [wemake-django-template](https://github.com/wemake-services/wemake-django-template)
- [django-startproject-templates](https://github.com/adamchainz/django-startproject-templates)

## Tips

> This section is a WIP

If there is any setting that you don't understand got to this [page](https://docs.djangoproject.com/en/dev/ref/settings/) and
search for it using `CTRL + F`

If using htmx boost + debug toolbar, see [this](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#htmx)

Disable signup at will with allauth:

```python
# settings.py
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_ADAPTER = "izimanage.users.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "izimanage.users.adapters.SocialAccountAdapter"

# adapters.py
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
```


https://adamj.eu/tech/2020/12/10/introducing-django-linear-migrations/
https://github.com/adamchainz/django-read-only
https://github.com/revsys/django-health-check

## Documentation

TODO

## Deployment

TODO
