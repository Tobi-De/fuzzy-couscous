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

If you are using one of these you might want an automatic reload feature when files changes, you can use the `hupper` python
package for that purpose. If your project was generated with fuzzy-couscous then it is already declared as a dev dependencies.