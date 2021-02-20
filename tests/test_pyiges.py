import pytest

import pyiges
from pyiges import examples


@pytest.fixture(scope='module')
def sample():
    return pyiges.read(examples.sample)


@pytest.fixture(scope='module')
def impeller():
    return pyiges.read(examples.impeller)


def test_str(sample):
    assert 'Number of Entities: 5' in str(sample)


def test_get_item(sample):
    assert '0.0, 0.0, 0.0' in str(sample.items[0])


def test_surfaces(impeller):
    surfaces = impeller.bspline_surfaces()
    mesh = surfaces[0].to_vtk(delta=0.1)
    assert mesh.n_cells
    assert mesh.n_points


def test_bsplines(impeller):
    curves = impeller.bsplines()
    mesh = curves[0].to_vtk()
    assert mesh.n_cells == 1
    assert mesh.n_points


def test_points(sample):
    points = sample.points(as_vtk=True, merge=True)
    assert points.n_points == 4


def test_to_vtk(impeller):
    lines = impeller.to_vtk(lines=True, bsplines=False, surfaces=False)
    assert lines.n_points
    assert lines.n_cells
