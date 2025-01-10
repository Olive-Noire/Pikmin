class Point:
    def __init__(self, x = 0., y = 0.):
        self.x = float(x)
        self.y = float(y)

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_coordinates(self):
        return (self.x, self.y)
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y
    
    def set_coordinates(self, x, y):
        self.x, self.y = x, y
    
    def __repr__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

class Vector:
    def __init__(self, x = 0, y = 0):
        self.components = Point(x, y)

    def get_x(self):
        return self.components.get_x()
    
    def get_y(self):
        return self.components.get_y()
    
    def get_components(self):
        return self.components.get_coordinates()
    
    def set_x(self, x):
        self.components.set_x(x)
    
    def set_y(self, y):
        self.components.set_y(y)
    
    def set_components(self, x, y):
        self.components.set_coordinates(x, y)
    
    def __add__(self, other):
        return Vector(self.components.x+other.components.x, self.components.y+other.components.y)
    
    def __sub__(self, other):
        return self+(other*(-1))
    
    def __mul__(self, scalar: float):
        return Vector(self.components.x*scalar, self.components.x*scalar)
    
    def __rmul__(self, scalar: float):
        return Vector(self.components.x*scalar, self.components.x*scalar)
    
    def __div__(self, scalar: float):
        return Vector(self.components.x/scalar, self.components.x/scalar)

    def __repr__(self):
        return self.components.__repr__()
