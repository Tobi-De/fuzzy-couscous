The CLI
=========

Since this template
uses `django’s startproject –template <https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject>`__, you
can
easily clone the project on your computer and generate a django project by using the command ``django-admin`` and
specifying the
``falco/templates/project_name`` folder as the template. The final command is a bit long, that’s why I made this
`cli <https://en.wikipedia.org/wiki/Command-line_interface>`__ to simplify the process. The cli command is installed
together with the package.

??? Tip “Install the package”

::

   ```shell
   pip install falco --upgrade
   ```

``cuzzy``
---------

**Usage**:

.. code:: console

   $ cuzzy [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--install-completion``: Install completion for the current shell.
-  ``--show-completion``: Show completion for the current shell, to copy it or customize the installation.
-  ``--help``: Show the help message and exit.

**Commands**:

-  ``make``: Initialize a new django project.
-  ``remove-poetry``: Run this command to remove poetry as a dependency from your project.
-  ``work``: Run multiple commands in parallel.
-  ``write-env``: Update or create a .env file from a .env.template file.



.. toctree::
   :hidden:

   start_project
   crud
   htmx
   work
   rm_migrations
   sync_dotenv