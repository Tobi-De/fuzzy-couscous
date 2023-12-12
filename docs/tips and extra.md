This section gathers tips, **copy and paste** configurations and package recommendations that I use quite often in my projects to solve specific problems.

Stuff too short to deserve a full guide or I don't know where to put them

## Understanding django Settings

If there is a setting in `settings.py` or elsewhere that you don't understand, go to the [official django settings reference page](https://docs.djangoproject.com/en/dev/ref/settings/)
and press <kbd>Ctrl</kbd> + <kbd>F</kbd> to search for it. I used the [django-production](https://github.com/lincolnloop/django-production) package to configure the production settings which I then customized.
I have removed the package as a dependency, but I advise you to go and check for yourself what is available.



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


## Lifecycle not signals


## Avoid huge apps for large projects


## Extra that I haven't tried myself yet

- [django-linear-migrations](https://github.com/adamchainz/django-linear-migrations): Read [introduction post](https://adamj.eu/tech/2020/12/10/introducing-django-linear-migrations/)
- [django-read-only](https://github.com/adamchainz/django-read-only): Disable Django database writes.

