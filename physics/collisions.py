from geometry.shape import Circle, Polygon

from geometry.vector import *
from geometry.utils import *

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

def sweep_and_prune(entities_dict): # one dimensional with insertion sort
    frames_bank = [(framing(entities_dict[key].body), key) for key in entities_dict]
    t = len(entities_dict)
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

def static_resolution(obj1, obj2):
    if type(obj1) == type(obj2) == Circle:
        c1,c2,r1,r2= obj1.get_center(), obj2.get_center(), obj1.get_radius(), obj2.get_radius()
        dist=(c1-c2)*(((r1+r2)/distance(c1,c2)-1))

        return dist*(1/2), dist*(-1/2)

def dynamic_resolution(ent1, ent2):
    first, second = ent1.body, ent2.body
    v1, v2 = ent1.get_velocity(), ent2.get_velocity()
    mass1, mass2 = ent1.get_mass(), ent2.get_mass()

    dir = normalize(first.get_center()-second.get_center())
    dir *= 2*dot_product(v1-v2, dir)/(mass1+mass2)
    
    if type(first) == type(second) == Circle:
        return v1-mass2*dir, v2+mass1*dir, 
