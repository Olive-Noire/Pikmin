from simulator.action import *
from simulator.camera import *

from geometry.shape import *

from physics.collisions import *

from pygame import draw

from simulator.trajectory import *

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
        
        self._state = state
        self._editing = False
        self._editing_id = None

        self._trajectories = dict()
        self._trajectories[1] = Trajectory(100)

        self._follow = 0
    
    def move_camera(self, x, y):
        translation = Vector(-x, y)
        self._camera.position += translation

        for key in self._entities:
            self._entities[key].body.translate(-1*translation)
        
        for key in self._trajectories:
            self._trajectories[key].translate(-1*translation)
    
    def zoom(self, relative: int):
        self._camera.zoom += relative
        if self._camera.zoom < 0:
            self._camera.zoom = 0
        
        for key in self._entities:
            self._entities[key].body.set_radius(self._entities[key].body.get_radius()*self._camera.zoom)

            center = self._entities[key].body.get_center()
            self._entities[key].body.set_center(Vector((center[0]-600)*self._camera.zoom+600, (center[1]-350)*self._camera.zoom+350))
        
        for key in self._trajectories:            
            self._trajectories[key].zoom(self._camera.zoom)

    def get_camera(self):
        return self._camera

    def set_editing(self, mode, identifiant):
        self._editing = mode
        self._editing_id = identifiant

    def on_editing(self):
        return self._editing, self._editing_id

    def update(self):
        if not(self._state):
            return
        
        if len(self._entities) > self._follow:
            pass

        for key in self._trajectories:
            if key in self._entities and self._trajectories[key].update_clock():
                self._trajectories[key].append(self._entities[key].body.get_center())
            
        couples, shapes = sweep_and_prune(self._entities)
        for c in couples:
            if intersection(self._entities[c[0]].body, self._entities[c[1]].body):
                if type(self._entities[c[0]]) == type(self._entities[c[1]]) == Circle:
                    deplacement = static_resolution(self._entities[c[0]].body, self._entities[c[0]].get_mass(), self._entities[c[1]].body, self._entities[c[1]].get_mass())
                    self._entities[c[0]].body.set_center(self._entities[c[0]].body.get_center()+deplacement[0])
                    self._entities[c[1]].body.set_center(self._entities[c[1]].body.get_center()+deplacement[1])

                speeds = dynamic_resolution(self._entities[c[0]], self._entities[c[1]])

                if type(self._entities[c[0]]) == type(self._entities[c[1]]) == Circle:
                    self._entities[c[0]].set_velocity(speeds[0])
                    self._entities[c[1]].set_velocity(speeds[1])
                else:
                    self._entities[c[0]].set_velocity(speeds[0][0])
                    self._entities[c[1]].set_velocity(speeds[1][0])

                    self._entities[c[0]].add_angular_velocity(speeds[0][1])
                    self._entities[c[1]].add_angular_velocity(speeds[1][1])

        for key in self._entities:
            self._entities[key].update(1/self._update_per_second)

        for key in self._entities:
            #self._entities[key].apply_force(-0.001*self._entities[key].body.get_radius()*self._entities[key].get_velocity())
            for other in self._entities:
                if key != other:
                    gravity = 6.6743e-11*self._entities[key].get_mass()*self._entities[other].get_mass()/squared_distance(self._entities[key].body.get_center(), self._entities[other].body.get_center())
                    dir = normalize(self._entities[key].body.get_center()-self._entities[other].body.get_center())
                    self._entities[key].apply_force(-gravity*dir)
    
    def display_on(self, surface):
        surface.fill((0, 0, 0))

        vect_to_tuple = lambda v: (v[0], -v[1])
        for e in self._entities.values():
            if type(e.body) == Circle:
                draw.circle(surface, (255, 255, 255), vect_to_tuple(e.body.get_center()), e.body.get_radius(), 0)
                draw.line(surface, (255, 0, 0), vect_to_tuple(e.body.get_center()), vect_to_tuple(e.body.get_center()+e.get_velocity()), 2)
            elif type(e.body) == Polygon:
                draw.polygon(surface, (255, 0, 0), [vect_to_tuple(p) for p in e.body.get_vertices()])

            for f in e.get_forces():
                draw.line(surface, (0, 0, 255), vect_to_tuple(e.body.get_center()), vect_to_tuple(e.body.get_center()+f), 2)

        for key in self._trajectories:
            if key in self._entities:
                self._trajectories[key].draw(surface, self._camera)

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
