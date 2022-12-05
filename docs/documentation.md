This template does not include a documentation setup, but it is very important for most projects (at least it should be)
to have a documentation site, especially if you are not working alone. Here are the options I would suggest for setting
up a documentation, recently I tend to favor the first one.

- [Mkdocs](https://www.mkdocs.org/) with the [Material theme](https://squidfunk.github.io/mkdocs-material/getting-started/)
- [Sphinx](https://www.sphinx-doc.org/en/master/) with the [Furo theme](https://github.com/pradyunsg/furo)

There is a chance that in the future I will include the docs directly in the template but for now here is a quick guide to
configure mkdocs with the material theme:

### Installation and configurations

Copy the configuration below into your `pyproject.toml` file under the `[tool.poetry.dependencies]` section.

```toml
[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.4.2"
mkdocs-material = "^8.5.10"
mkdocs-material-extensions = "^1.1.1"
mkdocs-include-markdown-plugin = "3.9.1"
```

Install the new dependencies.

```shell
poetry install --with docs
```

Create your new **mkdocs** site.

```shell
mkdocs new .
```

Update the `mkdocs.yml` file to specify the **material** theme, your configuration should look like this:

```yaml
site_name: My Docs # change this to the name of your project
theme:
  name: material
```

Run the documentation site locally

```shell
mkdocs serve
```

If you noticed, the dependencies added above via the section `[tool.poetry.group.docs.dependencies]` include more than just
mkdocs and the material theme, specifically :

- [mkdocs-material-extensions](https://github.com/facelessuser/mkdocs-material-extensions): Markdown extension resources for MkDocs for Material
- [mkdocs-include-markdown-plugin](https://github.com/mondeja/mkdocs-include-markdown-plugin):  Include other markdown files in your mkdocs site

For a complete example of how I configure them in projects, see this [configuration file](https://github.com/Tobi-De/dj-shop-cart/blob/master/mkdocs.yml).

### Deploy your documentation

**Mkdocs** can turn your documentation into a static site that you can host anywhere, [netlify](https://www.netlify.com/), [github pages](https://pages.github.com/), etc.
To build your site, run the command below and you will have a new `site` directory at the root of your project:

```shell
mkdocs build
```

This folder contains everything that is necessary to deploy your static site.

If you choose the **github pages** route, you can automate the process with [github actions](https://github.com/features/actions),
the official **mkdocs-material** documentation explains [how to do it](https://squidfunk.github.io/mkdocs-material/publishing-your-site/).
To use github actions, you will probably need a `requirements.txt` file, you can generate one with only what is needed
to build the docs with the command below.

```shell
poetry export -f requirements.txt --output docs/requirements.txt --without-hashes --only docs
```

Read the [mkdocs](https://www.mkdocs.org/) and [mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/) docs for more advanced configurations and details on what is possible.
