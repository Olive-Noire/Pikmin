from geometry.vector import Vector
from geometry.shape import Circle, Polygon


def framing(fig):
    if type(fig)==Circle:
        c=fig.get_center()
        r=fig.get_radius()
        return ((c-Vector(r,0),c+Vector(r,0)),(c-Vector(0,r),c+Vector(0,r)))
    if type(fig)==Polygon:
        l1=[i[0] for i in fig.get_vertices()]
        max_x=max(l1)
        min_x=min(l1)
        l1=[i[1] for i in fig.get_vertices()]
        max_y=max(l1)
        min_y=min(l1)
        return ((min_x,max_x),(min_y,max_y))


def sweep_and_prune_onedim_insertion(figs):
    frames_bank=[(framing(i),i) for i in figs]
    t=len(figs)
    coll_to_check=[]
    # On va trier par insertion car ce tri est optimal quand la liste est déjà quasi triée de base
    for i in range(t):
        for j in range(i-1,0,-1):
            if frames_bank[j][0][0][0]<frames_bank[j+1][0][0][0]:
                break
            frames_bank[j],frames_bank[j+1]=frames_bank[j+1],frames_bank[j]

    for i in range(t):
        for j in range(i+1,t):
            if frames_bank[i][0][0][1]<frames_bank[j][0][0][0]:
                break
            if max(frames_bank[i][0][1][0],frames_bank[j][0][1][0])<min(frames_bank[i][0][1][1],frames_bank[j][0][1][1]):
                coll_to_check.append([frames_bank[i][1],frames_bank[j][1]])
    liste_triee=[i[1] for i in frames_bank]
    return coll_to_check,liste_triee
        

