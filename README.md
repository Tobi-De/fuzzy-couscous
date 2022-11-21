# fuzzy-couscous

**TODO**
- complete the readme
- a branch for boostrap5

My highly opinionated django project template.
Based on [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject).
For something with more options I suggest [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django).

```shell
pip install fuzzy-couscous
fuzzy-couscous my_new_project
```

This setup makes a lot of assumptions, and if you like say 80% of it, but want to change some details then I suggest you
make your own couscous by [forking this repo](https://github.com/Tobi-De/fuzzy-couscous/fork).
You can then use the fuzzy-couscous command `repo` option to specify your github repository with the `username/repo` format.

Example:

```python
fuzzy-couscous my_new_site --repo "Tobi-De/fuzzy-couscous"
```

If you are searching completely different, [make you own template](https://www.valentinog.com/blog/django-project/).


## Tips

If there is any setting that you don't understand got to this [page](https://docs.djangoproject.com/en/dev/ref/settings/) and
search for it using `CTRL + F`

```python
from django.conf import settings
from django.core.management.base import BaseCommand
from {{ project_name }}.users.model import User


class Command(BaseCommand):
    help = "Command to create admin"

    def handle(self, *args, **options):
        if not User.objects.filter(email=settings.FIRST_SUPERUSER).exists():
            User.objects.create_superuser(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASS,
                is_active=True,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Admin {settings.FIRST_SUPERUSER} was created")
            )
        else:
            self.stdout.write(
                self.style.NOTICE(f"Admin {settings.FIRST_SUPERUSER} already exists")
            )
```

If using htmx boost + debug toolbar , see [this](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#htmx)


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

sentry settings

````python
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
integrations = [sentry_logging, DjangoIntegration(), RedisIntegration()]
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=integrations,
    environment=env("SENTRY_ENVIRONMENT", default="production"),
    traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
    auto_session_tracking=False,
    release="1.0.0",
)
````

## Django packages


https://adamj.eu/tech/2020/12/10/introducing-django-linear-migrations/
https://adamchainz.gumroad.com/l/byddx
https://github.com/adamchainz/django-read-only
https://github.com/revsys/django-health-check

## Documentation

## Deployment
