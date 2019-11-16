import os

from geomdl import NURBS, BSpline, utilities
import numpy as np
import vtk
import pyvista as pv

from pyiges.entity import Entity


class Line(Entity):
    """Straight line segment"""

    def _add_parameters(self, parameters):
        self.x1 = float(parameters[1])
        self.y1 = float(parameters[2])
        self.z1 = float(parameters[3])
        self.x2 = float(parameters[4])
        self.y2 = float(parameters[5])
        self.z2 = float(parameters[6])

    def __str__(self):
        s = '--- Line ---' + os.linesep
        s += Entity.__str__(self) + os.linesep
        s += "From point {0}, {1}, {2} {3}".format(self.x1, self.y1, self.z1, os.linesep)
        s += "To point {0}, {1}, {2}".format(self.x2, self.y2, self.z2)
        return s

    def to_vtk(self, resolution=1):
        return pv.Line([self.x1, self.y1, self.z1],
                       [self.x2, self.y2, self.z2], resolution)


class ConicArc(Entity):
    """Conic Arc (Type 104)
    Arc defined by the equation: Axt^2 + Bxtyt + Cyt^2 + Dxt + Eyt
    + F = 0, with a Transformation Matrix (Entity 124). Can define
    an ellipse, parabola, or hyperbola.

    The definitions of the terms ellipse, parabola, and hyperbola
    are given in terms of the quantities Q1, Q2, and Q3. These
    quantities are:

        |  A   B/2  D/2 |        |  A   B/2 | 
    Q1= | B/2   C   E/2 |   Q2 = | B/2   C  |   Q3 = A + C 
        | D/2  E/2   F  | 
    A parent conic curve is:

    An ellipse if Q2 > 0 and Q1, Q3 < 0.
    A hyperbola if Q2 < 0 and Q1 != 0.
    A parabola if Q2 = 0 and Q1 != 0.
    """

    def _add_parameters(self, parameters):
        """
        Index	Type	Name	Description
        1	REAL	A	coefficient of xt^2
        2	REAL	B	coefficient of xtyt
        3	REAL	C	coefficient of yt^2
        4	REAL	D	coefficient of xt
        5	REAL	E	coefficient of yt
        6	REAL	F	scalar coefficient
        7	REAL	X1	x coordinate of start point
        8	REAL	Y1	y coordinate of start point
        9	REAL	Z1	z coordinate of start point
        10	REAL	X2	x coordinate of end point
        11	REAL	Y2	y coordinate of end point
        12	REAL	Z2	z coordinate of end point
        """
        self.a = parameters[1]  #  coefficient of xt^2
        self.b = parameters[2]  #  coefficient of xtyt
        self.c = parameters[3]  #  coefficient of yt^2
        self.d = parameters[4]  #  coefficient of xt
        self.e = parameters[5]  #  coefficient of yt
        self.f = parameters[6]  #  scalar coefficient
        self.x1 = parameters[7]  #  x coordinate of start point
        self.y1 = parameters[8]  #  y coordinate of start point
        self.z1 = parameters[9]  #  z coordinate of start point
        self.x2 = parameters[10]  #  x coordinate of end point
        self.y2 = parameters[11]  #  y coordinate of end point
        self.z2 = parameters[12]  #  z coordinate of end point

    def __repr__(self):
        info = 'Conic Arc\nIGES Type 104\n'
        info += 'Start:  (%f, %f, %f)\n' % (self.x1, self.y1, self.z1)
        info += 'End:    (%f, %f, %f)\n' % (self.x2, self.y2, self.z2)
        info += 'Coefficient of xt^2: %f' % self.a
        info += 'Coefficient of xtyt: %f' % self.b
        info += 'Coefficient of yt^2: %f' % self.c
        info += 'Coefficient of xt:   %f' % self.d
        info += 'Coefficient of yt:   %f' % self.e
        info += 'Scalar coefficient:  %f' % self.f
        return info

    def to_vtk(self):
        raise NotImplementedError('Not yet implemented')

class RationalBSplineCurve(Entity):
    """Rational B-Spline Curve
    IGES Spec v5.3 p. 123 Section 4.23
    See also Appendix B, p. 545
    """

    def _add_parameters(self, parameters):
        self.K = int(parameters[1])
        self.M = int(parameters[2])
        self.prop1 = int(parameters[3])
        self.prop2 = int(parameters[4])
        self.prop3 = int(parameters[5])
        self.prop4 = int(parameters[6])
        
        self.N = 1 + self.K - self.M
        self.A = self.N + 2 * self.M

        # Knot sequence
        self.T = []
        for i in range(7, 7 + self.A + 1):
            self.T.append(float(parameters[i]))

        # Weights
        self.W = []
        for i in range(self.A + 8, self.A + self.K + 8):
            self.W.append(float(parameters[i]))

        # Control points
        self.control_points = []
        for i in range(9 + self.A + self.K, 9 + self.A + 4*self.K + 1, 3):
            point = (float(parameters[i]), float(parameters[i+1]), float(parameters[i+2]))
            self.control_points.append(point)

        # Parameter values
        self.V0 = float(parameters[12 + self.A + 4 * self.K])
        self.V1 = float(parameters[13 + self.A + 4 * self.K])

        # Unit normal (only for planar curves)
        if len(parameters) > 14 + self.A + 4 * self.K + 1:
            self.planar_curve = True
            self.XNORM = float(parameters[14 + self.A + 4 * self.K])
            self.YNORM = float(parameters[15 + self.A + 4 * self.K])
            self.ZNORM = float(parameters[16 + self.A + 4 * self.K])
        else:
            self.planar_curve = False

    def __str__(self):
        s = '--- Rational B-Spline Curve ---' + os.linesep
        s += Entity.__str__(self) + os.linesep
        s += str(self.T) + os.linesep
        s += str(self.W) + os.linesep
        s += str(self.control_points) + os.linesep
        s += "Parameter: v(0) = {0}    v(1) = {1}".format(self.V0, self.V1) + os.linesep
        if self.planar_curve:
            s += "Unit normal: {0} {1} {2}".format(self.XNORM, self.YNORM, self.ZNORM)
        return s

    def to_vtk(self, delta=0.01):
        """Set evaluation delta (controls the number of curve points)
        """
        # Create a 3-dimensional B-spline Curve
        curve = NURBS.Curve()
        curve.degree = self.M
        curve.ctrlpts = self.control_points  # Set control points (weights vector will be 1 by default)
        curve.weights = self.W + [1]
        curve.knotvector = self.T  # Set knot vector
        curve.delta = delta
        curve_points = np.array(curve.evalpts)

        return pv.Spline(curve_points)


class RationalBSplineSurface(Entity):

    def _add_parameters(self, input_parameters):
        parameters = np.empty(len(input_parameters))
        parameters[:] = input_parameters

        self.k1 = int(parameters[1])  # Upper index of first sum
        self.k2 = int(parameters[2])  # Upper index of second sum
        self.m1 = int(parameters[3])  # Degree of first basis functions
        self.m2 = int(parameters[4])  # Degree of second basis functions
        self.flag1 = bool(parameters[5])  # 0=closed in first direction, 1=not closed
        self.flag2 = bool(parameters[6])  # 0=closed in second direction, 1=not closed
        self.flag3 = bool(parameters[7])  # 0=rational, 1=polynomial
        self.flag4 = bool(parameters[8])  # 0=nonperiodic in first direction , 1=periodic
        self.flag5 = bool(parameters[9])  # 0=nonperiodic in second direction , 1=periodic

        # load knot sequences
        # knot1 = np.append(parameters[10:11 + self.k2 + self.m1-1], [1, 1])
        self.knot1 = parameters[10:12 + self.k1 + self.m1]
        self.knot2 = parameters[12 + self.k1 + self.m1: 14 + self.k2 + self.m1 + self.k1 + self.m2]

        # weights
        st = 14 + self.k2 + self.m1 + self.k1 + self.m2
        en = st + (1 + self.k2)*(1 + self.k1)
        self.weights = parameters[st:en]

        # control points
        st = 14 + self.k2 + self.k1 + self.m1 + self.m2 + (1 + self.k2)*(1 + self.k1)
        en = st + 3*(1 + self.k2)*(1 + self.k1)
        self.cp = parameters[st:en].reshape(-1, 3)

        self.u0 = parameters[-3]  # Start first parameter value
        self.u1 = parameters[-2]  # End first parameter value
        self.v0 = parameters[-1]  # Start second parameter value
        self.v1 = parameters[-0]  # End second parameter value

    def to_vtk(self, delta=0.025):
        
        surf = BSpline.Surface()

        # Set degrees
        surf.degree_u = self.m2
        surf.degree_v = self.m1

        cp2d = self.cp.reshape(self.k2 + 1, self.k1 + 1, 3)
        surf.ctrlpts2d = cp2d.tolist()

        # surf.knotvector_u = utilities.generate_knot_vector(surf.degree_u, surf.ctrlpts_size_u)
        surf.knotvector_u = self.knot2
        surf.knotvector_v = self.knot1
        # surf.knotvector_v = utilities.generate_knot_vector(surf.degree_v, surf.ctrlpts_size_v)

        # Set evaluation delta
        surf.delta = delta

        surf.weights = self.weights

        # Evaluate surface points
        surf.evaluate()

        faces = []
        for face in surf.faces:
            faces.extend([3] + face.vertex_ids)

        return pv.PolyData(np.array(surf.vertices), np.array(faces))


class CircularArc(Entity):
    """Circular Arc

    Type 100: Simple circular arc of constant radius. Usually defined
    with a Transformation Matrix Entity (Type 124).

    Notes
    -----
    Index in list    Type of data    Name    Description
    1                REAL            Z       z displacement on XT,YT plane
    2                REAL            X       x coordinate of center
    3                REAL            Y       y coordinate of center
    4                REAL            X1      x coordinate of start
    5                REAL            Y1      y coordinate of start
    6                REAL            X2      x coordinate of end
    7                REAL            Y2      y coordinate of end
    """

    def _add_parameters(self, parameters):
        self.z = float(parameters[1])
        self.y = float(parameters[2])
        self.x = float(parameters[3])
        self.x1 = float(parameters[4])
        self.y1 = float(parameters[5])
        self.x2 = float(parameters[6])
        self.y2 = float(parameters[7])

    def to_vtk(self, resolution=20):
        arc = pv.CircularArc([self.x1, self.y1, 0],
                             [self.x2, self.y2, 0],
                             [self.x, self.y, 0],
                             resolution=resolution,
                             normal=[0, 0, 1])
        return arc.extrude([0, 0, self.z])

    def __repr__(self):
        info = 'Circular Arc\nIGES Type 100\n'
        info += 'Center: (%f, %f)\n' % (self.x, self.y)
        info += 'Start:  (%f, %f)\n' % (self.x1, self.y1)
        info += 'End:    (%f, %f)\n' % (self.x2, self.y2)
        info += 'Z Disp: %f' % self.z
        return info
