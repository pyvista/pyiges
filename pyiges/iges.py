import pyvista
import vtk
from tqdm import tqdm

from pyiges.reader import read_entities
from pyiges.curves_surfaces import (Line, RationalBSplineCurve, RationalBSplineSurface,
                                    CircularArc)


class Iges():
    """IGES object"""

    def __init__(self, filename):
        self._entities, self._desc = read_entities(filename)

    def to_vtk(self, lines=True, bsplines=True,
               surfaces=True, delta=0.025, merge=True):
        """Converts entities to vtk object"""
        items = []
        for entity in tqdm(self, desc='Converting entities to vtk'):
            if isinstance(entity, RationalBSplineCurve) and bsplines:
                items.append(entity.to_vtk(delta))
            elif isinstance(entity, RationalBSplineSurface) and surfaces:
                items.append(entity.to_vtk(delta))
            elif isinstance(entity, Line) and lines:
                items.append(entity.to_vtk())

        # merge to a single mesh
        if merge:
            afilter = vtk.vtkAppendPolyData()
            for item in items:
                afilter.AddInputData(item)
            afilter.Update()

            return pyvista.wrap(afilter.GetOutput())

        return items

    def lines(self, as_vtk=False, **kwargs):
        """All lines"""
        return self._return_type(Line, as_vtk, **kwargs)

    def bsplines(self, as_vtk=False, **kwargs):
        """All bsplines"""
        return self._return_type(RationalBSplineCurve, as_vtk, **kwargs)

    def circular_arcs(self, as_vtk=False, **kwargs):
        """All circular_arcs"""
        return self._return_type(CircularArc, as_vtk, **kwargs)

    def _return_type(self, iges_type, as_vtk=False, **kwargs):
        """Return all of an iges type"""
        items = []
        for entity in self:
            if isinstance(entity, iges_type):
                if as_vtk:
                    items.append(entity.as_vtk(**kwargs))
                else:
                    items.append(entity)
        return items

    def __getitem__(self, indices):
        return self._entities[indices]

    def __iter__(self):
        for entity in self._entities:
            yield entity

    def __len__(self):
        return len(self._entities)

    def __repr__(self):
        info = 'pyiges.Iges object\n'
        info += 'Description: %s\n' % self._desc
        info += 'Number of Entities: %d' % len(self)
        return info

def read(filename):
    """Read an iges file"""
    return Iges(filename)
