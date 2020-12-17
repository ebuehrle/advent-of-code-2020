def parse_input(src):
    actives = set()
    z, w = 0, 0
    for x, xline in enumerate(src):
        for y, state in enumerate(xline):
            if state == '#':
                actives.add((x, y, z, w))
    return actives

def simulate(steps, actives):
    for s in range(steps):
        actives = step(actives)
    return actives

def neighbors(cube):
    x, y, z, w = cube
    neighbors = set()
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dw in (-1, 0, 1):
                    if dx or dy or dz or dw:
                        neighbors.add((x+dx, y+dy, z+dz, w+dw))
    return neighbors

def step(actives):
    potential_flips = actives.union(*[neighbors(c) for c in actives])
    next_actives = set()
    for cube in potential_flips:
        surrounding_actives = neighbors(cube).intersection(actives)
        if cube in actives and (2 <= len(surrounding_actives) <= 3):
            next_actives.add(cube)
        elif cube not in actives and len(surrounding_actives) == 3:
            next_actives.add(cube)
    return next_actives

if __name__ == '__main__':
    import sys
    actives = parse_input(sys.stdin)
    end_actives = simulate(6, actives)
    print(len(end_actives))
