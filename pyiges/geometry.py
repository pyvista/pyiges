import os

from geomdl import NURBS, BSpline
import numpy as np
import pyvista as pv

from pyiges.entity import Entity


class Point(Entity):
    """Straight line segment"""

    def _add_parameters(self, parameters):
        self.x = float(parameters[1])
        self.y = float(parameters[2])
        self.z = float(parameters[3])

    def __str__(self):
        s = '--- Point ---' + os.linesep
        s += Entity.__str__(self) + os.linesep
        s += "{0}, {1}, {2} {3}".format(self.x, self.y, self.z, os.linesep)
        return s

    def to_vtk(self):
        return pv.PolyData([self.x, self.y, self.z])


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
    Arc defined by the equation: 
    ``A*x**2 + B*x*y + C*y**2 + D*x + E*y + F = 0``

    with a Transformation Matrix (Entity 124). Can define
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
        info += 'Coefficient of x**2: %f' % self.a
        info += 'Coefficient of x*y:  %f' % self.b
        info += 'Coefficient of y**2: %f' % self.c
        info += 'Coefficient of x:    %f' % self.d
        info += 'Coefficient of y:    %f' % self.e
        info += 'Scalar coefficient:  %f' % self.f
        return info

    def to_vtk(self):

        # a*x**2 + b*x*y + c*y**2 + d*x + e*y + f = 0
        # from sympy import Symbol
        # from sympy.solvers import Solve
        # a = Symbol('a')
        # b = Symbol('b')
        # c = Symbol('c')
        # d = Symbol('d')
        # e = Symbol('e')
        # f = Symbol('f')
        # x = Symbol('x')
        # y = Symbol('y')
        # solve(a*x**2 + b*x*y + c*y**2 + d*x + e*y + f, x)

        # x0 = (-b*y - d + sqrt(-4*a*c*y**2 - 4*a*e*y - 4*a*f + b**2*y**2 + 2*b*d*y + d**2))/(2*a)
        # x1 = -(b*y + d + sqrt(-4*a*c*y**2 - 4*a*e*y - 4*a*f + b**2*y**2 + 2*b*d*y + d**2))/(2*a)

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

    def to_geomdl(self):
        curve = NURBS.Curve()
        curve.degree = self.M
        curve.ctrlpts = self.control_points
        curve.weights = self.W + [1]
        curve.knotvector = self.T  # Set knot vector
        return curve

    def to_vtk(self, delta=0.01):
        """Set evaluation delta (controls the number of curve points)
        """
        # Create a 3-dimensional B-spline Curve
        curve = self.to_geomdl()
        curve.delta = delta

        # spline segfaults here sometimes...
        # return pv.Spline(np.array(curve.evalpts))
        faces = np.arange(-1, 100)
        faces[0] = 100
        line = pv.PolyData()
        line.points = np.array(curve.evalpts)
        line.lines = faces
        return line


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

    def to_geomdl(self):
        surf = BSpline.Surface()

        # Set degrees
        surf.degree_u = self.m2
        surf.degree_v = self.m1

        # set control points and knots
        cp2d = self.cp.reshape(self.k2 + 1, self.k1 + 1, 3)
        surf.ctrlpts2d = cp2d.tolist()
        surf.knotvector_u = self.knot2
        surf.knotvector_v = self.knot1

        # set weights
        surf.weights = self.weights
        return surf

    def to_vtk(self, delta=0.025):
        surf = self.to_geomdl()
        # Set evaluation delta
        surf.delta = delta

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
        self.x = float(parameters[2])
        self.y = float(parameters[3])
        self.x1 = float(parameters[4])
        self.y1 = float(parameters[5])
        self.x2 = float(parameters[6])
        self.y2 = float(parameters[7])

    def to_vtk(self, resolution=20):
        start = [self.x1, self.y1, 0]
        end = [self.x2, self.y2, 0]
        center = [self.x, self.y, 0],
        arc = pv.CircularArc(center=center,
                             pointa=start,
                             pointb=end,
                             resolution=resolution)
        arc.points += [0, 0, self.z]
        return arc

    def __repr__(self):
        info = 'Circular Arc\nIGES Type 100\n'
        info += 'Center: (%f, %f)\n' % (self.x, self.y)
        info += 'Start:  (%f, %f)\n' % (self.x1, self.y1)
        info += 'End:    (%f, %f)\n' % (self.x2, self.y2)
        info += 'Z Disp: %f' % self.z
        return info


class Face(Entity):
    """Defines a bound portion of three dimensional space (R^3) which
    has a finite area. Used to construct B-Rep Geometries."""

    def _add_parameters(self, parameters):
        """
        Parameter Data
        Index	Type	Name	Description
        Pointer	Surface	Underlying surface
        2	INT	N	Number of loops
        3	BOOL	Flag	Outer loop flag:
                                True indicates Loop1 is outer loop.
                                False indicates no outer loop.
        4	Pointer	Loop1	Pointer to first loop of the face
        3+N	Pointer	LoopN	Pointer to last loop of the face
        """
        self.surf_pointer = int(parameters[1])
        self.n_loops = int(parameters[2])
        self.outer_loop_flag = bool(parameters[3])

        self.loop_pointers = []
        for i in range(self.n_loops):
            self.loop_pointers.append(int(parameters[4 + i]))

    @property
    def loops(self):
        loops = []
        for ptr in self.loop_pointers:
            loops.append(self.iges.from_pointer(ptr))

        return loops

    def __repr__(self):
        info = 'IGES Type 510: Face\n'
        # info += 'Center: (%f, %f)\n' % (self.x, self.y)
        # info += 'Start:  (%f, %f)\n' % (self.x1, self.y1)
        # info += 'End:    (%f, %f)\n' % (self.x2, self.y2)
        # info += 'Z Disp: %f' % self.z
        return info


class Loop(Entity):
    """Defines a loop, specifying a bounded face, for B-Rep
    geometries."""

    def _add_parameters(self, parameters):
        """Parameter Data
        Index   Type    Name                Description
        1       INT     N                   N Edges in loop
        2	INT	Type1	            Type of Edge 1
                                            0 = Edge
                                            1 = Vertex
        3	Pointer	E1                  First vertex list or edge list
        4	INT	Index1              Index of edge/vertex in E1
        5	BOOL	Flag1               Orientation flag -
                                            True = Agrees with model curve
        6	INT	K1                  Number of parametric space curves
        7	BOOL	ISO(1, 1)           Isoparametric flag of first
                                            parameter space curve
        8	Pointer	PSC(1, 1)           First parametric space curve of E1
        .
        6+2K1	Pointer	PSC(1, K1)          Last parametric space curve of E1
        7+2K1	INT	Type2               Type of Edge 2
        """
        self.parameters = parameters
        self.n_edges = int(self.parameters[1])
        self._edges = []

        c = 0
        for i in range(self.n_edges):
            edge = {'type': int(self.parameters[2 + c]),
                    'e1': int(self.parameters[3 + c]),  # first vertex or edge list
                    'index1': int(self.parameters[4 + c]),  # index of edge in e1
                    'flag1': bool(self.parameters[5 + c]),  # orientation flag
                    'k1': int(self.parameters[6 + c])}  # n curves
            curves = []
            for j in range(edge['k1']):
                curve = {'iso': bool(self.parameters[7 + c + j*2]),  # isopara flag
                         'psc': int(self.parameters[8 + c + j*2])}  # space curve
                curves.append(curve)
            c += 5 + 2*edge['k1']

            edge['curves'] = curves
            self._edges.append(edge)

    # @property
    # def edge_lists(self):
    #     for 

    def curves(self):
        """list of curves"""
        pass

    def __repr__(self):
        info = 'IGES Type 508: Loop\n'
        return info


class EdgeList(Entity):
    """Provides a list of edges, comprised of vertices, for specifying
    B-Rep Geometries."""
    _iges_type = 504

    def _add_parameters(self, parameters):
        """
        Parameter Data
        Index in list	Type of data	Name	Description
        INT	N	Number of Edges in list
        2	Pointer	Curve1	First model space curve
        3	Pointer	SVL1	Vertex list for start vertex
        4	INT	S1	Index of start vertex in SVL1
        5	Pointer	EVL1	Vertex list for end vertex
        6	INT	E1	Index of end vertex in EVL1
        .
        .	.
        .	.
        .	
        5N-3	Pointer	CurveN	First model space curve
        5N-2	Pointer	SVLN	Vertex list for start vertex
        5N-1	INT	SN	Index of start vertex in SVLN
        5N	Pointer	EVLN	Vertex list for end vertex
        5N+1	INT	EN	Index of end vertex in EVLN
        """
        self.parameters = parameters
        self.n_edges = int(parameters[1])

        self.edges = []
        for i in range(self.n_edges):
            edge = {'curve1': int(parameters[2 + 5*i]),  # first model space curve
                    'svl': int(parameters[3 + 5*i]),  # vertex list for start vertex
                    's': int(parameters[4 + 5*i]),  # start index
                    'evl': int(parameters[5 + 5*i]), # vertex list for end vertex
                    'e': int(parameters[6 + 5*i])} # index of end vertex in evl n
            self.edges.append(edge)

    # @property
    # def curve(self, ):
    #     for

    def __getitem__(self, indices):
        # TODO: limit spline based on start and end point
        ptr = self.edges[indices]['curve1']
        return self.iges.from_pointer(ptr)

    def __len__(self):
        return len(self.edges)

    def __repr__(self):
        info = 'IGES Type %d: Edge List\n' % self._iges_type
        return info


class VertexList(Entity):
    """Vertex List (Type 502 Form 1)"""
    _iges_type = 502

    def _add_parameters(self, parameters):
        """Parameter Data
        Index in list	Type of data	Name	Description
        INT	N	Number of vertices in list
        2	REAL	X1	Coordinates of first vertex
        3	REAL	Y1
        4	REAL	Z1
        .
        .	.
        .	.
        .
        3N-1	REAL	XN	Coordinates of last vertex
        3N	REAL	YN
        3N+1	REAL	ZN
        """
        self.parameters = parameters
        self.n_points = int(parameters[1])
        self.points = []
        for i in range(self.n_points):
            point = [float(self.parameters[2 + i*3]),
                     float(self.parameters[3 + i*3]),
                     float(self.parameters[4 + i*3])]
            self.points.append(point)
