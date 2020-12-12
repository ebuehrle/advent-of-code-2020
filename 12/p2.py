import math
import cmath

class Ship:
    def __init__(self):
        self.n = 0
        self.e = 0
        self.wn = 1
        self.we = 10
    
    def north(self, v):
        self.wn += v

    def south(self, v):
        self.north(-v)
    
    def east(self, v):
        self.we += v
    
    def west(self, v):
        self.east(-v)
    
    # def left(self, d):
    #     waypoint_distance = math.sqrt(self.we**2 + self.wn**2)
    #     current_angle_rad = math.atan(self.wn / self.we) + (math.radians(180) if self.we < 0 else 0)
    #     total_angle = current_angle_rad + math.radians(d)
    #     self.we = waypoint_distance * math.cos(total_angle)
    #     self.wn = waypoint_distance * math.sin(total_angle)
    
    def left(self, d):
        current = self.we + self.wn * 1j
        rotate = cmath.rect(1, math.radians(d))
        total = current * rotate
        self.we = total.real
        self.wn = total.imag
    
    def right(self, d):
        self.left(-d)
    
    def forward(self, v):
        self.e += v * self.we
        self.n += v * self.wn
    
    def manhattan(self):
        return abs(self.e) + abs(self.n)
    
    def __repr__(self):
        return f'Ship(e={self.e}, n={self.n}, we={self.we}, wn={self.wn})'

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
