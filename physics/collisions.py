from geometry.shape import Circle, Polygon
from geometry.utils import distance
from geometry.vector import *
from geometry.utils import *
from math import pi

def framing(fig):
    if type(fig) == Circle:
        c = fig.get_center()
        r = fig.get_radius()

        return [(c[0]-r, c[0]+r), (c[1]-r, c[1]+r)]
    elif type(fig) == Polygon:
        min_x = min_y = float("inf")
        max_x = max_y = -float("inf")

        for i in range(len(fig.get_vertices())):
            vertex = fig[i]

            min_x = min(min_x, vertex[0])
            min_y = min(min_y, vertex[1])
            max_x = max(max_x, vertex[0])
            max_y = max(max_y, vertex[1])

        return [(min_x, max_x), (min_y, max_y)]

def sweep_and_prune(shapes): # one dimensional with insertion sort
    frames_bank = [(framing(i), i) for i in shapes]
    t = len(shapes)
    coll_to_check = []

    # On va trier par insertion car ce tri est optimal quand la liste est déjà quasi triée de base
    for i in range(t):
        for j in range(i-1, 0, -1):
            if frames_bank[j][0][0][0] < frames_bank[j+1][0][0][0]:
                break
            frames_bank[j], frames_bank[j+1] = frames_bank[j+1], frames_bank[j]

    for i in range(t):
        for j in range(i+1, t):
            if frames_bank[i][0][0][1] < frames_bank[j][0][0][0]:
                break
            if max(frames_bank[i][0][1][0], frames_bank[j][0][1][0]) < min(frames_bank[i][0][1][1], frames_bank[j][0][1][1]):
                coll_to_check.append([frames_bank[i][1], frames_bank[j][1]])

    liste_triee = [i[1] for i in frames_bank]
    return coll_to_check, liste_triee

def static_resolution(obj1,obj2):
    first,second=obj1.get_position(),obj2.get_position()
    if type(first)==type(second)==Circle:
        c1,c2,r1,r2=first.get_center(),second.get_center(),first.get_radius(),second.get_radius()
        dist=(c1-c2)*(((r1+r2)/distance(c1,c2)-1))
        first.set_center(c1+dist*(1/2))
        second.set_center(c1+(-1)*dist*(1/2))
        return (first,second)

def dynamic_resolution(obj1,obj2):
    first,second=obj1.get_position(),obj2.get_position()
    v1,v2=obj1.get_velocity,obj2.get_velocity()
    mass1,mass2=obj1.get_mass(),obj2.get_mass()
    if type(first)==type(second)==Circle:
        c1,c2,r1,r2=first.get_center(),second.get_center(),first.get_radius(),second.get_radius()
        dist=distance(c1,c2)
        normal=(c2-c1)*(1/dist)
        x,y=normal.get_components()
        tangeantal=Vector(-y,x)
        dpt1=dot_product(v1,tangeantal)
        dpt2=dot_product(v2,tangeantal)
        dpn1=dot_product(v1,normal)
        dpn2=dot_product(v2,normal)
        second.set_center(c1+(-1)*dist*(1/2))
        tx,ty=tangeantal.get_components()

        #conservation of momentum
        m1=(dpn1*(mass1-mass2)+2*mass2*dpn2)/(mass2+mass1)
        m2=(dpn2*(mass2-mass1)+2*mass1*dpn1)/(mass2+mass1)
        obj1.apply_force(v1*dpt1+normal*m1)
        obj2.apply_force(v2*dpt2+normal*m2)
