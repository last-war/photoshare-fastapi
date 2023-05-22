import sys
import os

sys.path.append(os.path.abspath('..'))
project = 'PhotoShare Rest API'
copyright = '2023, command 6 Web9 GoIT'
author = 'command 6 Web9 GoIT'
release = '0.1.0'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']
