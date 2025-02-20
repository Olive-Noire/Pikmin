from utils import *
from vector import *

class Line:
    def __init__(self,vect,start_point):
        assert(vect[0]!=0 or vect[1]!=0)
        self.vect=vect
        self.start_point=start_point
        self.a=vect[1]
        self.b=vect[0]
        self.c=-self.a*start_point[0]-self.b*start_point[1]

    def get_coeffs(self):
        return (self.a,self.b,self.c)
    
    def get_points(self):
        return self.start_point,Vector(self.start_point[0]+self.vect[0], self.start_point[1]+self.vect[1])

    def __and__(self, other):
        if type(other)==Line:
            A,B=self.get_points()
            C,D=other.get_points()
            AB=B-A
            AC=C-A
            CD=D-C

            denom=determinant(AB,CD)
            if denom==0:
                return []
            num=determinant(AC,CD)

            t=num/denom

            return [A[0]+t*AB[0],A[1]+t*AB[1]]
        elif type(other)==Segment:
            A,B=self.get_points()
            C,D=other.get_endpoints()
            AB=B-A
            AC=C-A
            CD=D-C

            denom=determinant(AB,CD)
            if denom==0:
                return []
            num=determinant(AC,AB)

            t=num/denom

            if not(0<t<=1):
                return []
            return [C[0]+t*CD[0],C[1]+t*CD[1]]
        
        elif type(other)==Ray:
            A,B=self.get_points()
            C,D=other.get_points()
            AB=B-A
            AC=C-A
            CD=D-C

            denom=determinant(AB,CD)
            if denom==0:
                return []
            num=determinant(AC,AB)
            t=num/denom
            if not(0<num):
                return []
            return [C[0]+t*CD[0],C[1]+t*CD[1]]


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
            A, B, C, D = *self._endpoints, *other._endpoints
            AB=B-A
            CD=D-C
            l_AB=Line(AB,A)
            l_CD=Line(CD,C)

            if l_AB&other==[] or l_CD&self==[]:
                return []
            return l_AB&l_CD

        if type(other) == Ray:
            A, B, C, D = *self._endpoints, *other.get_points()
            AB=B-A
            CD=D-C
            l_AB=Line(AB,A)
            l_CD=Line(CD,C)

            if l_AB&other==[] or l_CD&self==[]:
                return [l_CD.get_points(),self.get_endpoints(),l_CD&self]
            return l_AB&l_CD

a=Vector(1,1)

b=Vector(0,4)

c=Line(a,b)

d=Vector(-2,0)

e=Vector(0,-2)

f=Ray(e,d)

print(c&f)