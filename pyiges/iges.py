import pyvista
import vtk
from tqdm import tqdm

from pyiges.reader import read_entities
from pyiges.curves_surfaces import (Line, RationalBSplineCurve, RationalBSplineSurface)


class Iges():
    """IGES object"""

    def __init__(self, filename):
        self._entities, self._desc = read_entities(filename)

    def to_vtk(self, bsplines=True, surfaces=True, delta=0.025, merge=True):
        """Converts entities to vtk object"""
        items = pyvista.MultiBlock()
        for entity in tqdm(self, desc='Converting entities to vtk'):
            if isinstance(entity, RationalBSplineCurve) and bsplines:
                items.append(entity.to_vtk(delta))
            elif isinstance(entity, RationalBSplineSurface) and surfaces:
                items.append(entity.to_vtk(delta))

        # merge to a single mesh
        if merge:
            afilter = vtk.vtkAppendPolyData()
            for item in items:
                afilter.AddInputData(item)
            afilter.Update()

            return pyvista.wrap(afilter.GetOutput())

        return items

    @property
    def bsplines(self):
        items = []
        for entity in self:
            if isinstance(entity, RationalBSplineCurve):
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
