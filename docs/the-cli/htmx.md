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
