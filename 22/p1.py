from collections import deque

def parse_cards(src):
    p1cards = deque()
    p2cards = deque()

    lines = map(str.strip, src)

    assert next(lines) == 'Player 1:'
    for line in lines:
        if not line:
            break
        p1cards.append(int(line))

    assert next(lines) == 'Player 2:'
    for line in lines:
        p2cards.append(int(line))
    
    return p1cards, p2cards

def score(deck):
    card_scores = [(i+1)*c for i, c in enumerate(reversed(deck))]
    return sum(card_scores)

def combat(p1cards, p2cards):
    while p1cards and p2cards:
        p1 = p1cards.popleft()
        p2 = p2cards.popleft()

        assert p1 != p2, f'Found two cards of value {p1}'

        if p1 > p2:
            p1cards.append(p1)
            p1cards.append(p2)
        elif p2 > p1:
            p2cards.append(p2)
            p2cards.append(p1)
    
    if p1cards:
        return score(p1cards)
    else:
        return score(p2cards)

if __name__ == '__main__':
    import sys
    p1cards, p2cards = parse_cards(open(sys.argv[1]))
    score = combat(p1cards, p2cards)
    print(score)
