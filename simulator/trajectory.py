from pygame import draw
from geometry.vector import Vector

class Trajectory:
    def __init__(self, max_clock):
        self._points = []
        self._clock = self._max_clock = max_clock
    
    def clear(self):
        self._points.clear()
    
    def append(self, position):
        self._points.append(position)
    
    def update_clock(self):
        self._clock -= 1
        if self._clock <= 0:
            self._clock = self._max_clock
            return True
        else:
            return False
    
    def translate(self, translation):
        for i in range(len(self._points)):
            self._points[i] += translation
    
    def zoom(self, z):
        for i in range(len(self._points)):
            self._points[i] = Vector((self._points[i][0]-600)*z+600, (self._points[i][1]-350)*z+350)
    
    def draw(self, surface, camera):
        if len(self._points) >= 2:
            vect_to_tuple = lambda v: (v[0], -v[1])

            # à optimiser parce que y a deux boucles
            draw.lines(surface, (0, 255, 0), False, [vect_to_tuple(position) for position in self._points], 2)
            for position in self._points:
                draw.polygon(surface, (255, 128, 0), [vect_to_tuple(position+Vector(-2, -2)), vect_to_tuple(position+Vector(2, -2)), vect_to_tuple(position+Vector(2, 2)), vect_to_tuple(position+Vector(-2, 2))], 0)
