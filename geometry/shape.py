from geometry.line import *
from geometry.vector import *
from geometry.utils import squared_distance, barycenter
from math import sin,cos,tan,atan,sqrt,pi

class Shape:
    def __init__(self):
        pass

class Circle(Shape):
    def __init__(self, center: Point, radius: float):
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
        if type(other) == Line:
            a, b, c = other.get_coefficients()

            great_a = 1+(a/b)**2
            great_b = -2*self._center[0]+2*(a/b)*(c/b+self._center[1])
            great_c = self._center[0]**2+(c/b+self._center[1])**2-self._radius**2

            return great_b**2 >= 4*great_a*great_c
        elif type(other) == Circle:
            return squared_distance(self._center, other._center) <= (self._radius+other._radius)**2

class Rectangle(Shape):
    def __init__(self, point_random: Point, width: float, height: float,angle=float):
        self.angle=angle
        self.origine = point_random
        self.width = width
        self.height = height
    def get_points(self):
        point_1=Point(self.origine[0]+self.width*sin(self.angle),self.origine[1]+self.width*cos(self.angle))
        point_2=Point(point_1[0]+self.height*sin(self.angle-pi/2),point_1[1]+self.height*cos(self.angle-pi/2))
        point_3=Point(self.origine[0]+self.height*sin(self.angle-pi/2),self.origine[1]+self.height*cos(pi/2-self.angle))

        return (self.origine,point_1,point_2,point_3,self.origine[1])

class Triangle(Shape):
    def __init__(self, vertex1: Point, vertex2: Point, vertex3: Point):
        self._vertices = [vertex1, vertex2, vertex3]
    
    def get_center(self):
        return barycenter(self._vertices)
    
    def get_vertices(self):
        return self._vertices
    
    def __getitem__(self, index):
        return self._vertices[index]
    
    def __setitem__(self, index, vertex):
        self._vertices[index] = vertex
