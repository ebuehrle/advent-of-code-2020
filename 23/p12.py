class llelem:
    def __init__(self, prev, content):
        self.content = content
        self.next = None
        if prev:
            prev.next = self

def makell(items):
    start = None
    end = None
    cache = {}
    for item in items:
        if end:
            end = llelem(end, item)
        else:
            start = llelem(None, item)
            end = start

        cache[end.content] = end

    return start, end, cache

def makelist(llstart):
    llist = []
    while llstart:
        llist.append(llstart.content)
        llstart = llstart.next
    return llist

def wrap(n, minn, maxn):
    return minn + (n - minn) % (maxn - minn + 1)

def game(cups, moves=100):
    maxc = max(cups)
    minc = min(cups)
    current, lastc, cache = makell(cups)

    for move in range(moves):
        pick1 = current.next
        pick2 = pick1.next
        pick3 = pick2.next

        best_possible_pick = wrap(current.content - 1, minc, maxc)
        while best_possible_pick in {pick1.content, pick2.content, pick3.content}:
            best_possible_pick = wrap(best_possible_pick - 1, minc, maxc)

        destination = cache[best_possible_pick]    

        current.next = pick3.next
        pick3.next = destination.next
        destination.next = pick1

        lastc = lastc if destination != lastc else pick3
        lastc.next = current
        lastc = current

        first = current
        current = current.next
        first.next = None
    
    return makelist(current)

if __name__ == '__main__':
    import sys

    cups = list(map(int, open(sys.argv[1]).readline().strip()))

    print('Please allow up to 60s') # 30s on Intel Core i7-3632QM

    final1 = game(cups, 100)
    pos1 = final1.index(1)
    labels_after_1 = final1[pos1:] + final1[:pos1]
    print('P1:', ''.join(map(str, labels_after_1[1:])))

    cups2 = cups + list(range(max(cups)+1, 1_000_001))
    final2 = game(cups2, 10_000_000)
    pos1 = final2.index(1)
    pos2 = (pos1 + 1) % len(final2)
    pos3 = (pos1 + 2) % len(final2)
    print('P2:', final2[pos2] * final2[pos3])
