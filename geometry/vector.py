class Point:
    def __init__(self, x = 0., y = 0.):
        self.x = float(x)
        self.y = float(y)

    def get_coordinates(self):
        return (self.x, self.y)
    
    def set_cordinates(self, x, y):
        self.x, self.y = x, y
    
    def __getitem__(self, index):
        assert(index == 0 or index == 1)

        if index == 0:
            return self.x
        elif index == 1:
            return self.y
    
    def __setitem__(self, index, value):
        assert(index == 0 or index == 1)

        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value

    def __repr__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

class Vector:
    def __init__(self, x = 0, y = 0):
        self.components = Point(x, y)
    
    def get_components(self):
        return self.components.get_coordinates()
    
    def set_components(self, x, y):
        self.components.set_coordinates(x, y)
    
    def __getitem__(self, index):
        return self.components[index]
    
    def __setitem__(self, index, value):
        self.components[index] = value
    
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
