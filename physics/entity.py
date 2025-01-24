from geometry.vector import Vector
from geometry.shape import *

class Entity:
    def __init__(self, position: Vector, velocity: Vector, collision_box: Shape, mass: float):
        self.position = position
        self.velocity = velocity
        self.collision_box = collision_box
        self.mass = mass
        self.forces = []
    
    def apply_force(self, vect):
        self.forces.append(vect)

    def update(self, dt):
        acceleration = sum(self.forces, start = Vector(0, 0))*(1/self.mass)
        self.velocity += dt*acceleration
        self.position += dt*self.velocity
    
    def render(self):
        if type(self.collision_box) == Circle:
            pass
            # afficher un cercle
