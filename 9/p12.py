def checknsum(numbers, target, n, start=0):
    if n == 0:
        return () if target == 0 else None

    for i, z in enumerate(numbers[start:], start):
        t = target - z
        r = checknsum(numbers, t, n-1, i+1)
        if r is not None:
            return (i,) + r

def find_invalid(numbers, preamble):
    for i, z in enumerate(numbers[preamble:], preamble):
        if not checknsum(numbers[i-preamble:i], z, 2):
            return z

def findsum(numbers, target):
    lo, hi = 0, 1
    while lo < len(numbers) and hi <= len(numbers):
        r = sum(numbers[lo:hi])
        if r == target:
            return (lo, hi)
        elif r < target:
            hi += 1
        elif r > target:
            lo += 1

if __name__ == '__main__':
    import sys

    numbers = list(map(int, sys.stdin))
    invalid = find_invalid(numbers, 25)
    print('P1', invalid)

    lo, hi = findsum(numbers, invalid)
    smallest = min(numbers[lo:hi])
    largest = max(numbers[lo:hi])
    print('P2', smallest + largest)
