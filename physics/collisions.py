from geometry.shape import Circle, Polygon

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

def static_resolution(shapes):
    pass

def dynamic_resolution(shapes):
    pass
