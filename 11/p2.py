def first_seat_in_dir(grid, p, d):
    x, y = p
    dx, dy = d
    height = len(grid)
    width = len(grid[0])
    while True:
        x += dx
        y += dy
        if not 0 <= x < height or not 0 <= y < width:
            break
        if grid[x][y] in ['L', '#']:
            return grid[x][y]

def simulate_step(grid):
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]
    next_grid = grid.copy()
    for i, row in enumerate(grid):
        next_grid[i] = grid[i].copy()
        for j, tile in enumerate(row):
            adj_tiles = [first_seat_in_dir(grid, (i, j), d) for d in directions]
            if tile == 'L' and '#' not in adj_tiles:
                next_grid[i][j] = '#'
            elif tile == '#' and adj_tiles.count('#') >= 5:
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
    print(sum(row.count('#') for row in grid), 'occupied seats (P2)')
