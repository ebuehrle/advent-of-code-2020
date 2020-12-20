import numpy as np
import sys
import functools
import math
import operator

class Tile:
    def __init__(self, tileid, pixels):
        self.id = tileid
        self.pixels = np.array([list(row) for row in pixels])
        self.rot, self.flip = 0, None

    def oriented_pixels(self):
        if self.flip is not None:
            return np.flip(np.rot90(self.pixels, k=self.rot), self.flip)
        return np.rot90(self.pixels, k=self.rot)
    
    def top_edge(self):
        return tuple(self.oriented_pixels()[0, :])
    
    def left_edge(self):
        return tuple(self.oriented_pixels()[:, 0])
    
    def bottom_edge(self):
        return tuple(self.oriented_pixels()[-1, :])

    def right_edge(self):
        return tuple(self.oriented_pixels()[:, -1])

    def gen_orientations(self):
        bk_rot, bk_flip = self.rot, self.flip

        for flip in [None, 0, 1]:
            for rot in [0, 1, 2, 3]:
                self.flip, self.rot = flip, rot
                yield self
        
        self.rot, self.flip = bk_rot, bk_flip

    def __repr__(self):
        return f'Tile(id={self.id}, pixels={self.oriented_pixels()})'


class Assignment:
    def __init__(self, width, height, initial_tile):
        self.assignment = {(0, 0): initial_tile}
        self.width, self.height = width, height

    def iscomplete(self):
        miny, minx = min(self.assignment.keys())
        for dy in range(self.height):
            for dx in range(self.width):
                if not (miny + dy, minx + dx) in self.assignment:
                    return False
        return True
    
    def above(tilepos):
        return (tilepos[0] - 1, tilepos[1] + 0)
    
    def left(tilepos):
        return (tilepos[0] + 0, tilepos[1] - 1)
    
    def below(tilepos):
        return (tilepos[0] + 1, tilepos[1] + 0)
    
    def right(tilepos):
        return (tilepos[0] + 0, tilepos[1] + 1)
    
    def heightcomplete(self):
        miny, _ = min(self.assignment.keys(), key=lambda k: k[0])
        maxy, _ = max(self.assignment.keys(), key=lambda k: k[0])
        if maxy - miny == self.height - 1:
            return (miny, maxy)

        if maxy - miny > self.height - 1:
            raise ValueError('Assignment has tiles further apart than the max. height.')
    
    def widthcomplete(self):
        _, minx = min(self.assignment.keys(), key=lambda k: k[1])
        _, maxx = max(self.assignment.keys(), key=lambda k: k[1])
        if maxx - minx == self.width - 1:
            return (minx, maxx)

        if maxx - minx > self.width - 1:
            raise ValueError('Assignment has tiles further apart than the max. width.')

    def candidate_positions(self):
        all_neighbors = set.union(
            *[{
                Assignment.above(p), Assignment.left(p), Assignment.right(p), Assignment.below(p)
            } for p in self.assignment.keys()]
        )

        ybounds = self.heightcomplete()
        xbounds = self.widthcomplete()
        valid_neighbors = set(filter(
            lambda tpos: (not ybounds or ybounds[0] <= tpos[0] <= ybounds[1]) and (not xbounds or xbounds[0] <= tpos[1] <= xbounds[1]),
            all_neighbors
        ))

        return valid_neighbors - set(self.assignment.keys())

    def used_tiles(self):
        return set(self.assignment.values())
    
    def add(self, pos, tile):
        pright = Assignment.right(pos)
        if pright in self.assignment and self.assignment[pright].left_edge() != tile.right_edge():
            return False

        ptop = Assignment.above(pos)
        if ptop in self.assignment and self.assignment[ptop].bottom_edge() != tile.top_edge():
            return False
        
        pleft = Assignment.left(pos)
        if pleft in self.assignment and self.assignment[pleft].right_edge() != tile.left_edge():
            return False
        
        pbottom = Assignment.below(pos)
        if pbottom in self.assignment and self.assignment[pbottom].top_edge() != tile.bottom_edge():
            return False
        
        self.assignment[pos] = tile
        return True
        
    def remove(self, pos):
        self.assignment.pop(pos, None)
    
    def asmatrix(self):
        matrix = []
        miny, minx = min(self.assignment.keys())
        for dy in range(self.height):
            matrix.append([])
            for dx in range(self.width):
                matrix[dy].append(self.assignment[(miny + dy, minx + dx)])

        return matrix
    
    def __repr__(self):
        return '\n'.join([
            'Assignment(',
            f' width={self.width}',
            f' height={self.height}',
            f' assignment={self.assignment}',
            ')'
        ])


def bf(all_tiles, part_assign):
    if part_assign.iscomplete():
        return part_assign
    
    for pos in part_assign.candidate_positions():
        for tile in all_tiles - part_assign.used_tiles():
            for oriented_tile in tile.gen_orientations():
                possible = part_assign.add(pos, oriented_tile)
                if not possible:
                    continue
                if bf(all_tiles, part_assign):
                    return part_assign

        part_assign.remove(pos)
    
    return None

def parse_tiles(src):
    def redfn(acc, line):
        if not line:
            acc.append([0, []])
        elif line.startswith('Tile'):
            tileid = line[len('Tile '):-1]
            acc[-1][0] = int(tileid)
        else:
            acc[-1][1].append(line)
        return acc

    id_pixels = functools.reduce(
        redfn,
        map(str.strip, src),
        [[0, []]]
    )

    return set(map(lambda idpx: Tile(idpx[0], idpx[1]), id_pixels))

def crop_and_concat(tile_matrix):
    tile_height, tile_width = tile_matrix[0][0].oriented_pixels().shape
    cropped_tile_height, cropped_tile_width = tile_height - 2, tile_width - 2
    num_tiles_height = len(tile_matrix)
    num_tiles_width = len(tile_matrix[0])

    concatenated = np.empty((num_tiles_height * cropped_tile_height, num_tiles_width * cropped_tile_width), dtype=str)
    for y, row in enumerate(tile_matrix):
        for x, tile in enumerate(row):
            y0 = y * cropped_tile_height
            y1 = (y + 1) * cropped_tile_height
            x0 = x * cropped_tile_width
            x1 = (x + 1) * cropped_tile_width
            cropped_tile = tile.oriented_pixels()[1:-1, 1:-1]
            concatenated[y0:y1, x0:x1] = cropped_tile

    return concatenated

def gen_orientations(image):
    for rot in [0, 1, 2, 3]:
        yield np.rot90(image, k=rot)
    for rot in [0, 1, 2, 3]:
        yield np.flip(np.rot90(image, k=rot), 0)
    for rot in [0, 1, 2, 3]:
        yield np.flip(np.rot90(image, k=rot), 1)

def remove_seamonsters(image):
    seamonster_string = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    ]

    image_binary = image == '#'
    image_height, image_width = image_binary.shape

    seamonster_binary = np.array([list(r) for r in seamonster_string]) == '#'
    monster_height, monster_width = seamonster_binary.shape

    for y in range(image_height - (monster_height - 1)):
        for x in range(image_width - (monster_width - 1)):
            canvas = np.zeros_like(image_binary, dtype=bool)
            canvas[y:y+monster_height, x:x+monster_width] = seamonster_binary
            if np.alltrue((image_binary & canvas) == canvas):
                image_binary &= ~canvas

    return image_binary

def water_roughness(image):
    no_seamonsters = remove_seamonsters(image)
    return sum(sum(row) for row in no_seamonsters)

if __name__ == '__main__':
    tiles = parse_tiles(open(sys.argv[1]))
    
    print(len(tiles), 'tiles')
    print('Please allow up to 30s.') # 10s on Intel Core i7-3632QM

    side = int(math.sqrt(len(tiles)))
    part_assign = Assignment(side, side, next(iter(tiles)))
    full_assign = bf(tiles, part_assign).asmatrix()

    corner_tiles = [
        full_assign[0][0],
        full_assign[-1][0],
        full_assign[-1][-1],
        full_assign[0][-1]
    ]
    corner_ids = list(map(lambda t: t.id, corner_tiles))
    print('P1:', functools.reduce(operator.mul, corner_ids))

    recon_image = crop_and_concat(full_assign)
    water_roughness = [water_roughness(i) for i in gen_orientations(recon_image)]
    print('P2:', min(water_roughness))
