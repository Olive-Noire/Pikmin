from geometry.utils import *

def get_line_coefficients(u: Vector, v: Vector):
    return u[1]-v[1], v[0]-u[0], determinant(u, v)

class Line:
    def __init__(self, direction: Vector, start_point: Vector):
        assert(direction[0] != 0 or direction[1] != 0)

        self._direction = direction
        self._start_point = start_point

    def get_coefficients(self):
        return get_line_coefficients(self._start_point, self._start_point+self._direction)
    
    def get_endpoints(self):
        return self._start_point, self._start_point+self._direction
    
    def __contains__(self, point: Vector):
        assert(type(point) == Vector)

        a, b, c = self.get_coefficients()
        return abs(a*point[0]+b*point[1]+c) <= 1e-7

    def __and__(self, other):
        assert(type(other) == Segment or type(other) == Ray or type(other) == Line)

        A, B = self.get_endpoints()
        C, D = other.get_endpoints()
        AB = B-A
        CD = D-C

        det = determinant(AB, CD)
        if abs(det) == 0:
            return []
        
        I = C+(determinant(C-A, AB)/det)*CD
        if I in other:
            return [I]
        else:
            return []
        
class Ray:
    def __init__(self, startpoint: Vector, endpoint: Vector):
        assert(startpoint != endpoint)

        self._startpoint = startpoint
        self._endpoint = endpoint

    def get_endpoints(self):
        return [self._startpoint, self._endpoint]

    def __contains__(self, point: Vector):
        assert(type(point) == Vector)

        a, b, c = get_line_coefficients(self._startpoint, self._endpoint)

        # must verify cartesian equation
        if abs(a*point[0]+b*point[1]+c) <= 1e-7:
            return dot_product(point-self._startpoint, self._endpoint-self._startpoint) >= 0

        return False

    def __and__(self, s):
        return s&self
    
class Segment:
    def __init__(self, endpoint1: Vector, endpoint2: Vector):
        assert(endpoint1 != endpoint2)
        self._endpoints = [endpoint1, endpoint2]

    def get_endpoints(self):
        return self._endpoints
    
    def get_middle(self):
        return barycenter(self._endpoints)
    
    def __contains__(self, point: Vector):
        assert(type(point) == Vector)

        a, b, c = get_line_coefficients(*self._endpoints)

        # must verify cartesian equation
        if abs(a*point[0]+b*point[1]+c) <= 1e-7:
            line_direction = self._endpoints[1]-self._endpoints[0]
            vect = point-self._endpoints[0]

            return dot_product(vect, line_direction) >= 0 and squared_norm(vect) <= squared_norm(line_direction)

        return False

    def __and__(self, other):
        assert(type(other) == Line or type(other) == Ray)

        if type(other) == Line:
            return other&self

        A, B, C, D = *self._endpoints, *other.get_endpoints()
        AB = B-A
        CD = D-C

        line_AB = Line(AB, A)
        line_CD = Line(CD, C)

        if line_AB&other == [] or line_CD&self == []:
                return []
        
        return line_AB&line_CD
