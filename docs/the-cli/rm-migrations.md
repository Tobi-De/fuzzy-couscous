## `cuzzy rm-migrations`

!!! Note
This command was previously part of the generated project as a django management command, but I decided to move it to
the
`fuzzy-couscous` package since I'm probably the only one using it and I don't want to pollute the generated project with
unnecessary code.

Remove all migrations for the specified applications directory, intended only for development.

!!! Warning
This command will delete all your migrations files, be sure to commit your changes before running this command.

**Usage**:

```console
$ cuzzy rm-migrations [OPTIONS] APPS_DIR
```

**Arguments**:

* `APPS_DIR`: The path to your django apps directory. [required]

**Options**:

* `-e, --exclude TEXT`: A file to exclude from the deletion. This option can be repeated.

## `cuzzy htmx`

Download the htmx javascript library or one of its extension if specified. You won't have to download htmx or its
extensions
often but at least if you need it, I think this is an easy way to get the file available locally.

**Usage**:

```console
$ cuzzy htmx [OPTIONS] VERSION
```

**Arguments**:

* `VERSION`: The version of htmx to download. [default: latest]

**Options**:

* `-e, --extension TEXT`: The name of the extension to download.
* `-f, --output-file TEXT`: The filename for the htmx download. [default: htmx.min.js]
* `-d, --output-dir DIRECTORY`: The directory to write the downloaded file to, default to the current working directory.
* `-w, --web-types`: Download the web-types file.
* `--help`: Show the help message and exit.
