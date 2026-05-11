"""PyVista reader-registry integration for IGES files."""

import os

try:
    # On pyvista >= 0.48, raising ``LocalFileRequiredError`` from a
    # reader entry point makes ``pv.read("http://.../foo.igs")``
    # download the file first and retry against the local copy.
    from pyvista import LocalFileRequiredError as _LocalFileRequiredError
    from pyvista import has_scheme as _has_scheme
except ImportError:  # pragma: no cover - older pyvista or no pyvista installed
    _LocalFileRequiredError = None
    _has_scheme = None

from pyiges.iges import Iges


def read_as_mesh(filename, merge=True):
    """Read an IGES file and return it as a PyVista mesh.

    Wraps :class:`pyiges.Iges` and converts all supported entities to
    a PyVista object via :meth:`pyiges.Iges.to_vtk`. Suitable for use
    as a PyVista reader-registry entry point.

    Parameters
    ----------
    filename : str | os.PathLike
        Path to the IGES file.
    merge : bool, default: True
        If ``True``, return a single :class:`pyvista.PolyData`
        containing all converted entities. If ``False``, return a
        :class:`pyvista.MultiBlock`.

    Returns
    -------
    pyvista.PolyData or pyvista.MultiBlock
        The converted geometry.

    Raises
    ------
    pyvista.LocalFileRequiredError
        If a remote URI is passed and ``pyvista >= 0.48`` is installed.
        The PyVista reader registry uses this to download the file and
        retry against the local copy.
    """
    fname = os.fspath(filename)
    if _has_scheme is not None and _has_scheme(fname):
        raise _LocalFileRequiredError
    return Iges(fname).to_vtk(merge=merge)
