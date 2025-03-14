from simulator.action import *
from simulator.camera import *

from geometry.shape import *

from physics.collisions import *

from pygame import draw

class Simulation:
    count = 0

    def __init__(self, update_per_second: float, display_per_second = None, state = False):
        Simulation.count += 1

        self._identifiant = Simulation.count

        self._actions_stack = []
        self._canceled_actions_stack = []
        
        self._entities = dict()
        
        self._update_per_second = self._display_per_second = update_per_second
        
        if not(display_per_second is None):
            self._display_per_second = display_per_second
        
        self._camera = Camera(Vector(0, 0), 1)
        
        self._state = False
        self._editing = False
        self._editing_id = None
    
    def moove_camera(self, x, y):
        self._camera.position[0] += x
        self._camera.position[1] += y
    
    def set_editing(self, mode, identifiant):
        self._editing = mode
        self._editing_id = identifiant

    def on_editing(self):
        return self._editing, self._editing_id

    def update(self):
        couples, shapes = sweep_and_prune([self._entities[e].body for e in self._entities])
        print(couples)
        for c in couples:
            static_resolution(*c)

        dynamic_resolution(couples)

        for key in self._entities:
            self._entities[key].apply_force(Vector(0, -60))
            self._entities[key].update(1/self._update_per_second)
    
    def display_on(self, surface):
        surface.fill((0, 0, 0))

        for e in self._entities.values():
            if type(e.body) == Circle:
                draw.circle(surface, (255, 255, 255), (e.body.get_center()[0], -e.body.get_center()[1]), e.body.get_radius(), 50)

    def __del__(self):
        Simulation.count -= 1
    
    def get_state(self):
        return self._state

    def get_entities(self):
        return self._entities
    
    def set_state(self, state: bool):
        self._state = state
    
    def set_update_per_second(self, update_per_second):
        self._update_per_second = update_per_second
    
    def set_display_per_second(self, display_per_second):
        self._display_per_second = display_per_second
    
    def add_entity(self, e):
        self._entities[len(self._entities)] = e

    def execute_action(self, action):
        action.apply(self._entities)

    def save(file_path):
        pass

def load_simulation(file_path):
    pass

"""
s = Simulation()
a = Action(0, [15, "caca"])
b = Action(0, [21, "skibidi"])

s.execute_action(a)
s.execute_action(b)
print(s.get())
s.execute_action(Action(1, [21]))
print(s.get())
"""
