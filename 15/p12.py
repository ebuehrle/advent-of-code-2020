import sys

max_len = 2020 if len(sys.argv) < 2 else int(sys.argv[1])

starting_numbers = [int(n) for n in input().split(',')]
last_index = {n:i for i, n in enumerate(starting_numbers[:-1])}
last_spoken = starting_numbers[-1]
len_numbers = len(starting_numbers)

while len_numbers < max_len:
    turns_passed = len_numbers - 1 - last_index.get(last_spoken, len_numbers - 1)
    last_index[last_spoken] = len_numbers - 1
    last_spoken = turns_passed
    len_numbers += 1

print(last_spoken)
