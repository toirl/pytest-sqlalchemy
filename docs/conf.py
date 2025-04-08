from importlib import metadata

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('http://docs.python.org', None),
}

project = 'pytest-sqlalchemy'
author = 'Torsten Irländer'
release = metadata.version(project)
copyright = f'2015 onwards {author}'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_member_order = 'bysource'

html_theme = 'furo'

nitpicky = True
nitpick_ignore: list[tuple[str, str]] = []
