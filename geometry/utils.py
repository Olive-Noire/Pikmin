from geometry.vector import *

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
    return sum(points, start = Vector(0, 0))*(1/len(points)) # mean of components

def has_duplicates(l: list):
    already_seen = set()
    for x in l:
        if x in already_seen:
            return True

        already_seen.add(x)

    return False

# Area of the parallelogram
def determinant(a: Vector, b: Vector):
    return a[0]*b[1]-a[1]*b[0]

def dot_product(a: Vector, b: Vector):
    return a[0]*b[0]+a[1]*b[1]

def normalize(v: Vector):
    return v/norm(v)

def solve_quadratic_equation(a, b, c):
    discriminant = b**2-4*a*c
    if discriminant < 0:
        return set()
    else:
        discriminant = sqrt(discriminant)
        return {(-b-discriminant)/(2*a), (-b+discriminant)/(2*a)}
