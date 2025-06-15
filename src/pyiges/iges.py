from tqdm import tqdm

from pyiges import geometry
from pyiges.check_imports import assert_full_module_variant, pyvista, vtkAppendPolyData
from pyiges.entity import Entity


class Iges:
    """pyiges.Iges object

    Parameters
    ----------
    filename : str
        Filename of an IGES file.

    Examples
    --------
    >>> import pyiges
    >>> from pyiges import examples
    >>> iges = pyiges.read(examples.impeller)
        pyiges.Iges object
        Description:
        Number of Entities: 4615
    """

    def __init__(self, filename):
        self._read(filename)
        self._desc = ""

    def entities(self):
        """Return a list of all entities

        Examples
        --------
        >>> iges.entities
        [<pyiges.geometry.Point at 0x7f7056069c10>,
         <pyiges.geometry.Point at 0x7f7056069790>,
         <pyiges.geometry.Point at 0x7f7056069a50>,
         <pyiges.geometry.Point at 0x7f7056069b10>,
         <pyiges.entity.Entity at 0x7f7056069910>]
        """

    @assert_full_module_variant
    def to_vtk(
        self,
        lines=True,
        bsplines=True,
        surfaces=True,
        points=True,
        delta=0.025,
        merge=True,
        progress=tqdm,
    ):
        """Converts entities to a vtk object

        Parameters
        ----------
        lines : bool, optional
            Convert lines.

        surfaces : bool, optional
            Convert B-Spline surfaces.

        points : bool, optional
            Convert points.

        delta : float, optional
            Resolution when converting spline entities.  Higher
            resolution creates a better plot at the cost of computing
            time.

        merge : bool, optional
            Merge all converted entities into one output.

        progress: function, optional
            Report conversion progress by use of this function. Example::

                def silent_progress(iterable, *args, **kwargs):
                    return iterable

            Passing progress=silent_progress will show no progress, the
            default is to use tqdm for progress reporting.

        Returns
        -------
        surf : pyvista.PolyData or pyvista.MultiBlock
            Geometry represented as ``pyvista.PolyData`` if merged or
            a ``MultiBlock`` if unmerged.

        Examples
        --------
        Convert all entities except for surfaces to vtk

        >>> lines = iges.to_vtk(surfaces=False)
        >>> print(lines)
        PolyData (0x7f700c79f3d0)
          N Cells:	2440
          N Points:	96218
          X Bounds:	-4.299e+01, 6.912e+14
          Y Bounds:	-4.255e+01, 6.290e+14
          Z Bounds:	-9.980e+02, 6.702e+14
          N Arrays:	0
        """
        items = pyvista.MultiBlock()
        for entity in progress(self, desc="Converting entities to vtk"):
            if isinstance(entity, geometry.RationalBSplineCurve) and bsplines:
                items.append(entity.to_vtk(delta))
            elif isinstance(entity, geometry.RationalBSplineSurface) and surfaces:
                items.append(entity.to_vtk(delta))
            elif isinstance(entity, geometry.Line) and lines:
                items.append(entity.to_vtk())
            elif isinstance(entity, geometry.Point) and points:
                items.append(entity.to_vtk())

        # merge to a single mesh
        if merge:
            afilter = vtkAppendPolyData()
            for item in items:
                afilter.AddInputData(item)
            afilter.Update()

            return pyvista.wrap(afilter.GetOutput())

        return items

    def points(self, as_vtk=False, merge=False, **kwargs):
        """Return all points"""
        return self._return_type(geometry.Point, as_vtk, merge, **kwargs)

    def edge_lists(self, as_vtk=False, merge=False, **kwargs):
        """All Edge Lists"""
        return self._return_type(geometry.EdgeList, as_vtk, merge, **kwargs)

    def vertex_lists(self, as_vtk=False, merge=False, **kwargs):
        """All Point Lists"""
        return self._return_type(geometry.VertexList, as_vtk, merge, **kwargs)

    def lines(self, as_vtk=False, merge=False, **kwargs):
        """All lines"""
        return self._return_type(geometry.Line, as_vtk, merge, **kwargs)

    def bsplines(self, as_vtk=False, merge=False, **kwargs):
        """All bsplines"""
        return self._return_type(geometry.RationalBSplineCurve, as_vtk, merge, **kwargs)

    def bspline_surfaces(self, as_vtk=False, merge=False, **kwargs):
        """All bsplines

        Examples
        --------
        Convert and plot all bspline surfaces.  This takes a while
        since the geometry tessellation is done in pure python by
        ``geomdl``.  Reduce the conversion time by setting delta to a
        larger than default value (0.025)

        >>> mesh = iges.bspline_surfaces(as_vtk=True, merge=True)
        >>> mesh.plot()

        Alternatively, just extract the B-REP surfaces and extract
        their parameters

        >>> bsurf = iges.bspline_surfaces()
        >>> bsurf[0]
        Rational B-Spline Surface
            Upper index of first sum:        3
            Upper index of second sum:       3
            Degree of first basis functions: 3
            Degree of second basis functions: 3
            Open in the first direction
            Open in the second direction
            Polynomial
            Periodic in the first direction
            Periodic in the second direction
            Knot 1: [0. 0. 0. 0. 1. 1. 1. 1.]
            Knot 2: [0. 0. 0. 0. 1. 1. 1. 1.]
            u0: 1.000000
            u1: 0.000000
            v0: 1.000000
            v1: 128.000000
            Control Points: 16
        """
        return self._return_type(
            geometry.RationalBSplineSurface, as_vtk, merge, **kwargs
        )

    def circular_arcs(self, to_vtk=False, merge=False, **kwargs):
        """All circular_arcs"""
        return self._return_type(geometry.CircularArc, to_vtk, merge, **kwargs)

    def conic_arcs(self, as_vtk=False, merge=False, **kwargs):
        return self._return_type(geometry.ConicArc, as_vtk, merge, **kwargs)

    def faces(self, as_vtk=False, merge=False, **kwargs):
        return self._return_type(geometry.Face, as_vtk, merge, **kwargs)

    def loops(self, as_vtk=False, merge=False, **kwargs):
        return self._return_type(geometry.Loop, as_vtk, merge, **kwargs)

    def _return_type(self, iges_type, to_vtk=False, merge=False, **kwargs):
        """Return an iges type"""
        items = []
        for entity in self:
            if isinstance(entity, iges_type):
                if to_vtk:
                    items.append(entity.to_vtk(**kwargs))
                else:
                    items.append(entity)

        # merge to a single mesh
        if merge and to_vtk:
            afilter = vtkAppendPolyData()
            for item in items:
                afilter.AddInputData(item)
            afilter.Update()

            return pyvista.wrap(afilter.GetOutput())

        return items

    def __iter__(self):
        yield from self._entities

    def __len__(self):
        return len(self._entities)

    def __repr__(self):
        info = "pyiges.Iges object\n"
        info += "Description: %s\n" % self._desc
        info += "Number of Entities: %d" % len(self)
        return info

    def from_pointer(self, ptr):
        """Return an iges object according to an iges pointer"""
        return self[self._pointers[ptr]]

    @staticmethod
    def _parse_separators_from_first_global_line(line):
        if line[0] == ",":
            a = ","
            if line[1] == a:
                b = ";"
            elif line[1:3] == "1H":
                b = line[3]
            else:
                raise RuntimeError("Invalid Global section format")
        elif line[0:2] == "1H":
            a = line[2]
            if line[4:6] == "1H":
                b = line[6]
            elif line[3] == a:
                b = ";"
            else:
                raise RuntimeError("Invalid Global section format")
        else:
            raise RuntimeError("Invalid Global section format")
        return a, b

    def _read(self, filename):
        with open(filename) as f:
            param_string = ""
            entity_list = []
            entity_index = 0
            first_dict_line = True
            first_global_line = True
            first_param_line = True
            global_string = ""
            pointer_dict = {}
            entities_to_discard = []

            # for line in tqdm(f.readlines(), desc='Reading file'):
            for line_no, line in enumerate(f.readlines(), start=1):
                data = line[:80]
                id_code = line[72]

                if id_code == "S":  # Start
                    desc = line[:72].strip()

                elif id_code == "G":  # Global
                    global_string += data  # Consolidate all global lines
                    if first_global_line:
                        (
                            param_sep,
                            record_sep,
                        ) = self._parse_separators_from_first_global_line(data)
                        first_global_line = False

                elif id_code == "D":  # Directory entry
                    if first_dict_line:
                        entity_type_number = int(data[0:8].strip())
                        # Curve and surface entities.  See IGES spec v5.3, p. 38, Table 3
                        if entity_type_number == 100:  # Circular arc
                            e = geometry.CircularArc(self)
                        elif entity_type_number == 102:  # Composite curve
                            e = Entity(self)
                        elif entity_type_number == 104:  # Conic arc
                            e = geometry.ConicArc(self)
                        elif entity_type_number == 108:  # Plane
                            e = Entity(self)
                        elif entity_type_number == 110:  # Line
                            e = geometry.Line(self)
                        elif entity_type_number == 112:  # Parametric spline curve
                            e = Entity(self)
                        elif entity_type_number == 114:  # Parametric spline surface
                            e = Entity(self)
                        elif entity_type_number == 116:  # Point
                            e = geometry.Point(self)
                        elif entity_type_number == 118:  # Ruled surface
                            e = Entity(self)
                        elif entity_type_number == 120:  # Surface of revolution
                            e = Entity(self)
                        elif entity_type_number == 122:  # Tabulated cylinder
                            e = Entity(self)
                        elif entity_type_number == 124:  # Transformation matrix
                            e = geometry.Transformation(self)
                        elif entity_type_number == 126:  # Rational B-spline curve
                            e = geometry.RationalBSplineCurve(self)
                        elif entity_type_number == 128:  # Rational B-spline surface
                            e = geometry.RationalBSplineSurface(self)

                        # CSG Entities. See IGES spec v5.3, p. 42, Section 3.3
                        elif entity_type_number == 150:  # Block
                            e = Entity(self)

                        # B-Rep entities.  See IGES spec v5.3, p. 43, Section 3.4
                        elif entity_type_number == 186:
                            e = Entity(self)

                        # Annotation entities.  See IGES spec v5.3, p. 46, Section 3.5
                        elif entity_type_number == 202:
                            e = Entity(self)

                        # Structural entities.  See IGES spec v5.3, p. 50, Section 3.6
                        elif entity_type_number == 132:
                            e = Entity(self)
                        elif entity_type_number == 502:
                            e = geometry.VertexList(self)
                        elif entity_type_number == 504:
                            e = geometry.EdgeList(self)
                        elif entity_type_number == 508:
                            e = geometry.Loop(self)
                        elif entity_type_number == 510:
                            e = geometry.Face(self)
                        else:
                            e = Entity(self)

                        e.add_section(data[0:8], "entity_type_number")
                        e.add_section(data[8:16], "parameter_pointer")
                        e.add_section(data[16:24], "structure")
                        e.add_section(data[24:32], "line_font_pattern")
                        e.add_section(data[32:40], "level")
                        e.add_section(data[40:48], "view")
                        e.add_section(data[48:56], "transform")
                        e.add_section(data[56:65], "label_assoc")
                        e.add_section(data[65:72], "status_number")
                        e.sequence_number = int(data[73:].strip())

                        first_dict_line = False
                    else:
                        e.add_section(data[8:16], "line_weight_number")
                        e.add_section(data[16:24], "color_number")
                        e.add_section(data[24:32], "param_line_count")
                        e.add_section(data[32:40], "form_number")
                        e.add_section(data[56:64], "entity_label", type="string")
                        e.add_section(data[64:72], "entity_subs_num")

                        first_dict_line = True
                        entity_list.append(e)
                        pointer_dict.update({e.sequence_number: entity_index})
                        entity_index += 1

                elif id_code == "P":  # Parameter data
                    # Concatenate multiple lines into one string
                    if first_param_line:
                        param_string = data[:64]
                        directory_pointer = int(data[64:72].strip())
                        first_param_line = False
                    else:
                        param_string += data[:64]

                    if param_string.strip()[-1] == record_sep:
                        first_param_line = True
                        param_string = param_string.strip()[:-1]
                        parameters = param_string.split(param_sep)
                        this_entity = entity_list[pointer_dict[directory_pointer]]
                        try:
                            this_entity._add_parameters(parameters)
                        except Exception as err:
                            print(
                                "Warning: Could not initialize entity from parameters with Parameter section "
                                "ending on line {}. Possibly wrong or (yet) unsupported format. Entity will be discarded.".format(
                                    line_no
                                )
                            )
                            entities_to_discard.append(this_entity)

                elif id_code == "T":  # Terminate
                    pass

        for e in entities_to_discard:
            try:
                entity_list.remove(e)
            except:
                pass

        self._entities = entity_list
        self.desc = desc
        self._pointers = pointer_dict

    def __getitem__(self, index):
        """Get an item by its pointer"""
        return self._entities[self._pointers[index]]

    @property
    def items(self):
        """IGES items

        Examples
        --------
        >>> from pyiges import examples
        >>> import pyiges
        >>> sample = pyiges.read(examples.sample)
        >>> item = sample.items[0]
        >>> item
        --- IGES Point ---
        0.0, 0.0, 0.0
        """
        return self._entities


def read(filename):
    """Read an iges file.


    Parameters
    ----------
    filename : str
        Filename of an IGES file.

    Examples
    --------
    >>> import pyiges
    >>> from pyiges import examples
    >>> iges = pyiges.read(examples.impeller)
        pyiges.Iges object
        Description:
        Number of Entities: 4615
    """
    return Iges(filename)
