Keep the .env and .env.template in sync
=======================================


``cuzzy write-env``
-------------------

Running this will create a new ``.env`` by filling the file with the keys and values from the following options:

1. a ``env.template`` file, used if it exists
2. a ``DEFAULT_VALUES`` dictionary, internal to the ``falco`` package, contains some default for common
   keys, ``DJANGO_DEBUG``, ``DJANGO_SECRET_KEY``, etc.
3. a ``.env`` file, used if it exists

The order defines the priority of the values that are used, which means that the values contained in your
original ``.env`` file are preserved if the file exists.

**Usage**:

.. code:: console

   $ cuzzy write-env [OPTIONS]

**Options**:

-  ``-f, --fill-missing``: Prompt to fill missing values. [default: False]
-  ``-o, --output-file FILE``: The output file path. [default: .env]
-  ``-p, --postgres-pass``: Prompt for the postgres password to use to build the ``DATABASE_URL``.
-  ``--help``: Show the help message and exit.
