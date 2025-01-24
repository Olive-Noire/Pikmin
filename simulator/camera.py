from geometry.shape import Vector

class Camera:
    def __init__(self, position: Vector, zoom: int):
        assert(zoom >= 1)
        
        self.position = position
        self.zoom = zoom