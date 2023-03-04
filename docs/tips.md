This section gathers tips, **copy and paste** configurations and package recommendations that I use quite often in my projects to solve specific problems.

## Settings

If there is a setting in `settings.py` or elsewhere that you don't understand, go to the [official django settings reference page](https://docs.djangoproject.com/en/dev/ref/settings/)
and press <kbd>Ctrl</kbd> + <kbd>F</kbd> to search for it. I used the [django-production](https://github.com/lincolnloop/django-production) package to configure the production settings which I then customized.
I have removed the package as a dependency, but I advise you to go and check for yourself what is available.

## Dynamic web pages

[HTMX](https://htmx.org/) for simple interactive elements, [django-unicorn](https://github.com/adamghill/django-unicorn) if I need something more integrated with django.
It's not a binary choice, you can use both, the main advantage for me is the simplicity compared to a frontend javascript framework.

!!! Note
    If you use [htmx boost](https://htmx.org/docs/#boosting) + [debug toolbar](https://github.com/jazzband/django-debug-toolbar) (already included in the template), you will need [this](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#htmx).

## Task queues and schedulers

Task queues are used to offload tasks to a dedicated worker process when the processing of those tasks does not fit into a traditional request-response cycle.
Basically, if you need to do something that might take too long to process and whose result does not need to be shown immediately to the user, you use a queue manager.
Schedulers are used to periodically run tasks.
There are many options available in the [django third-party ecosystem](https://djangopackages.org/grids/g/workers-queues-tasks/), some focus solely on providing a task queue,
others are just schedulers and many of them provide both in one package. You can also search for purely python solutions and
integrate them into your django project yourself.

I prefer options that do not require additional infrastructure (redis, rabbitmq, etc.) for simple tasks.
For more complex tasks, I tend to choose a solution that supports redis as a task broker.

**Doesn't require setup of external tools, redis, rabbitmq, etc..**

- [django-q2](https://github.com/GDay/django-q2) : Task queue + scheduler
- [django-chard](https://github.com/drpancake/chard) : Task queue
- [django-pgpubsub](https://github.com/Opus10/django-pgpubsub) : Task queue
- [procrastinate](https://github.com/procrastinate-org/procrastinate) : Task queue + scheduler
- [rocketry](https://github.com/Miksus/rocketry) : Scheduler

**Require the setup of external tools, redis, rabbitmq, etc.**

- [django-dramatiq](https://github.com/Bogdanp/django_dramatiq) : Task queue
- [django-rq](https://github.com/rq/django-rq) : Task queue + scheduler via [django-rq-scheduler](https://github.com/dsoftwareinc/django-rq-scheduler)
- [wakaq](https://github.com/wakatime/wakaq) : Task queue + scheduler

!!! Note
    The order matters, that's the order in which I would choose one of these packages.

## Media storage

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

## Database backup

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

## Health check your django project

**Health check** is about making sure that your django application and related services are always available / running.
My go-to package for this is [django-health-check](https://github.com/revsys/django-health-check).
After installing and configuring **django-health-check**, you need to associate it with an uptime monitoring service, this
is the service that will periodically call your **health-check** endpoint to make sure everything is fine.
Here is a list of available options.

- [upptime](https://github.com/upptime/upptime)
- [uptime-kuma](https://github.com/louislam/uptime-kuma)
- [uptimerobot](https://uptimerobot.com/)
- [better-uptime](https://betterstack.com/better-uptime)
- [glitchtip](https://glitchtip.com/)

Read more on the health check pattern [here](https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring).

## Extra that I haven't tried myself yet

- [django-linear-migrations](https://github.com/adamchainz/django-linear-migrations): Read [introduction post](https://adamj.eu/tech/2020/12/10/introducing-django-linear-migrations/)
- [django-read-only](https://github.com/adamchainz/django-read-only): Disable Django database writes.
