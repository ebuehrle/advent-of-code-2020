# Reminiscent of the Chinese Remainder Theorem,
# but the text does not state that the shuttle
# intervals are pairwise coprime (even though
# they actually were prime in my input).

def lcm(a, b):
    """ Least Common Multiple """
    return a * b // gcd(a, b)

def gcd(a, b):
    """ Greatest Common Divisor """
    return a if b == 0 else gcd(b, a % b)

def min_time(time, incr, remaining_shuttles):
    if not remaining_shuttles:
        return time
    
    interval, target_wait = remaining_shuttles.pop()
    while (time % interval) != (interval - target_wait) % interval:
        time += incr # previous wait times remain unchanged
    
    incr = lcm(incr, interval)

    return min_time(time, incr, remaining_shuttles)

_ = int(input())
ids = [(int(v), i) for (i, v) in enumerate(input().split(',')) if v != 'x']
print(min_time(0, 1, ids))
