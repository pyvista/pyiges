##############
 Contributing
##############

We absolutely welcome contributions and we hope that this guide will
facilitate an understanding of the PyIGES code repository. It is
important to note that this PyVista software package is maintained on a
volunteer basis and thus we need to foster a community that can support
user questions and develop new features to make this software a useful
tool for all users.

This page is dedicated to outline where you should start with your
question, concern, feature request, or desire to contribute.

******************
 Being Respectful
******************

Please demonstrate empathy and kindness toward other people, other
software, and the communities who have worked diligently to build
(un)related tools.

Please do not talk down in Pull Requests, Issues, or otherwise in a way
that portrays other people or their works in a negative light.

*******************************
 Cloning the Source Repository
*******************************

You can clone the source repository from
https://github.com/pyvista/pyiges and install the latest version by
running:

.. code:: bash

   git clone https://github.com/pyvista/pyiges.git
   cd pyiges
   python -m pip install -e .

****************
 Reporting Bugs
****************

If you stumble across any bugs, crashes, or concerning quirks while
using code distributed here, please report it on the `issues page
<https://github.com/pyvista/pyiges/issues>`_ with an appropriate label
so we can promptly address it. When reporting an issue, please be overly
descriptive so that we may reproduce it. Whenever possible, please
provide tracebacks, screenshots, and sample files to help us address the
issue.

******************
 Feature Requests
******************

We encourage users to submit ideas for improvements to PyIGES code base.
Please create an issue on the `issues page
<https://github.com/pyvista/pyiges/issues>`_ with a *Feature Request*
label to suggest an improvement. Please use a descriptive title and
provide ample background information to help the community implement
that functionality. For example, if you would like a reader for a
specific file format, please provide a link to documentation of that
file format and possibly provide some sample files with screenshots to
work with. We will use the issue thread as a place to discuss and
provide feedback.

***********************
 Contributing New Code
***********************

If you have an idea for how to improve PyIGES, please first create an
issue as a feature request which we can use as a discussion thread to
work through how to implement the contribution.

Once you are ready to start coding and develop for PyIGES, please see
the `Development Practices <#development-practices>`_ section for more
details.

***********
 Licensing
***********

All contributed code will be licensed under The MIT License found in the
repository. If you did not write the code yourself, it is your
responsibility to ensure that the existing license is compatible and
included in the contributed files or you can obtain permission from the
original author to relicense the code.

----

***********************
 Development Practices
***********************

This section provides a guide to how we conduct development in the
PyIGES repository. Please follow the practices outlined here when
contributing directly to this repository.

Contributing to PyIGES through GitHub
=====================================

To submit new code to PyIGES, first fork the `pyiges GitHub Repository
<https://github.com/pyvista/pyiges>`_ and then clone the forked
repository to your computer. Then, create a new branch based on the
`Branch Naming Conventions Section <#branch-naming-conventions>`_ in
your local repository.

Next, add your new feature and commit it locally. Be sure to commit
frequently as it is often helpful to revert to past commits, especially
if your change is complex. Also, be sure to test often. See the `Testing
Section <#testing>`_ below for automating testing.

When you are ready to submit your code, create a pull request by
following the steps in the `Creating a New Pull Request section
<#creating-a-new-pull-request>`_.

Coding Style
------------

We adhere to `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_
wherever possible, except that line widths are permitted to go beyond 79
characters to a max of 99 characters for code. This should tend to be
the exception rather than the norm. A uniform code style is enforced by
`black <https://github.com/psf/black>`_ to prevent energy wasted on
style disagreements.

As for docstrings, follow the guidelines specified in `PEP 8 Maximum
Line Length
<https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_ of
limiting docstrings to 72 characters per line. This follows the
directive:

   Some teams strongly prefer a longer line length. For code maintained
   exclusively or primarily by a team that can reach agreement on this
   issue, it is okay to increase the line length limit up to 99
   characters, provided that comments and docstrings are still wrapped
   at 72 characters.

Outside of PEP 8, when coding please consider `PEP 20 - The Zen of
Python <https://www.python.org/dev/peps/pep-0020/>`_. When in doubt:

.. code:: python

    import this

PyIGES uses pre-commit_ to enforce PEP8 and other styles automatically.
Please see the `Style Checking section <#style-checking>`_ for further
details.

Documentation Style
-------------------

PyIGES follows the `Google Developer Documentation Style
<https://developers.google.com/style>`_ with the following exceptions:

-  Allow first person pronouns. These pronouns (for example, "We") refer
   to "PyVista Developers", which can be anyone who contributes to
   PyVista.

-  Future tense is permitted.

Docstrings
----------

PyIGES uses Python docstrings to create reference documentation for our
Python APIs. Docstrings are read by developers, interactive Python
users, and readers of our online documentation. This section describes
how to write these docstrings for PyIGES.

PyIGES follows the ``numpydoc`` style for its docstrings. Please follow
the `numpydoc Style Guide`_ in all ways except for the following:

-  Be sure to describe all ``Parameters`` and ``Returns`` for all public
   methods.

-  We strongly encourage you to add an example section.

-  With optional parameters, use ``default: <value>`` instead of
   ``optional`` when the parameter has a default value instead of
   ``None``.

Sample docstring follows:

.. code:: python

    def slice_x(self, x=None, generate_triangles=False):
        """Create an orthogonal slice through the dataset in the X direction.

        Parameters
        ----------
        x : float, optional
            The X location of the YZ slice. By default this will be the X center
            of the dataset.

        generate_triangles : bool, default: False
            If this is enabled, the output will be all triangles. Otherwise the
            output will consist of the intersection polygons.

        Returns
        -------
        pyvista.PolyData
            Sliced dataset.

        Examples
        --------
        Slice the random hills dataset with one orthogonal plane.

        >>> from pyvista import examples
        >>> hills = examples.load_random_hills()
        >>> slices = hills.slice_x(5, generate_triangles=False)
        >>> slices.plot(line_width=5)

        See :ref:`slice_example` for more examples using this filter.

        """

        pass  # implementation goes here

Note the following:

-  The parameter definition of ``generate_triangles`` uses ``default:
   False``, and does not include the default in the docstring's
   "description" section.

-  There is a newline between each parameter. This is different than
   ``numpydoc``'s documentation where there are no empty lines between
   parameter docstrings.

-  This docstring also contains a returns section and an examples
   section.

-  The returns section does not include the parameter name if the
   function has a single return value. Multiple return values (not
   shown) should have descriptive parameter names for each returned
   value, in the same format as the input parameters.

-  The examples section references the "full example" in the gallery if
   it exists.

Branch Naming Conventions
-------------------------

To streamline development, we have the following requirements for naming
branches. These requirements help the core developers know what kind of
changes any given branch is introducing before looking at the code.

-  ``fix/``, ``patch/`` and ``bug/``: any bug fixes, patches, or
   experimental changes that are minor
-  ``feat/``: any changes that introduce a new feature or significant
   addition
-  ``junk/``: for any experimental changes that can be deleted if gone
   stale
-  ``maint/``: for general maintenance of the repository or CI routines
-  ``doc/``: for any changes only pertaining to documentation
-  ``no-ci/``: for low impact activity that should NOT trigger the CI
   routines
-  ``testing/``: improvements or changes to testing
-  ``release/``: releases (see below)
-  ``breaking-change/``: Changes that break backward compatibility

Testing
-------

After making changes, please test changes locally before creating a pull
request. The following tests will be executed after any commit or pull
request, so we ask that you perform the following sequence locally to
track down any new issues from your changes.

To run our comprehensive suite of unit tests, install all the
dependencies listed in ``requirements_test.txt`` and
``requirements_docs.txt``:

.. code:: bash

   pip install -r requirements_test.txt
   pip install -r requirements_docs.txt

Then, if you have everything installed, you can run the various test
suites.

Unit Testing
============

Run the primary test suite and generate coverage report:

.. code:: bash

   python -m pytest -v --cov pyiges

Style Checking
==============

PyIGES follows PEP8 standard as outlined in the `Coding Style section
<#coding-style>`_ and implements style checking using pre-commit_.

To ensure your code meets minimum code styling standards, run:

.. code:: bash

   pip install pre-commit
   pre-commit run --all-files

You can also install this as a pre-commit hook by running:

.. code:: bash

   pre-commit install

This way, it's not possible for you to push code that fails the style
checks. For example, each commit automatically checks that you meet the
style requirements:

.. code:: bash

   $ pre-commit install
   $ git commit -m "added my cool feature"
   black....................................................................Passed
   isort....................................................................Passed
   flake8...................................................................Passed
   codespell................................................................Passed

The actual installation of the environment happens before the first
commit following ``pre-commit install``. This will take a bit longer,
but subsequent commits will only trigger the actual style checks.

Even if you are not in a situation where you are not performing or able
to perform the above tasks, you can comment `pre-commit.ci autofix` on a
pull request to manually trigger auto-fixing.

.. _numpydoc style guide: https://numpydoc.readthedocs.io/en/latest/format.html

.. _pre-commit: https://pre-commit.com/
