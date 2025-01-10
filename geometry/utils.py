from geometry.vector import *
from math import sqrt

def squared_norm(v: Vector):
    return v[0]**2+v[1]**2

def squared_distance(A: Point, B: Point):
    return squared_norm(create_vector(A, B))

def norm(v: Vector):
    return sqrt(squared_norm(v))

def distance(a: Point, b: Point):
    return sqrt(squared_distance(a, b))

def barycenter(points: list):
    vectors = [create_vector(p) for p in points] # convert points to vectors
    vectors_mean = sum(vectors, start = Vector(0, 0))/len(points) # mean of components
    return Point(*vectors_mean.get_components())
