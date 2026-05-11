"""Optional-dependency probes for the ``[full]`` install variant."""

try:
    import geomdl
    import pyvista
    from vtkmodules.vtkFiltersCore import vtkAppendPolyData

    _IS_FULL_MODULE = True
except (ModuleNotFoundError, ImportError) as exc:
    pyvista = None
    geomdl = None
    vtkAppendPolyData = None
    _IS_FULL_MODULE = False
    _PROBLEM_MSG = (
        "Import from '{}' failed, to support this feature please install pyiges[full]".format(
            exc.name
        )
    )


def assert_full_module_variant(inner_func):
    """Wrap a function to require the optional ``[full]`` install variant.

    Raises an exception at call time if any of ``pyvista``, ``geomdl``,
    or VTK could not be imported, instructing the user to install
    ``pyiges[full]``.
    """

    def safe_func(*a, **kw):
        if not _IS_FULL_MODULE:
            raise Exception(_PROBLEM_MSG)
        return inner_func(*a, **kw)

    return safe_func
