## `cuzzy rm-migrations`

!!! Note
This command was previously part of the generated project as a django management command, but I decided to move it to
the
`falco` package since I'm probably the only one using it and I don't want to pollute the generated project with
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

