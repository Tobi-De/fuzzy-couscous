# fuzzy-couscous

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/fuzzy-couscous/blob/master/LICENSE)
[![Code style: djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://www.djlint.com)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

My highly opinionated django project template based on [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject). This project is heavily inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) but is meant to be a lighter version.

## Features

- Django 4+
- Python 3.10+
- Frontend: [HTMX](https://htmx.org/) with [editor support](https://oluwatobi.dev/blog/posts/htmx-support-in-pycharm/) using [web-types](https://github.com/JetBrains/web-types#web-types)
- Frontend CSS: [tailwindcss](https://github.com/timonweb/pytailwindcss) via [pytailwindcss](https://github.com/timonweb/pytailwindcss)
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
- Dependency management using [poetry](https://github.com/python-poetry/poetry)

## Templates

I use github branches to create variations of the base template.

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

> **NOTE**: You probably want to update the **authors** key in the `pyproject.toml` file in the `[tool.poetry]` section.

This command may take two optional arguments:

`--repo (-r)`: This template makes a lot of assumptions, if you like it but want to make some slight adjustments, make your own couscous by [forking this repo](https://github.com/Tobi-De/fuzzy-couscous/fork). 
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

If you've read this far and still think this template doesn't work for you, feel free to [create your own template](https://www.valentinog.com/blog/django-project/)
and copy and paste what you want from other similar projects like I did.

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
ACCOUNT_ADAPTER = "project_name.users.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "project_name.users.adapters.SocialAccountAdapter"

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
https://github.com/lincolnloop/django-production

## Documentation

This template does not include a documentation setup, but it is very important for most projects (at least it should be) 
to have a documentation site, especially if you are not working alone. Here are the options I would suggest for setting 
up a documentation, recently I tend to favor the first one.

- [Mkdocs](https://www.mkdocs.org/) with the [Material theme](https://squidfunk.github.io/mkdocs-material/getting-started/)
- [Sphinx](https://www.sphinx-doc.org/en/master/) with the [Furo theme](https://github.com/pradyunsg/furo)

There is a chance that in the future I will include the docs directly in the template but for now here is a quick guide to 
configure mkdocs with the material theme:

### Installation and configurations

Copy the configuration below into your `pyproject.toml` file under the `[tool.poetry.dependencies]` section.

```toml
[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.4.2"
mkdocs-material = "^8.5.10"
mkdocs-material-extensions = "^1.1.1"
mkdocs-include-markdown-plugin = "^3.9.1"
```

Install the new dependencies.

```shell
poetry install --with docs
```

Create your new **mkdocs** site.

```shell
mkdocs new .
```

Update the `mkdocs.yml` file to specify the **material** theme, your configuration should look like this:

```yaml
site_name: My Docs # change this to the name of your project
theme:
  name: material
```

If you noticed, the dependencies added above via the section `[tool.poetry.group.docs.dependencies]` include more than just 
mkdocs and the material theme, specifically :

- [mkdocs-material-extensions](https://github.com/facelessuser/mkdocs-material-extensions): Markdown extension resources for MkDocs for Material
- [mkdocs-include-markdown-plugin](https://github.com/mondeja/mkdocs-include-markdown-plugin):  Include other markdown files in your mkdocs site 

For a complete example of how I configure them in projects, see this [configuration file](https://github.com/Tobi-De/dj-shop-cart/blob/master/mkdocs.yml).

### Deploy your documentation

**Mkdocs** can turn your documentation into a static site that you can host anywhere, [netlify](https://www.netlify.com/), [github pages](https://pages.github.com/), etc.
To build your site, run the command below and you will have a new `site` directory at the root of your project:

```shell
mkdocs build
```

This folder contains everything that is necessary to deploy your static site.

If you choose the **github pages** route, you can automate the process with [github actions](https://github.com/features/actions), 
the official **mkdocs-material** documentation explains [how to do it](https://squidfunk.github.io/mkdocs-material/publishing-your-site/).
To use github actions, you will probably need a `requirements.txt` file, you can generate one with only what is needed
to build the docs with the command below.

```shell
poetry export -f requirements.txt --output docs/requirements.txt --without-hashes --only docs
```

Read the [mkdocs](https://www.mkdocs.org/) and [mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/) docs for more advanced configurations and details on what is possible.

## Deployment

TODO
