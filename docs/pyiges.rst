Pyiges Usage
------------

There are two ways the ``pyiges`` module can open iges files.  First,
use the ``read`` function:

.. autofunction:: pyiges.read


Alternatively, you can create an object directly from the ``Iges``
class:

.. code:: python

    >>> import pyiges
    >>> iges = pyiges.Iges('my_file.iges')
    pyiges.Iges object
    Description: 
    Number of Entities: 4615


.. autoclass:: pyiges.Iges
    :members:
