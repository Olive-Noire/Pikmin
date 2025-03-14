from geometry.vector import Vector
from geometry.shape import *

class Entity:
    def __init__(self, velocity: Vector, collision_box: Shape, mass: float):
        self._velocity = velocity
        self._collision_box = collision_box
        self._mass = mass
        self._forces = []
    
    def apply_force(self, vect):
        self._forces.append(vect)

    def update(self, dt):
        acceleration = sum(self._forces, start = Vector(0, 0))*(1/self._mass)
        self._velocity += dt*acceleration
        self._collision_box.set_center(self._collision_box.get_center()+dt*self._velocity)

        self._forces.clear()
    
    def get_velocity(self):
        return self._velocity
    
    def get_position(self):
        return self.collision_box.get_center()
    
    def get_mass(self):
        return self._mass

    @property
    def body(self):
        return self._collision_box
