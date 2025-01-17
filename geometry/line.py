from utils import *
class Ray:
    def __init__(self, start_point, useless_point):
        assert(start_point != useless_point)
        self.point=start_point
        self.point_2=useless_point
        self.a = start_point[1]-useless_point[1]
        self.b = useless_point[0]-start_point[0]
        self.c = start_point[0]*useless_point[1]-start_point[1]*useless_point[0]

    def get_coefficients(self):
        return self.a, self.b, self.c
    def get_points(self):
        return [self.point,self.point_2]
    def on_ray(self,p):

        if self.a*p[0]+self.b*p[1]+self.c==0:
            if (p[0]>=self.point[0] and self.b>0) or (p[0]<=self.point[0] and self.b<0) :
                return True
            if self.point[0]==0 and ((p[1]>=self.point[1] and self.a<0) or (p[1]<=self.point[1] and self.b>0)):
                return True
        return False
    
class Segment:
    def __init__(self, endpoint1: Vector, endpoint2: Vector):
        assert(endpoint1 != endpoint2)
        self._endpoints = [endpoint1, endpoint2]

    def get_endpoints(self):
        return self._endpoints
    
    def get_coefficients(self):
        return self._endpoints[0][1]-self._endpoints[1][1], self._endpoints[1][0]-self._endpoints[0][0], determinant(*self._endpoints)
    
    def __and__(self, other):
        if type(other) == Segment:
            A, B = *self._endpoints,
            CD = D-C
            AB=B-A
            d = determinant(AB, CD)
            return d != 0 and 0 <= determinant(C-A, CD)/d <= 1 and 0 <= determinant(D-B, AB)/d

        if type(other) == Ray:
            A, B, C, D = *self._endpoints, *other.get_points()
            CD = D-C

            d = determinant(B-A, CD)
            return d != 0 and 0 <= determinant(C-A, CD)/d <= 1

                
