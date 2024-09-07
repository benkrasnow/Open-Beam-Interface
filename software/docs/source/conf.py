# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Open Beam Interface'
copyright = '2024, Isabel Burgos, Adam McCombs'
author = 'Isabel Burgos, Adam McCombs'
release = '0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser", 
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.linkcode",
    "enum_tools.autoenum"
    ]

autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True
}
autodoc_preserve_defaults = True
autodoc_inherit_docstrings = False

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_favicon = '_static/favicon.png'
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#FF4F00",
        "color-brand-content": "#2EA22A",
        "color-brand-visited": "#1F7B1E"
    },
    "dark_css_variables": {
        "color-brand-primary": "#FF4F00",
        "color-brand-content": "#2EA22A",
        "color-brand-visited": "#1F7B1E"
    },
    "light_logo": "image_scan_drawing_black.svg",
    "dark_logo": "image_scan_drawing_white.svg"
}

def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    return "https://github.com/nanographs/Open-Beam-Interface/blob/update-main/software/%s.py" % filename
    