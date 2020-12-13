depart = int(input())
ids = [int(i) for i in input().split(',') if i != 'x']
wait = [(i - (depart % i)) % i for i in ids]

min_id, min_wait = min(zip(ids, wait), key=lambda e: e[1])
print(min_id * min_wait)
