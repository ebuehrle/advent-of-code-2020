def surrounding_tiles(grid, r, c):
    height = len(grid)
    width = len(grid[0])
    surrounding_coordinates = [
        (r-1, c-1), (r-1, c), (r-1, c+1),
        (r,   c-1),           (r,   c+1),
        (r+1, c-1), (r+1, c), (r+1, c+1)
    ]
    valid_coordinates = [
        (x, y) for (x, y) in surrounding_coordinates if 0 <= x < height and 0 <= y < width
    ]
    return [
        grid[x][y] for (x, y) in valid_coordinates
    ]

def simulate_step(grid):
    next_grid = grid.copy()
    for i, row in enumerate(grid):
        next_grid[i] = grid[i].copy()
        for j, tile in enumerate(row):
            adj_tiles = surrounding_tiles(grid, i, j)
            if tile == 'L' and '#' not in adj_tiles:
                next_grid[i][j] = '#'
            elif tile == '#' and adj_tiles.count('#') >= 4:
                next_grid[i][j] = 'L'
    return next_grid

def print_grid(grid):
    for row in grid:
        print(''.join(row))

if __name__ == '__main__':
    import sys
    grid = [list(l.strip()) for l in sys.stdin]

    while True:
        next_grid = simulate_step(grid)
        if next_grid == grid:
            break
        grid = next_grid

    print_grid(next_grid)
    print(sum(row.count('#') for row in grid), 'occupied seats (P1)')
