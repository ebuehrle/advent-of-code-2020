import sys
import count_trees

forest = list(map(str.strip, sys.stdin))
print(count_trees.count_trees_rec(forest, 0, 0, (3, 1)))
