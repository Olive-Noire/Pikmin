from vector import Point
from math import sqrt

def squared_norm(p: Point):
    return p.x**2+p.y**2

def squared_distance(a: Point, b: Point):
    return squared_norm(a-b)

def norm(p: Point):
    return sqrt(squared_norm(p))

def distance(a: Point, b: Point):
    return sqrt(squared_distance(a, b))
