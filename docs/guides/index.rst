Guides
======

This is a collection of guides on somehwat common topics related to any web development project but tailor to django. It is 
like the `django topic guides <https://docs.djangoproject.com/en/5.0/topics/>`_ but instead of focusing on components of the framework
like ``forms``, ``models``, ``views`` etc. it focuses on more general topics like ``task queues``, ``deployment``, ``realtime`` etc.
These are very opniniated since based on my own experience. For each guide when it make sens I'll add a `Tl;DR` and specific first 
what is my current (because this might change with new experiences) approach of tackling the issue at hand, I'll also includes alternatives
so that you can make your own mind. The set of guides here will be keep restricted, this is not like a blog where I may post any and everything 
(for that checkout my `blog <https://oluwatobi.dev/blog>`_). This is more like a collection of recipes for common problems.
For feedback on the content of any of this guides, open a `new github discussion <https://github.com/Tobi-De/falco/discussions>`_, if you think I'm wrong on
something of thing my be formulate better or if you have a better approach, I'll be happy to hear it.

.. note::
   ``note`` I want to use github discussion mostly for the guides part and issues (broken code) for the cli part


A lot of the content here is geared toward beginner to intermidate but more for the latter, in the sense should have at least complete a django project (
like the `official django tutorial <https://docs.djangoproject.com/en/5.0/intro/tutorial01/>`_), I think you need to at least that to feel comfortable reading these guides,
but I'll try to make them as digestable as I can and link to enought external ressources if it is needed for deeper understanding.


External Ressources
-------------------

These are my personal top picks for places to look for django, htmx and web dev in general.

.. grid:: 2

    .. grid-item-card:: The official Django documentation
        :link: https://docs.djangoproject.com/en/dev/

        Always have a tab open to the official Django documentation. It is the best source for django.

    .. grid-item-card:: The HTMX documentation
        :link: https://htmx.org/

        The htmx documentation have everything you need to understand htmx but they also have great essays that are worth reading to broader your understanding of web development.

    .. grid-item-card:: HTML First
        :link: https://html-first.com/

        HTML First is a set of principles that aims to make building web software easier, faster, more inclusive, and more maintainable.

    .. grid-item-card:: Adam Johnson blog
        :link: https://adamj.eu/tech/

        A core django developer, he has the most unique content on django I Know of, on every aspect of the framework.

    .. grid-item-card:: BugBytes
        :link: https://www.youtube.com/bugbytes

        Great youtube channel with a lot of django and htmx content.

    .. grid-item-card:: GrugBrain dev
        :link: https://grugbrain.dev

        A layman's guide to thinking like the self-aware smol brained.

.. toctree::
    :hidden:

    interactive_user_experience_with_htmx
    task_queues_and_schedulers
    working_around_fat_models
    optimizing_database_access
    realtime
    permissions_and_authorization
    writing_documentation
    writing_tests
    deployment
    multitenancy
    database_tips