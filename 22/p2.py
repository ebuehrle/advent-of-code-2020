def parse_cards(src):
    p1cards = []
    p2cards = []

    lines = map(str.strip, src)

    assert next(lines) == 'Player 1:'
    for line in lines:
        if not line:
            break
        p1cards.append(int(line))

    assert next(lines) == 'Player 2:'
    for line in lines:
        p2cards.append(int(line))
    
    return tuple(p1cards), tuple(p2cards)

def score(deck):
    card_scores = [i*c for i, c in enumerate(reversed(deck), 1)]
    return sum(card_scores)

def recursive_combat(p1cards, p2cards):
    previous_hands = set()

    while p1cards and p2cards:
        if (p1cards, p2cards) in previous_hands:
            return (score(p1cards), 0)

        previous_hands.add((p1cards, p2cards))

        p1 = p1cards[0]
        p2 = p2cards[0]

        if (len(p1cards) - 1 >= p1) and (len(p2cards) - 1 >= p2):
            round_score = recursive_combat(p1cards[1:1+p1], p2cards[1:1+p2])
        else:
            round_score = (p1, p2)

        assert round_score[0] != round_score[1], 'Could not determine winner.'
        if round_score[0] > round_score[1]:
            p1cards = p1cards[1:] + (p1, p2)
            p2cards = p2cards[1:]
        else:
            p1cards = p1cards[1:]
            p2cards = p2cards[1:] + (p2, p1)
    
    return (score(p1cards), score(p2cards))

if __name__ == '__main__':
    import sys
    p1cards, p2cards = parse_cards(open(sys.argv[1]))
    score = recursive_combat(p1cards, p2cards)
    print(score)
