from math import cos, sin

from geometry.vector import *

def rotate(v: Vector, angle: float, center = Vector(0, 0)):
    v -= center
    v = Vector(v[0]*cos(angle)-v[1]*sin(angle), v[0]*sin(angle)+v[1]*cos(angle))
    return v+center
