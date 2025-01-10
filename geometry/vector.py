class Point:
    def __init__(self, x = 0., y = 0.):
        self._x = float(x)
        self._y = float(y)

    def get_coordinates(self):
        return (self._x, self._y)
    
    def set_cordinates(self, x: float, y: float):
        self._x, self._y = x, y
    
    def __getitem__(self, index: int):
        assert(index == 0 or index == 1)

        if index == 0:
            return self._x
        elif index == 1:
            return self._y
    
    def __setitem__(self, index: int, value: float):
        assert(index == 0 or index == 1)

        if index == 0:
            self._x = value
        elif index == 1:
            self._y = value
    
    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __repr__(self):
        return "("+str(self._x)+", "+str(self._y)+")"

class Vector:
    def __init__(self, x = 0, y = 0):
        self._components = Point(x, y)
    
    def get_components(self):
        return self._components.get_coordinates()
    
    def set_components(self, x: float, y: float):
        self._components.set_coordinates(x, y)
    
    def __getitem__(self, index: int):
        return self._components[index]
    
    def __setitem__(self, index: int, value: float):
        self._components[index] = value
    
    def __add__(self, other):
        return Vector(self._components.x+other._components.x, self._components.y+other._components.y)
    
    def __sub__(self, other):
        return self+(other*(-1))
    
    def __mul__(self, scalar: float):
        return Vector(self._components.x*scalar, self._components.x*scalar)
    
    def __rmul__(self, scalar: float):
        return self*scalar
    
    def __div__(self, scalar: float):
        return Vector(self._components.x/scalar, self._components.x/scalar)
    
    def __eq__(self, other):
        return self._components == other._components

    def __repr__(self):
        return self._components.__repr__()

def create_vector(A: Point, B: Point = None):
    if B is None:
        return Vector(A[0], A[1])
    else:
        assert(type(B) == Point)
        return Vector(B[0]-A[0], B[1]-A[1])
