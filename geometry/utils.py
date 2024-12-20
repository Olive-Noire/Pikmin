from geometry.vector import *
from math import sqrt

def squared_norm(p: Point):
    return p.x**2+p.y**2

def squared_distance(a: Point, b: Point):
    return squared_norm(a-b)

def norm(p: Point):
    return sqrt(squared_norm(p))

def distance(a: Point, b: Point):
    return sqrt(squared_distance(a, b))

def barycenter(points):
    vectors = [Vector(p.x, p.y) for p in points] # convert points to vectors
    vectors_mean = sum(vectors, start = Vector(0, 0))/len(points) # mean of components
    return Point(vectors_mean.components.x, vectors_mean.components.y)