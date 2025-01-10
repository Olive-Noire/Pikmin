class Line:
    def __init__(self, p1, p2):
        assert(p1 != p2)
        
        self.a = p1[1]-p2[1]
        self.b = p2[0]-p1[0]
        self.c = p1[0]*p2[1]-p1[1]*p2[0]

    def get_coefficients(self):
        return self.a, self.b, self.c
