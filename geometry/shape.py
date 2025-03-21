from math import sqrt, pi

from geometry.line import Segment, Ray, Line, get_line_coefficients
from geometry.utils import squared_distance, barycenter, has_duplicates, solve_quadratic_equation, normalize, determinant
from geometry.transformations import rotate
from geometry.vector import Vector

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
    
    def set_center(self, center: Vector):
        self._center = center
    
    def set_radius(self, radius: float):
        assert(radius > 0)
        self._radius = radius

    def __contains__(self, point: Vector):
        return squared_distance(self._center, point) <= self._radius**2
    
    def __and__(self, other):
        if type(other) == Segment or type(other) == Line or type(other) == Ray:
            a, b, c = get_line_coefficients(*other.get_endpoints())
            if b == 0: # segment vertical
                ordinates = solve_quadratic_equation(1, -2*self._center[1], self._center[1]**2-self._radius**2+(c/a-self._center[0])**2)
                return {point for point in [Vector(-c/a, y) for y in ordinates] if point in other}
            else:
                abscissa = solve_quadratic_equation(1+(a/b)**2, -2*self._center[0]+2*(a/b)*(c/b+self._center[1]), self._center[0]**2+(c/b+self._center[1])**2-self._radius**2)
                return {point for point in [Vector(x, -(a*x+c)/b) for x in abscissa] if point in other}
            
        elif type(other) == Circle:
            if squared_distance(self._center, other._center) > (self._radius+other._radius)**2:
                return set()
            
            squared_D = squared_distance(self._center, other._center)
            squared_radius = [self._radius**2, other._radius**2]
            squared_height = (squared_radius[0]*squared_radius[1]-(squared_D-squared_radius[0]-squared_radius[1])**2/4)/squared_D
            direction = normalize(other._center-self._center)

            I = self._center+sqrt(squared_radius[0]-squared_height)*direction
            gap = rotate(direction, pi/2)*sqrt(squared_height)

            return {I-gap, I+gap}
        else:
            return other&self

class Polygon(Shape):
    def __init__(self, vertices: list):
        assert(len(vertices) >= 3 and not(has_duplicates(vertices)))
        self._vertices = vertices
    
    def get_center(self):
        return barycenter(self._vertices)
    
    def get_vertices(self):
        return self._vertices
    
    def __add__(self, v: Vector):
        return Polygon([self._vertices[i]+v for i in range(len(self._vertices))])
    
    def __getitem__(self, index):
        return self._vertices[index]
    
    def __setitem__(self, index, vertex):
        self._vertices[index] = vertex
    
    def __contains__(self, other):
        # A vector is similar to a point
        assert(type(other) == Vector)

        ray = Ray(other, Vector(0, 0))
        flag = False
        for i in range(len(self._vertices)):
            A, B = self._vertices[i], self._vertices[(i+1)%len(self._vertices)]
            intersection = ray&Segment(A, B)
            if intersection and not(A in intersection or B in intersection):
                flag = not(flag)
        
        return flag
    
    def __and__(self, other):
        intersection = set()
        for i in range(len(self._vertices)):
            intersection |= other&Segment(self._vertices[i], self._vertices[(i+1)%len(self._vertices)])

        return intersection

def intersection(a: Shape, b: Shape):
    if type(a) == type(b) == Circle:
        return squared_distance(a.get_center(), b.get_center()) <= (a.get_radius()+b.get_radius())**2
