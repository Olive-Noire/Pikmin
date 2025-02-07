from simulator.action import *
from simulator.camera import *

class Simulation:
    count = 0

    def __init__(self, update_per_second: float, display_per_second = None, state = False):
        Simulation.count += 1

        self._identifiant = Simulation.count

        self._actions_stack = []
        self._canceled_actions_stack = []
        
        self._entities = Pygame.Sprite.Group()
        
        self._update_per_second = self._display_per_second = update_per_second
        
        if not(display_per_second is None):
            self._display_per_second = display_per_second
        
        self._camera = Camera(Vector(0, 0), 1)
        
        self._state = False
        self._surface = caca

    def update(self):
        for e in self._entities.values():
            e.update(1/self._update_per_second)
    
    def display_on(self, surface):
        for e in self._entities.values():
            e.display_on(surface, self._camera)
    
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
