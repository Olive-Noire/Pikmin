class Point:
    def __init__(self, x = 0., y = 0.):
        self.x = float(x)
        self.y = float(y)
    
    def __init__(self, v):
        self.x = v.components.x
        self.y = v.components.y
    
    def __repr__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

class Vector:
    def __init__(self, x = 0, y = 0):
        self.components = Point(x, y)
    
    def __init__(self, p: Point):
        self.components = p
    
    def __add__(self, other):
        return Vector(self.components.x+other.components.x, self.components.y+other.components.y)
    
    def __sub__(self, other):
        return self+(other*(-1))
    
    def __mul__(self, scalar: float):
        return Vector(self.components.x*scalar, self.components.x*scalar)
    
    def __div__(self, scalar: float):
        return Vector(self.components.x/scalar, self.components.x/scalar)

    def __repr__(self):
        return self.components.__repr__()