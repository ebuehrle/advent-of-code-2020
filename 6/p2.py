import sys
import functools
import operator

initset = set('abcdefghijklmnopqrstuvwxyz')

stripln = map(str.strip, sys.stdin)
answers = functools.reduce(
    lambda acc, x: acc[:-1] + [acc[-1].intersection(set(x))] if x else acc + [initset],
    stripln,
    [initset]
)
cntansw = map(len, answers)

print(functools.reduce(operator.add, cntansw))
