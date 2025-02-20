class Vector:
    def __init__(self, x = 0, y = 0):
        self._x = x
        self._y = y
    
    def get_components(self):
        return (self._x, self._y)
    
    def set_components(self, x: float, y: float):
        self._x = x
        self._y = y
    
    def __getitem__(self, index: int):
        assert(index == 0 or index == 1)

        if index == 0:
            return self._x
        else:
            return self._y
    
    def __setitem__(self, index: int, value: float):
        assert(index == 0 or index == 1)

        if index == 0:
            self._x = value
        else:
            self._y = value
    
    def __add__(self, other):
        return Vector(self._x+other._x, self._y+other._y)
    
    def __sub__(self, other):
        return self+(other*(-1))
    
    def __mul__(self, scalar: float):
        return Vector(self._x*scalar, self._y*scalar)
    
    def __rmul__(self, scalar: float):
        return self*scalar
    
    def __truediv__(self, scalar: float):
        return Vector(self._x/scalar, self._y/scalar)
    
    def __rtruediv__(self, scalar: float):
        return Vector(self._x/scalar, self._y/scalar)
    
    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __repr__(self):
        return "("+str(self._x)+", "+str(self._y)+")"
    
    def __hash__(self):
        return (self._x, self._y).__hash__()

# Area of the parallelogram
def determinant(a: Vector, b: Vector):
    return a[0]*b[1]-a[1]*b[0]

