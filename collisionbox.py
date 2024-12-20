from vector import Vector
from utils import squared_distance

class CollisionBox:
    def __init__(self):
        pass

class Circle(CollisionBox):
    def __init__(self, center: Vector, radius: float):
        self.center = center
        self.radius = radius

class Rectangle(CollisionBox):
    def __init__(self, top_left_corner: Vector, width: float, height: float):
        self.top_left_corner = top_left_corner
        self.width = width
        self.height = height

class Triangle(CollisionBox):
    def __init__(self, vertex1: Vector, vertex2: Vector, vertex3: Vector):
        self.vertices = [vertex1, vertex2, vertex3]

def collision(c1: Circle, c2: Circle):
    return (c1.radius+c2.radius)**2 <= squared_distance(c1.center, c2.center)
