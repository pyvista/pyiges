
try:
    import pyvista
    import geomdl
    from pyvista._vtk import vtkAppendPolyData
    _IS_FULL_MODULE = True
except ModuleNotFoundError as exc:
    pyvista = None
    geomdl = None
    vtkAppendPolyData = None
    _IS_FULL_MODULE = False
    _PROBLEM_MSG = 'Module \'{}\' not found, to support this feature '\
        'please install pyiges[full]'.format(exc.name)

def assert_full_module_variant(inner_func):
    def safe_func(*a, **kw):
        if not _IS_FULL_MODULE:
            raise Exception(_PROBLEM_MSG)
        return inner_func(*a, **kw)
    return safe_func
