import sys
import functools
import operator

def checknsum(expenses, target, n, start=0):
    if n == 0:
        return () if target == 0 else None

    for i, z in enumerate(expenses[start:], start):
        t = target - z
        r = checknsum(expenses, t, n-1, i+1)
        if r is not None:
            return (i,) + r

if __name__ == '__main__':
    expenses = list(map(int, sys.stdin))
    target = 2020
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2

    r = checknsum(expenses, target, n)
    p = functools.reduce(lambda p, i: p * expenses[i], r, 1)
    print(p)
