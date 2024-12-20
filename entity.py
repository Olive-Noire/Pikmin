from vector import Vector
from collisionbox import CollisionBox

class Entity:
    def __init__(self, position: Vector, velocity: Vector, acceleration: Vector, collision_box: CollisionBox):
        self.position = position
        self.velocity = velocity
        self.acceleraiton = acceleration
        self.collision_box = collision_box