class Line:
    def __init__(self,p1,p2):
        self.a=p1[1]-p2[1]
        self.b=-(p1[0]-p2[0])
        self.c=p1[1]*p2[0]-p1[0]*p2[1]
    def get(self):
        return self.a,self.b,self.c

def intersection(l:Line,c1:Circle):
    ce,r=c1.get()
    a,b,c=l.get()
    great_a=1+a**2/b**2
    great_b=-2*ce[0]+2*(a/b)*(c/b+ce[1])
    great_c=ce[0]**2+(c/b+ce[1])**2-r**2

    delta=great_b**2-4*great_a*great_c

    return True if delta>=0 else False
