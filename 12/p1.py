import math

class Ship:
    def __init__(self):
        self.n = 0
        self.e = 0
        self.r = 0
    
    def north(self, v):
        self.n += v

    def south(self, v):
        self.n -= v
    
    def east(self, v):
        self.e += v
    
    def west(self, v):
        self.e -= v
    
    def left(self, d):
        self.r += d
    
    def right(self, d):
        self.r -= d
    
    def forward(self, v):
        self.e += v * math.cos(math.radians(self.r))
        self.n += v * math.sin(math.radians(self.r))
    
    def manhattan(self):
        return abs(self.e) + abs(self.n)
    
    def __repr__(self):
        return f'Ship(east={self.e}, north={self.n}, rot={self.r})'

if __name__ == '__main__':
    import sys

    ferry = Ship()
    act = {
        'N': ferry.north,
        'S': ferry.south,
        'E': ferry.east,
        'W': ferry.west,
        'L': ferry.left,
        'R': ferry.right,
        'F': ferry.forward
    }

    for line in sys.stdin:
        action, value = line[0], int(line[1:])
        act[action](value)
    
    print(round(ferry.manhattan()))
