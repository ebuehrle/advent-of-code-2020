import sys

adapters = list(sorted(map(int, sys.stdin)))

joltages = [0] + adapters + [adapters[-1] + 3]
dist = [0, 0, 0, 0]
for prv, nxt in zip(joltages[:-1], joltages[1:]):
    dist[nxt - prv] += 1

print('P1:', dist[1] * dist[3])

cnt_ways = [0 for j in joltages]
cnt_ways[-1] = 1
for i in reversed(range(len(joltages[:-1]))):
    v1 = joltages[i]
    for j, v2 in enumerate(joltages[i+1:], i+1):
        if v2 - v1 > 3:
            break
        cnt_ways[i] += cnt_ways[j]

print('P2:', cnt_ways[0])
