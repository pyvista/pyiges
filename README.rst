pyIGES
======
Python IGES reader with basic functionality to read an IGES file and
convert some entities to a ``pyvista`` or ``vtk`` mesh.

This module can read in and perform basic parsing of all entities and
can perform additional parsing and geometry visualization of the
following entities:

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


Installation
------------
Install with pip using:

.. code::

   pip install pyiges

Otherwise, if you want the bleeding edge version, feel free to clone
this repo and install with:

.. code:: bash

   git clone https://github.com/pyvista/pyiges
   cd pyiges
   pip install .


Usage
-----
The ``pyiges`` module can read in many entities as raw text, but only
NURBS surfaces and bsplines can be converted to ``pyvista`` meshes.

.. code:: python

    import pyiges
    from pyiges import examples

    # load an example impeller
    iges = pyiges.read(examples.impeller)

    # print an invidiual entity (boring)
    print(iges[0])

    # convert all lines to a vtk mesh and plot it
    lines = iges.to_vtk(bsplines=True, surfaces=False, merge=True)
    lines.plot(color='w', line_width=2)

    # convert all surfaces to a vtk mesh and plot it
    mesh = iges.to_vtk(bsplines=False, surfaces=True, merge=True, delta=0.05)
    mesh.plot(color='w', smooth_shading=True)
    # control resolution of the mesh by changing "delta"

    # save this surface to file
    mesh.save('mesh.ply')  # as ply
    mesh.save('mesh.stl')  # as stl
    mesh.save('mesh.vtk')  # as vtk


Lines
~~~~~
.. image:: https://github.com/pyvista/pyiges/raw/master/docs/images/impeller_lines.png


Surfaces
~~~~~~~~
.. image:: https://github.com/pyvista/pyiges/raw/master/docs/images/impeller_surf.png



Acknowledgments
---------------
Substantial code was obtained from or inspired by https://github.com/cfinch/IGES-File-Reader

IGES reference definitions were obtained from `Eclipse IGES Wiki <https://wiki.eclipse.org/IGES_file_Specification#Rational_B-Spline_Curve_.28Type_126.29>`_,
