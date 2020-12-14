import sys
import re
import functools

instructions = []
current_mask = ''
for instruction in map(str.strip, sys.stdin):
    if instruction.startswith('mask = '):
        current_mask = instruction[len('mask = '):]
    else:
        address, value = re.match('^mem\[(\d+)\] = (\d+)$', instruction).groups()
        instructions.append((int(address), int(value), current_mask))

instructions.sort(key=lambda i: i[0]) # stable; writes to same memory location are kept in order
instructions.reverse()

@functools.lru_cache(maxsize=1)
def ones(mask):
    make_zeros = [pos for (pos, value) in enumerate(reversed(mask)) if value == '1']
    bit_values = [2**bit for bit in make_zeros]
    return sum(bit_values)

@functools.lru_cache(maxsize=1)
def zeros(mask):
    make_ones = [pos for (pos, value) in enumerate(reversed(mask)) if value != '0']
    bit_values = [2**bit for bit in make_ones]
    return sum(bit_values)

def masked(value, mask):
    value = value | ones(mask)
    value = value & zeros(mask)
    return value

lastaddr_sum = functools.reduce(
    # state = (last_addr, current_sum); instr = (address, value, mask)
    lambda state, instr: (instr[0], state[1] + (0 if instr[0] == state[0] else masked(instr[1], instr[2]))),
    instructions,
    (-1, 0)
)

print(lastaddr_sum[1])
