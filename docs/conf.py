# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Falco"
copyright = "2023, Tobi DEGNON"
author = "Tobi DEGNON"
release = "2023"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx_design"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "shibuya"
html_static_path = ["_static"]

# -- Shibuya theme options ---------------------------------------------------
html_context = {
    "source_type": "github",
    "source_user": "tobi-de",
    "source_repo": "falco",
}
html_theme_options = {
    "mastodon_url": "https://fosstodon.org/@tobide",
    "github_url": "https://github.com/tobi-de/falco",
    "twitter_url": "https://twitter.com/tobidegnon",
}
