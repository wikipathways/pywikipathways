project = 'pywikipathways'
copyright = '2021, Kozo Nishida'
author = 'Kozo Nishida'
import pywikipathways
version = pywikipathways.__version__
release = version

extensions = ['nbsphinx'
]

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'

html_static_path = ['_static']
html_logo = '_static/images/Wplogo_with_text_500.png'
