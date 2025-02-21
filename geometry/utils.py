from vector import *

from math import sqrt

def squared_norm(v: Vector):
    return v[0]**2+v[1]**2

def squared_distance(a: Vector, b: Vector):
    return squared_norm(a-b)

def norm(v: Vector):
    return sqrt(squared_norm(v))

def distance(a: Vector, b: Vector):
    return sqrt(squared_distance(a, b))

def barycenter(points: list):
    return sum(points, start = Vector(0, 0))/len(points) # mean of components

def has_duplicates(l: list):
    already_seen = set()
    for x in l:
        if x in already_seen:
            return True

        already_seen.add(x)

    return False
