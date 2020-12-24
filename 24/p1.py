def steps2coords(steps):
    steps = steps.strip()
    x1, x2 = 0, 0
    while steps:
        if steps.startswith('nw'):
            x1 -= 1
            steps = steps[2:]
        elif steps.startswith('ne'):
            x1 -= 1
            x2 += 1
            steps = steps[2:]
        elif steps.startswith('e'):
            x2 += 1
            steps = steps[1:]
        elif steps.startswith('sw'):
            x1 += 1
            x2 -= 1
            steps = steps[2:]
        elif steps.startswith('se'):
            x1 += 1
            steps = steps[2:]
        elif steps.startswith('w'):
            x2 -= 1
            steps = steps[1:]
        else:
            raise ValueError(f'Unknown character {steps[0]}')
    return (x1, x2)

def neighbours(coords):
    x1, x2 = coords
    nbs = {
        (x1-1, x2), (x1-1, x2+1),
        (x1, x2-1), (x1, x2+1),
        (x1+1, x2-1), (x1+1, x2),
    }
    return nbs

def step(black_tiles):
    potential_flips = black_tiles.union(*(neighbours(t) for t in black_tiles))
    next_black_tiles = set()

    for t in potential_flips:
        adjacent_black_tiles = neighbours(t).intersection(black_tiles)
        if t in black_tiles and not (not adjacent_black_tiles or len(adjacent_black_tiles) > 2):
            next_black_tiles.add(t) # stays black
        elif t not in black_tiles and (len(adjacent_black_tiles) == 2):
            next_black_tiles.add(t) # flips to black
    
    return next_black_tiles

if __name__ == '__main__':
    import sys

    black_tiles = set()
    for steps in open(sys.argv[1]):
        coords = steps2coords(steps)
        if coords not in black_tiles:
            black_tiles.add(coords)
        else:
            black_tiles.remove(coords)

    print('P1:', len(black_tiles))

    res = black_tiles
    for days in range(100):
        res = step(res)
    
    print('P2:', len(res))
        