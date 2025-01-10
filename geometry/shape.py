from geometry.vector import *
from geometry.utils import squared_distance, barycenter

class Shape:
    def __init__(self):
        pass

class Circle(Shape):
    def __init__(self, center: Point, radius: float):
        assert(radius > 0)

        self.center = center
        self.radius = radius
    
    def get_center(self):
        return self.center
    
    def get_radius(self):
        return self.radius
    
    def set_center(self, center):
        self.center = center
    
    def set_radius(self, radius):
        assert(radius > 0)
        self.radius = radius

    def __and__(self, other):
        if type(other) == Line:
            a, b, c = other.get_coefficients()

            great_a = 1+(a/b)**2
            great_b = -2*self.center[0]+2*(a/b)*(c/b+self.center[1])
            great_c = self.center[0]**2+(c/b+self.center[1])**2-self.radius**2

            return great_b**2 >= 4*great_a*great_c

class Rectangle(Shape):
    def __init__(self, top_left_corner: Point, width: float, height: float):
        self.top_left_corner = top_left_corner
        self.width = width
        self.height = height

class Triangle(Shape):
    def __init__(self, vertex1: Point, vertex2: Point, vertex3: Point):
        self.vertices = [vertex1, vertex2, vertex3]

def center(c: Circle):
    return c.center

def center(r: Rectangle):
    c = Vector(r.top_left_corner)+Vector(r.width, r.height)/2
    return Point(c)

def center(t: Triangle):
    return barycenter(t.vertices)

def collision(c1: Circle, c2: Circle):
    return (c1.radius+c2.radius)**2 <= squared_distance(c1.center, c2.center)

def collision(c1:Rectangle,c2:Rectangle):
    tlc1,width1,height1=c1.get()
    points=[tlc1,(tlc1[0]+width1,tlc1[1]),(tlc1[0],tlc1[1]-height1),(tlc1[0]+width1,tlc1[1]+height1)]
    tlc2,width2,height2=c2.get()

    for i in points:
        if tlc2[0]<=i[0]<=tlc2[0]+width2 and tlc2[1]-height1<=i[1]<=tlc2[1]:
            return False

def collision(r=Rectangle,c=Circle):
    tlc1,width1,height1=r.get()
    points=[tlc1,(tlc1[0]+width1,tlc1[1]),(tlc1[0]+width1,tlc1[1]+height1),(tlc1[0],tlc1[1]-height1),tlc1]
    for i in range(4):
        ligne=Line(points[i],points[i+1])
        if intersection(ligne,c):
            return True
    return False

def collision(c=Circle,r=Rectangle):
    return collision(r,c)
