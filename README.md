# fuzzy-couscous

[![pypi](https://badge.fury.io/py/fuzzy-couscous.svg)](https://pypi.org/project/fuzzy-couscous/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/fuzzy-couscous/blob/master/LICENSE)
[![Code style: djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://www.djlint.com)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

My highly opinionated django project template based on [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject). This project is heavily inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) but is meant to be a lighter version.

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
- Dependency management using [poetry](https://github.com/python-poetry/poetry)

## Templates

I use github branches to create variations of the base template.

- [main](https://github.com/Tobi-De/fuzzy-couscous): The base template
- [tailwind](https://github.com/Tobi-De/fuzzy-couscous/tree/tailwind): The base template + [tailwindcss](https://github.com/timonweb/pytailwindcss)  via [pytailwindcss](https://github.com/timonweb/pytailwindcss)
- [bootstrap](https://github.com/Tobi-De/fuzzy-couscous/tree/bootstrap): The base template + [bootstrap5](https://getbootstrap.com/) via [django-bootstrap5](https://github.com/zostera/django-bootstrap5)

## Usage

Since this template uses [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject), you can
easily clone the project on your computer and generate a django project by using the command `django-admin` and specifying the `fuzzy-couscous/project_name` folder as the template.
The final command is a bit long so I made a simple [cli](https://en.wikipedia.org/wiki/Command-line_interface) to simplify the process, install it with the command below:

```shell
pip install fuzzy-couscous==1.1.0
```

now initialize a new django project with the command below:

```shell
fuzzy-couscous make my_new_project
```

> **NOTE**: You probably want to update the **authors** key in the `pyproject.toml` file in the `[tool.poetry]` section.

This command may take two optional arguments:

`--repo (-r)`: This template makes a lot of assumptions, if you like it but want to make some slight adjustments, make your own couscous by [forking this repo](https://github.com/Tobi-De/fuzzy-couscous/fork). 
You can then use this option to specify your github repository with the format `username/repo`.

Example:

```python
fuzzy-couscous make my_new_site --repo "Tobi-De/fuzzy-couscous"
```

`--branch (-b)`: Specify the branch from which you want to create the template (e.g. **tailwind**), the default value being **main**.

Example:

```python
fuzzy-couscous make my_new_site -b tailwind
```

If you've read this far and still think this template doesn't work for you, feel free to [create your own template](https://www.valentinog.com/blog/django-project/)
and copy and paste what you want from other similar projects like I did.

Some examples of templates you can use as inspiration:

- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [wemake-django-template](https://github.com/wemake-services/wemake-django-template)
- [django-startproject-templates](https://github.com/adamchainz/django-startproject-templates)

### Additional commands

Some additional commands I added to automate some boring stuff. These commands should be run at the root of
your projects, most will work even in projects that have not been generated with this template.

Usage
```shell
fuzzy-couscous command
```

`write-env`: Running this will create a new `.env` by filling the file with the keys and values from the following options:

1. a `env.template` file, used if it exists
2. a `DEFAULT_VALUES` dictionary, internal to the `fuzzy-couscous` package, contains some default for common keys, `DJANGO_DEBUG`, `DJANGO_SECRET_KEY`, etc.
3. a `.env` file, used if it exists

> **Note**: The order defines the priority of the values that are used, which means that the values contained in your original `.env` file are preserved if the file exists.

This command defines two additional optional options:

- `--fill-missing (-f)`: Prompt for missing values before the final `.env` file is generated
- `--output-file (-o)`: The output filename, default to `.env`

`work`: run multiple command in parallel. When working with tailwind, I usually have to run the django `runserver` command and 
the tailwind `compile` command, so I made this to run both in one command. This command use the python [subprocess](https://docs.python.org/3/library/subprocess.html) module to 
run the commands in the same shell. By default it will try to run the two commands below:

- `poe r`: run the django development server
- `poe t`: Compile tailwind in watch mode, available if you create your project using the `tailwind` branch

To specify your own commands, use the `-c` option, example:

```shell
fuzzy-coucsous work -c "python manage.py runserver" -c "python -m http.server 9000"
```

## Tips

This section gathers tips, **copy and paste** configurations and package recommendations that I use quite often in my projects to solve specific problems.

### Settings

If there is a setting in `settings.py` or elsewhere that you don't understand, go to the [official django settings reference page](https://docs.djangoproject.com/en/dev/ref/settings/)
and press <kbd>Ctrl</kbd> + <kbd>F</kbd> to search for it. I used the [django-production](https://github.com/lincolnloop/django-production) package to configure the production settings which I then customized.
I have removed the package as a dependency but I advise you to go and check for yourself what is available.

### Dynamic web pages

[HTMX](https://htmx.org/) for simple interactive elements, [django-unicorn](https://github.com/adamghill/django-unicorn) if I need something more integrated with django.
It's not a binary choice, you can use both, the main advantage for me is the simplicity compared to a frontend javascript framework.

> **NOTE**: If you use [htmx boost](https://htmx.org/docs/#boosting) + [debug toolbar](https://github.com/jazzband/django-debug-toolbar) (already included in the template), you will need [this](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#htmx).

### Task queues and schedulers

Task queues are used to offload tasks to a dedicated worker process when the processing of those tasks does not fit into a traditional request-response cycle.
Basically, if you need to do something that might take too long to process and whose result does not need to be shown immediately to the user, you use a queue manager.
Schedulers are used to periodically run tasks.
There are many options available in the [django third-party ecosystem](https://djangopackages.org/grids/g/workers-queues-tasks/), some focus solely on providing a task queue, 
others are just schedulers and many of them provide both in one package. You can also search for purely python solutions and 
integrate them into your django project yourself.

I prefer options that do not require additional infrastructure (redis, rabbitmq, etc.) for simple tasks.
For more complex tasks, I tend to choose a solution that supports redis as a task broker.

**Doesn't require setup of external tools, redis, rabbitmq, etc..**

- [django-chard](https://github.com/drpancake/chard): Task queue 
- [django-pgpubsub](https://github.com/Opus10/django-pgpubsub): Task queue 
- [procrastinate](https://github.com/procrastinate-org/procrastinate): Task queue + scheduler
- [django-q2](https://github.com/GDay/django-q2): Task queue + scheduler
- [rocketry](https://github.com/Miksus/rocketry): Scheduler

**Require the setup of external tools, redis, rabbitmq, etc.**

- [django-dramatiq](https://github.com/Bogdanp/django_dramatiq): Task queue 
- [django-rq](https://github.com/rq/django-rq): Task queue + scheduler via [django-rq-scheduler](https://github.com/dsoftwareinc/django-rq-scheduler)
- [wakaq](https://github.com/wakatime/wakaq): Task queue + scheduler

> **NOTE**: The order matters, that's the order in which I would choose one of these packages.

### Media storage

Media files in django usually refer to files uploaded by users, profile pictures, product images, etc.
I usually manage my media files using [django-storages](https://github.com/jschneier/django-storages).
Here is how I set it up.

```python
# core/storages.py
from storages.backends.s3boto3 import S3Boto3Storage

class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False

    
# settings.py - production settings
AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
DEFAULT_FILE_STORAGE = "project_name.core.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/"
```

### Database backup

Whenever possible, take advantage of a fully managed database solution, they usually offer automatic backup of your databases.
In my opinion, this is the best option if you don't want to deal with the hassle of managing your own database.

- [Amazon RDS](https://aws.amazon.com/rds/)
- [Linode Managed Databases](https://www.linode.com/products/databases/)
- [DigitalOcean Managed Databases](https://www.digitalocean.com/products/managed-databases)
- [Heroku postgres](https://www.heroku.com/postgres)

For specific postgresql options, see their [hosting support page](https://www.postgresql.org/support/professional_hosting/).

However, if for some reason you want / need to manage your database yourself and just want an automatic backup solution
then [django-dbbackup](https://github.com/jazzband/django-dbbackup) is what you need. You can use one of the scheduling 
packages discussed above to periodically run the backup command.

### Health check your django project

**Health check** is about making sure that your django application and related services are always available / running. 
My go-to package for this is [django-health-check](https://github.com/revsys/django-health-check).
After installing and configuring **django-health-check**, you need to associate it with an uptime monitoring service, this
is the service that will periodically call your **health-check** endpoint to make sure everything is fine.
Here is a list of available options.

- [upptime](https://github.com/upptime/upptime)
- [uptime-kuma](https://github.com/louislam/uptime-kuma)
- [uptimerobot](https://uptimerobot.com/)
- [glitchtip](https://glitchtip.com/)

Read more on the health check pattern [here](https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring). 

### Extra that I haven't tried myself yet

- [django-linear-migrations](https://github.com/adamchainz/django-linear-migrations): Read [introduction post](https://adamj.eu/tech/2020/12/10/introducing-django-linear-migrations/)
- [django-read-only](https://github.com/adamchainz/django-read-only): Disable Django database writes.

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

This template was configured to simplify deployment on [caprover](https://caprover.com/), since that is what I use 99% of the time.

> CapRover is an extremely easy to use app/database deployment & web server manager for your NodeJS, Python, PHP, ASP.NET, Ruby, MySQL, MongoDB, Postgres, WordPress (and etc...) applications!
> **Official site**

CapRover is a self-hosted [PaaS](https://en.wikipedia.org/wiki/Platform_as_a_service) solution, think [heroku](https://www.heroku.com/) but on your own servers. 
Nowadays, I tend to prefer PaaS solutions over manual deployment and configuration, as they are easy to use with little configuration to deploy most apps.
Software is usually quite a pain to deploy and even though I've gotten better at it over time, I'll always choose a managed solution over manual deployment. 
Some other options than **CapRover** are:

- [Dokku](https://dokku.com/) (self hosted)
- [Fly](https://fly.io/) (hosted)
- [Render](https://render.com/) (hosted)
- [Coolify](https://github.com/coollabsio/coolify) (self hosted)
- [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform) (hosted)
- [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) (hosted)
- [Btn](https://btn.dev/) (hosted and not ready yet)

I find that self-hosted solutions are generally cheaper than managed/hosted solutions, but I don't have much experience with managed solutions, 
so I could be wrong, do your own research and if you can afford it, try them out to see what works best for you.

After installing CaProver with the [getting started guide](https://caprover.com/docs/get-started.html), there is not much left to do, create a new application and in the section `deployment`.
configure your application using the third method `Method 3: Deploy from Github/Bitbucket/Gitlab`.

> **Note**: If you use github, instead of entering your password directly into the `password` field, you can use a [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token),
> which is a more secure option.

> **Tip**: Checkout [caprover automatic deploy](https://caprover.com/docs/deployment-methods.html#automatic-deploy-using-github-bitbucket-and-etc) to automate the deployment of your applications.
