class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x,y)
    
    def __sub__(self, other):
        return self+(other*(-1))
    
    def __mul__(self, scalar):
        x = self.x * scalar
        y = self.y * scalar
        return Vector(x,y)

    def __repr__(self):
        return "("+str(self.x)+", "+str(self.y)+")"
