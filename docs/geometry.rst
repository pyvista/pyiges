Geometry Entities
-----------------
The ``pyiges.Iges`` class stores each individual IGES entity
seperately and each entity of an ``pyiges.Iges`` object can be
accessed either via indexing or by querying for a specific type of entity

.. code:: python

    >>> import pyiges
    >>> from pyiges import examples
    >>> iges = pyiges.read(examples.impeller)
    >>> type(iges[0])
    pyiges.entity.Entity

    >>> lines = iges.lines()
    >>> print(lines[0])
    --- Line ---
    ----- Entity -----
    110
    1213
    0
    ...
    0
    From point 0.0, 0.0, -997.963013157 
    To point 0.0, 0.0, 2.036986843

Many of the entities are not yet fully supported, and those entities
are represented as a generic ``pyiges.geometry.Entity`` object.
However, many entities are supported, including:

- Vertex List (Type 502 Form 1)
- Edge List
- Loop (for specifying a bounded face for BREP geometries
- Face
- Circular arc
- Rational B-Spline Surface
- Rational B-Spline Curve
- Conic Arc (Type 104)
- Line
- Point


Entity Definitions
~~~~~~~~~~~~~~~~~~
.. autoclass:: pyiges.entity.Entity
    :members:

.. autoclass:: pyiges.geometry.Point
    :members:

.. autoclass:: pyiges.geometry.Line
    :members:

.. autoclass:: pyiges.geometry.ConicArc
    :members:

.. autoclass:: pyiges.geometry.RationalBSplineCurve
    :members:

.. autoclass:: pyiges.geometry.RationalBSplineSurface
    :members:

.. autoclass:: pyiges.geometry.CircularArc
    :members:

.. autoclass:: pyiges.geometry.Face
    :members:

.. autoclass:: pyiges.geometry.EdgeList
    :members:

.. autoclass:: pyiges.geometry.VertexList
    :members:
