from geometry.vector import Vector
from geometry.shape import *

class Entity:
    def __init__(self, velocity: Vector, collision_box: Shape, mass: float):
        self._velocity = velocity # m.s^-1
        self._collision_box = collision_box

        self.angular_velocity = 0
        self.angle = 0

        self._mass = mass # Kg
        self._forces = [] # N
    
    def apply_force(self, vect):
        self._forces.append(vect)
    
    def get_forces(self):
        return self._forces

    def update(self, dt):
        acceleration = sum(self._forces, start = Vector(0, 0))*(1/self._mass) # m.s^-2
        self._velocity += dt*acceleration
        self._collision_box.set_center(self._collision_box.get_center()+dt*self._velocity)

        if type(self.body) == Polygon:
            self.body.rotate(self.angular_velocity*dt)

        self._forces.clear()
    
    def add_angular_velocity(self, ac):
        self.angular_velocity += ac
    
    def get_velocity(self):
        return self._velocity
    
    def set_velocity(self, velocity):
        self._velocity = velocity
    
    def get_position(self):
        return self.collision_box.get_center()
    
    def get_mass(self):
        return self._mass

    @property
    def body(self):
        return self._collision_box
