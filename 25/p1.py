import itertools

def transform(subject_number, value=1):
    while True:
        yield value
        value *= subject_number
        value %= 20201227

if __name__ == '__main__':
    card_public_key = int(input().strip())
    door_public_key = int(input().strip())
    card_loop_size = next(i for i, v in enumerate(transform(7)) if v == card_public_key)
    door_loop_size = next(i for i, v in enumerate(transform(7)) if v == door_public_key)
    encryption_key = next(itertools.islice(transform(card_public_key), door_loop_size, None))
    print('P1:', encryption_key)