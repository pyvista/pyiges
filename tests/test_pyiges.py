import numpy as np
import pytest

import pyiges
from pyiges import examples


@pytest.fixture(scope='module')
def sample():
    return pyiges.read(examples.sample)


@pytest.fixture(scope='module')
def impeller():
    return pyiges.read(examples.impeller)


@pytest.fixture(scope='module')
def surf(impeller):
    return impeller.bspline_surfaces()[0] # pyiges.geometry.RationalBSplineSurface


@pytest.fixture(scope='module')
def curve(impeller):
    return impeller.bsplines(as_vtk=False)[0] # geometry.RationalBSplineCurve


@pytest.fixture(scope='module')
def point(sample):
    return sample.points(as_vtk=False, merge=False)[0] # pyiges.geometry.Point


@pytest.fixture(scope='module')
def carc(impeller):
    return impeller.circular_arcs()[0] # pyiges.geometry.CircularArc


@pytest.fixture(scope='module')
def trafo(impeller):
    return impeller._entities[172] # pyiges.geometry.Transformation


@pytest.fixture(scope='module')
def line(impeller):
    return impeller.lines()[0] # pyiges.geometry.Line


@pytest.fixture(scope='module')
def entity(impeller):
    return impeller._entities[0] # pyiges.entity.Entity


def test_str(sample):
    assert 'Number of Entities: 5' in str(sample)


def test_get_item(sample):
    assert '0.0, 0.0, 0.0' in str(sample.items[0])
    assert '0.0, 0.0, 0.0' in str(sample[1])


def test_parse_completeness1(impeller):
    assert len(impeller.bspline_surfaces()) == 247
    assert len(impeller.bsplines()) == 2342
    assert len(impeller.circular_arcs()) == 468
    assert len(impeller.conic_arcs()) == 0
    assert len(impeller.edge_lists()) == 0
    assert len(impeller.faces()) == 0
    assert len(impeller.lines()) == 98
    assert len(impeller.loops()) == 0
    assert len(impeller.points()) == 0
    assert len(impeller.vertex_lists()) == 0


def test_parse_completeness2(sample):
    assert len(sample.bspline_surfaces()) == 0
    assert len(sample.bsplines()) == 0
    assert len(sample.circular_arcs()) == 0
    assert len(sample.conic_arcs()) == 0
    assert len(sample.edge_lists()) == 0
    assert len(sample.faces()) == 0
    assert len(sample.lines()) == 0
    assert len(sample.loops()) == 0
    assert len(sample.points()) == 4
    assert len(sample.vertex_lists()) == 0


@pytest.mark.parametrize('merge', [False, True])
def test_iges_to_vtk1(impeller, merge):
    items = impeller.to_vtk(delta=0.5, merge=merge)
    assert items.bounds == pytest.approx((-50.516562808,  49.445007453, -49.510005208,
                                          50.494748866, -997.9630126953125, 1011.0750122070312))

@pytest.mark.parametrize('merge', [False, True])
def test_iges_to_vtk2(sample, merge):
    items = sample.to_vtk(merge=merge)
    assert items.bounds == pytest.approx((0.0, 1.0, 0.0, 1.0, 0.0, 0.0))


def test_surfaces_vtk(surf):
    mesh = surf.to_vtk(delta=0.1)

    assert mesh.area == pytest.approx(277.4757547644264)
    assert mesh.n_arrays == 0
    assert mesh.n_cells == 162
    assert mesh.n_faces == 162
    assert mesh.n_lines == 0
    assert mesh.n_open_edges == 36
    assert mesh.n_points == 100
    assert mesh.n_strips == 0
    assert mesh.n_verts == 0

    assert mesh.bounds == pytest.approx((-30.547425187, -26.209437969209873, -16.775362758,
                                         -9.363301218200274, -45.772995131000016, -8.876323512))


def test_surfaces_parse(surf):
    assert surf.parameters == []
    assert surf.sequence_number == 3

    assert surf.flag1 is False
    assert surf.flag2 is False
    assert surf.flag3 is False
    assert surf.flag4 is False
    assert surf.flag5 is False
    assert surf.k1 == 3
    assert surf.k2 == 3
    assert surf.m1 == 3
    assert surf.m2 == 3
    assert surf.u0 == 1.
    assert surf.u1 == 0.
    assert surf.v0 == 1.
    assert surf.v1 == 128.

    assert surf.knot1 == pytest.approx([0., 0., 0., 0., 1., 1., 1., 1.])
    assert surf.knot2 == pytest.approx([0., 0., 0., 0., 1., 1., 1., 1.])

    assert surf.weights == pytest.approx(np.array(
        [1., 0.99569778, 0.99569778, 1., 0.99516272,
         0.9908813, 0.9908813, 0.99516272, 0.99516272, 0.9908813,
         0.9908813, 0.99516272, 1., 0.99569778, 0.99569778, 1.]
    ))

    assert surf.control_points() == pytest.approx(np.array(
        [[-26.90290533, -16.51153913,  -8.87632351],
         [-25.85182035, -15.86644037, -21.16779478],
         [-25.99572556, -15.95476156, -33.51982653],
         [-27.33276363, -16.77536276, -45.77299513],
         [-28.23297477, -14.34440426,  -8.87632351],
         [-27.12992455, -13.78397453, -21.16779478],
         [-27.28094438, -13.86070358, -33.51982653],
         [-28.6840851 , -14.57360111, -45.77299513],
         [-29.29280315, -12.03305788,  -8.87632351],
         [-28.14834588, -11.56293146, -21.16779478],
         [-28.3050348 , -11.62729699, -33.51982653],
         [-29.76084756, -12.22532372, -45.77299513],
         [-30.06701039,  -9.61104189,  -8.87632351],
         [-28.89230518,  -9.2355426 , -21.16779478],
         [-29.05313537,  -9.28695263, -33.51982653],
         [-30.54742519,  -9.76460843, -45.77299513]]
    ))

    assert surf.d == {
        'entity_type_number': 128,
        'parameter_pointer': 2,
        'structure': 0,
        'line_font_pattern': 0,
        'level': 0,
        'view': None,
        'transform': None,
        'label_assoc': 0,
        'status_number': 1010000,
        'line_weight_number': 0,
        'color_number': 0,
        'param_line_count': 18,
        'form_number': 0,
        'entity_label': '',
        'entity_subs_num': 0,
    }
    assert repr(surf)
    assert str(surf)


def test_bsplines_parse(curve):
    assert curve.parameters == []
    assert curve.sequence_number == 5

    assert curve.A == 17
    assert curve.K == 14
    assert curve.M == 2
    assert curve.N == 13
    assert curve.V0 == pytest.approx(0.0)
    assert curve.V1 == pytest.approx(1.0)
    assert curve.XNORM == pytest.approx(0.0)
    assert curve.YNORM == pytest.approx(0.0)
    assert curve.ZNORM == pytest.approx(1.0)
    assert curve.prop1 == 1
    assert curve.prop2 == 0
    assert curve.prop3 == 1
    assert curve.prop4 == 0

    assert curve.T == pytest.approx([0.0, 0.0, 0.0, 0.25, 0.25, 0.375,
                                     0.375, 0.5, 0.5, 0.625, 0.625,
                                     0.75, 0.75, 0.875, 0.875, 1.0,
                                     1.0, 1.0, ])

    assert curve.W == pytest.approx([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                                     1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    assert curve.d == {
        'entity_type_number': 126,
        'parameter_pointer': 20,
        'structure': 0,
        'line_font_pattern': 0,
        'level': 0,
        'view': None,
        'transform': None,
        'label_assoc': 0,
        'status_number': 1010500,
        'line_weight_number': 0,
        'color_number': 0,
        'param_line_count': 10,
        'form_number': 0,
        'entity_label': '',
        'entity_subs_num': 0,
    }
    assert repr(curve)
    assert str(curve)


def test_bsplines_vtk(curve):
    mesh = curve.to_vtk()

    assert mesh.area == 0.0
    assert mesh.n_arrays == 0
    assert mesh.n_cells == 1
    assert mesh.n_faces == 1
    assert mesh.n_lines == 1
    assert mesh.n_open_edges == 0
    assert mesh.n_points == 100
    assert mesh.n_strips == 0
    assert mesh.n_verts == 0

    assert mesh.bounds == pytest.approx((0.531027642, 0.559345007,
                                         0.006617509, 0.127235606, 0., 0.))


def test_points_vtk(sample):
    points = sample.points(as_vtk=True, merge=True) # pv.PolyData

    assert points.n_cells == 4
    assert points.n_faces == 4
    assert points.n_lines == 0
    assert points.n_open_edges == 0
    assert points.n_points == 4
    assert points.n_strips == 0
    assert points.n_verts == 4

    assert points.bounds == pytest.approx((0.0, 1.0, 0.0, 1.0, 0.0, 0.0))
    assert points.points == pytest.approx(np.array([[0., 0., 0.],
                                                    [1., 0., 0.],
                                                    [1., 1., 0.],
                                                    [0., 1., 0.]]))


def test_points_parse(sample):
    points = sample.points(as_vtk=False, merge=True) # pyiges.geometry.Point

    assert points[0].coordinate == pytest.approx((0., 0., 0.))
    assert points[1].coordinate == pytest.approx((1., 0., 0.))
    assert points[2].coordinate == pytest.approx((1., 1., 0.))
    assert points[3].coordinate == pytest.approx((0., 1., 0.))

    assert points[0].parameters == []
    assert points[1].parameters == []
    assert points[2].parameters == []
    assert points[3].parameters == []

    assert points[0].sequence_number == 1
    assert points[1].sequence_number == 3
    assert points[2].sequence_number == 5
    assert points[3].sequence_number == 7

    assert points[3].d == {
        'entity_type_number': 116,
        'parameter_pointer': 7,
        'structure': 0,
        'line_font_pattern': 0,
        'level': 0,
        'view': 0,
        'transform': 0,
        'label_assoc': 0,
        'status_number': 1,
        'line_weight_number': 0,
        'color_number': 0,
        'param_line_count': 2,
        'form_number': 0,
        'entity_label': 'POINT',
        'entity_subs_num': 4,
    }
    assert repr(sample)
    assert str(sample)


def test_point_parse(point):
    assert point.parameters == []
    assert point.sequence_number == 1

    assert point.coordinate == pytest.approx(np.array([0., 0., 0.]))

    assert point.d == {
        'entity_type_number': 116,
        'parameter_pointer': 1,
        'structure': 0,
        'line_font_pattern': 0,
        'level': 0,
        'view': 0,
        'transform': 0,
        'label_assoc': 0,
        'status_number': 1,
        'line_weight_number': 0,
        'color_number': 0,
        'param_line_count': 2,
        'form_number': 0,
        'entity_label': 'POINT',
        'entity_subs_num': 1,
    }
    assert repr(point)
    assert str(point)


def test_point_vtk(point):
    point = point.to_vtk() # pv.PolyData

    assert point.n_arrays == 0
    assert point.n_cells == 1
    assert point.n_faces == 1
    assert point.n_lines == 0
    assert point.n_open_edges == 0
    assert point.n_points == 1
    assert point.n_strips == 0
    assert point.n_verts == 1

    assert point.bounds == pytest.approx((0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    assert point.points == pytest.approx(np.array([[0., 0., 0.]]))


def test_circular_arcs_parse(carc):
    assert carc.parameters == []
    assert carc.sequence_number == 19

    assert carc.x == pytest.approx(0.0)
    assert carc.x1 == pytest.approx(-29.279537336)
    assert carc.x2 == pytest.approx(-28.792209864)
    assert carc.y == pytest.approx(0.0)
    assert carc.y1 == pytest.approx(-9.405469593)
    assert carc.y2 == pytest.approx(-10.805684432)
    assert carc.z == pytest.approx(-25.115661529)

    assert carc.d == {
        'entity_type_number': 100,
        'parameter_pointer': 86,
        'structure': 0,
        'line_font_pattern': 0,
        'level': 0,
        'view': None,
        'transform': None,
        'label_assoc': 0,
        'status_number': 1010000,
        'line_weight_number': 0,
        'color_number': 0,
        'param_line_count': 2,
        'form_number': 0,
        'entity_label': '',
        'entity_subs_num': 0,
    }
    assert repr(carc)
    assert str(carc)


def test_circular_arcs_vtk(carc):
    polydata = carc.to_vtk()

    assert polydata.n_arrays == 2
    assert polydata.n_cells == 1
    assert polydata.n_faces == 1
    assert polydata.n_lines == 1
    assert polydata.n_points == 21
    assert polydata.n_strips == 0
    assert polydata.n_verts == 0

    assert polydata.bounds == pytest.approx((
        -29.2795372009277, -28.79220962524414, -10.80568408966064,
        -9.40546989440918, -25.11566162109375, -25.11566162109375,
    ))
    assert polydata.points == pytest.approx(np.array(
        [[-29.279537, -9.4054700, -25.115662],
         [-29.256779, -9.4760270, -25.115662],
         [-29.233849, -9.5465290, -25.115662],
         [-29.210750, -9.6169760, -25.115662],
         [-29.187483, -9.6873665, -25.115662],
         [-29.164043, -9.7577010, -25.115662],
         [-29.140436, -9.8279780, -25.115662],
         [-29.116660, -9.8981990, -25.115662],
         [-29.092712, -9.9683620, -25.115662],
         [-29.068598, -10.038467, -25.115662],
         [-29.044313, -10.108514, -25.115662],
         [-29.019860, -10.178502, -25.115662],
         [-28.995237, -10.248431, -25.115662],
         [-28.970448, -10.318300, -25.115662],
         [-28.945490, -10.388110, -25.115662],
         [-28.920362, -10.457859, -25.115662],
         [-28.895067, -10.527547, -25.115662],
         [-28.869604, -10.597175, -25.115662],
         [-28.843973, -10.666739, -25.115662],
         [-28.818176, -10.736243, -25.115662],
         [-28.792210, -10.805684, -25.115662]]
    ))


def test_entity_parse(entity):
    assert entity.parameters[0][0] == '314'
    assert entity.sequence_number == 1

    assert list(map(float, entity.parameters[0][1:4])) == pytest.approx(
        [75.2941176, 75.2941176, 75.2941176]
    )

    assert entity.d == {
        'entity_type_number': 314,
        'parameter_pointer': 1,
        'structure': 0,
        'line_font_pattern': 0,
        'level': 0,
        'view': None,
        'transform': None,
        'label_assoc': 0,
        'status_number': 200,
        'line_weight_number': 0,
        'color_number': 8,
        'param_line_count': 1,
        'form_number': 0,
        'entity_label': '',
        'entity_subs_num': 0,
    }
    assert str(entity)
    assert repr(entity)


def test_line_parse(line):
    assert line.parameters == []
    assert line.sequence_number == 333

    assert line.coordinates == pytest.approx(np.array(
        [[0., 0., -997.96301316],
         [0., 0., 2.03698684]]
    ))

    assert line.d == {
        'entity_type_number': 110,
        'parameter_pointer': 1213,
        'structure': 0,
        'line_font_pattern': 0,
        'level': 0,
        'view': None,
        'transform': None,
        'label_assoc': 0,
        'status_number': 1010000,
        'line_weight_number': 0,
        'color_number': 0,
        'param_line_count': 1,
        'form_number': 0,
        'entity_label': '',
        'entity_subs_num': 0,
    }
    assert repr(line)
    assert str(line)


def test_line_vtk(line):
    polydata = line.to_vtk()
    assert polydata.n_arrays == 2
    assert polydata.n_cells == 1
    assert polydata.n_faces == 1
    assert polydata.n_lines == 1
    assert polydata.n_open_edges == 0
    assert polydata.n_open_edges == 0
    assert polydata.n_points == 2
    assert polydata.n_strips == 0
    assert polydata.n_verts == 0

    assert polydata.bounds == pytest.approx((0.0, 0.0, 0.0, 0.0, -997.9630126, 2.0369868))
    assert polydata.points == pytest.approx(np.array([[0., 0., -997.963],
                                                      [0., 0., 2.0369868]]))


def test_transformation_parse(trafo):
    assert trafo.parameters == []
    assert trafo.sequence_number == 345

    assert trafo.r11 == pytest.approx(1.0)
    assert trafo.r12 == pytest.approx(-7.35035671743047e-15)
    assert trafo.r13 == pytest.approx(8.55166289179392e-31)
    assert trafo.r21 == pytest.approx(-7.35035671743047e-15)
    assert trafo.r22 == pytest.approx(-1.0)
    assert trafo.r23 == pytest.approx(6.98296267768627e-15)
    assert trafo.r31 == pytest.approx(-5.04721003363181e-29)
    assert trafo.r32 == pytest.approx(-6.98296267768627e-15)
    assert trafo.r33 == pytest.approx(-1.0)
    assert trafo.t1 == pytest.approx(-2.42609551059902e-30)
    assert trafo.t2 == pytest.approx(-1.98105732386527e-14)
    assert trafo.t3 == pytest.approx(5.67397368511119)

    assert trafo.d == {
        'entity_type_number': 124,
        'parameter_pointer': 1221,
        'structure': 0,
        'line_font_pattern': 0,
        'level': 0,
        'view': None,
        'transform': None,
        'label_assoc': 0,
        'status_number': 0,
        'line_weight_number': 0,
        'color_number': 0,
        'param_line_count': 5,
        'form_number': 0,
        'entity_label': '',
        'entity_subs_num': 0,
    }
    assert repr(trafo)
    assert str(trafo)

def test_transformation_vtk(trafo):
    trafo = trafo._to_vtk()
    m = trafo.GetMatrix()
    assert m.GetElement(2,3) == pytest.approx(5.67397368511119)

def test_to_vtk(impeller):
    lines = impeller.to_vtk(lines=True, bsplines=False, surfaces=False)
    assert lines.n_points
    assert lines.n_cells

@pytest.mark.parametrize('line, expected_separators', [
    # possible forms 1-4, see http://paulbourke.net/dataformats/iges/IGES.pdf
    # p. 15
    (',,', (',', ';')),
    ('1Haa1Hba', ('a', 'b')),
    ('1Haaa', ('a', ';')),
    (',1Hb,', (',', 'b')),
    # typical special case of form 2
    ('1H,,1H;,', (',', ';')),
    # invalid forms
    ('xyz', None),
    (',2H', None),
    ('1Hxy', None),
])
def test_parse_separators_from_first_global_line(line, expected_separators):
    if expected_separators is None:
        with pytest.raises(RuntimeError, match='Invalid Global section format'):
            pyiges.Iges._parse_separators_from_first_global_line(line)
    else:
        separators = pyiges.Iges._parse_separators_from_first_global_line(line)
        assert separators == expected_separators
