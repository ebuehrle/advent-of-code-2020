def count_trees(forest, x, y, slope):
    count = 0
    x = x
    for y in range(y, len(forest), slope[1]):
        x = x % len(forest[y])
        if forest[y][x] == '#':
            count += 1
        x = x + slope[0]
    return count

def count_trees_rec(forest, x, y, slope):
    if y >= len(forest):
        return 0
    x = x % len(forest[y])
    tree = forest[y][x] == '#'
    return tree + count_trees_rec(forest, x + slope[0], y + slope[1], slope)