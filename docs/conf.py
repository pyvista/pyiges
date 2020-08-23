"""
Configuration file for the Sphinx documentation builder.
"""
import sphinx_rtd_theme

import pyiges


# -- Project information -----------------------------------------------------
project = 'pyiges'
copyright = '2020, Alex Kaszynski'
author = 'Alex Kaszynski'
release = version = pyiges.__version__

# # Manage errors
# pyvista.set_error_output_file('errors.txt')
# # Ensure that offscreen rendering is used for docs generation
# pyvista.OFF_SCREEN = True
# # Preferred plotting style for documentation
# # pyvista.set_plot_theme('document')
# pyvista.rcParams['window_size'] = np.array([1024, 768]) * 2
# # Save figures in specified directory
# pyvista.FIGURE_PATH = os.path.join(os.path.abspath('./images/'), 'auto-generated/')
# if not os.path.exists(pyvista.FIGURE_PATH):
#     os.makedirs(pyvista.FIGURE_PATH)

# pyvista.BUILDING_GALLERY = True

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.doctest',
              'sphinx.ext.autosummary',
              'notfound.extension',
              'sphinx_copybutton',
              # 'sphinx_gallery.gen_gallery',
              'sphinx.ext.extlinks',
              'sphinx.ext.coverage',
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
