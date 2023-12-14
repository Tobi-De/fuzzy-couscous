The CLI
=========

The falco CLI is available you install the package. It is home to some command that I hope you will find useuful through the Lifecycle of your project,
from starting the project through to deployment.

.. hint:: Install the cli
   :class: dropdown

   .. code:: console

      $ pip install falco --upgrade


falco
-----

The entrypoint for the CLI is the ``falco`` command. It is used to run the commands that are available to you.

**Usage**:

.. code:: console

   $ falco [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--completion generate``: Install completion for the current shell.
-  ``--help``: Show the help message and exit.

**Commands**:

-  ``start-project``: Initialize a new django project.
-  ``crud``: Generate CRUD (Create, Read, Update, Delete) views for a model.
-  ``work``: Run multiple commands in parallel.
-  ``sync-dotenv``: Syncronize the .env file with the .env.template file.
-  ``htmx``: Download the latest version of htmx.
-  ``htmx-ext``: Download an htmx extension.
-  ``rm-migrations``: Remove all migrations from all apps.



.. toctree::
   :hidden:

   start_project
   crud
   htmx
   work
   rm_migrations
   sync_dotenv