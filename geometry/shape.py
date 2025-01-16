from math import sin, cos, tan, atan, sqrt, pi

from geometry.utils import squared_distance, barycenter, has_duplicates
from geometry.vector import *

class Segment:
    def __init__(self, endpoint1: Vector, endpoint2: Vector):
        assert(endpoint1 != endpoint2)
        self._endpoints = [endpoint1, endpoint2]

    def get_endpoints(self):
        return self._endpoints
    
    def get_coefficients(self):
        return self._endpoints[0][1]-self._endpoints[1][1], self._endpoints[1][0]-self._endpoints[0][0], determinant(*self._endpoints)
    
    def __and__(self, other):
        if type(other) == Segment:
            A, B, C, D = *self._endpoints, *other._endpoints
            CD = D-C

            d = determinant(B-A, CD)
            return d != 0 and 0 <= determinant(C-A, CD)/d <= 1

class Shape:
    def __init__(self):
        pass

class Circle(Shape):
    def __init__(self, center: Vector, radius: float):
        assert(radius > 0)

        self._center = center
        self._radius = radius
    
    def get_center(self):
        return self._center
    
    def get_radius(self):
        return self._radius
    
    def set_center(self, center):
        self._center = center
    
    def set_radius(self, radius):
        assert(radius > 0)
        self._radius = radius
    
    def __and__(self, other):
        if type(other) == Segment:
            return other&self

            a, b, c = other.get_coefficients()

            great_a = 1+(a/b)**2
            great_b = -2*self._center[0]+2*(a/b)*(c/b+self._center[1])
            great_c = self._center[0]**2+(c/b+self._center[1])**2-self._radius**2

            return great_b**2 >= 4*great_a*great_c
        elif type(other) == Circle:
            return squared_distance(self._center, other._center) <= (self._radius+other._radius)**2

class Rectangle(Shape):
    def __init__(self, point_random: Vector, width: float, height: float, angle: float):
        self.angle = angle
        self.origin = point_random
        self.width = width
        self.height = height

    def get_points(self):
        point_1 = Vector(self.origin[0]+self.width*sin(self.angle), self.origin[1]+self.width*cos(self.angle))
        point_2 = Vector(point_1[0]+self.height*sin(self.angle-pi/2), point_1[1]+self.height*cos(self.angle-pi/2))
        point_3 = Vector(self.origin[0]+self.height*sin(self.angle-pi/2), self.origin[1]+self.height*cos(pi/2-self.angle))

        return (self.origin, point_1, point_2, point_3, self.origin[1])

class Polygon(Shape):
    def __init__(self, vertices: list):
        assert(len(vertices) >= 3 and not(has_duplicates(vertices)))
        self._vertices = vertices
    
    def get_center(self):
        return barycenter(self._vertices)
    
    def get_vertices(self):
        return self._vertices
    
    def __getitem__(self, index):
        return self._vertices[index]
    
    def __setitem__(self, index, vertex):
        self._vertices[index] = vertex
    
    def __contains__(self, other):
        # A vector is similar to a point
        assert(type(other) == Vector)

        for i in range(len(self._vertices)):
            A, B = self._vertices[i], self._vertices[(i+1)%len(self._vertices)]
            if determinant(B-A, other-A) < 0:
                return False
        
        return True
    
    def __and__(self, other):
        if type(other) == Segment:
            pass
