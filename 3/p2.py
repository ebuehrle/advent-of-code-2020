import sys
import count_trees
import functools
import operator

forest = list(map(str.strip, sys.stdin))
r = [count_trees.count_trees_rec(forest, 0, 0, slope) for slope in [
    (1, 1), (3, 1), (5, 1), (7, 1), (1, 2)
]]
print(r)
print(functools.reduce(operator.mul, r))