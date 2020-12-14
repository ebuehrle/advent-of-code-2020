import sys
import re
import functools

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

def generate_addresses(address_string, mask_string):
    assert len(address_string) == len(mask_string)

    a = address_string[:1]
    m = mask_string[:1]

    if m == '':
        yield ''
    elif m == '0':
        yield from (a + tail for tail in generate_addresses(address_string[1:], mask_string[1:]))
    elif m == '1':
        yield from ('1' + tail for tail in generate_addresses(address_string[1:], mask_string[1:]))
    elif m == 'X':
        for tail in generate_addresses(address_string[1:], mask_string[1:]):
            yield '0' + tail
            yield '1' + tail
    else:
        raise ValueError('Unknown character ' + m + ' in mask.')

if __name__ == '__main__':
    input_lines = list(map(str.strip, sys.stdin))

    instructions = []
    for instruction in input_lines:
        if instruction.startswith('mask = '):
            current_mask = instruction[len('mask = '):]
        else:
            address, value = map(int, re.match('^mem\[(\d+)\] = (\d+)$', instruction).groups())
            instructions.extend([(a, value, current_mask) for a in generate_addresses('{:036b}'.format(address), current_mask)])

    print(len(input_lines), 'input lines')
    print(len(instructions), 'expanded instructions')
    print(len(instructions) / len(input_lines), 'times increase')

    instructions.sort(key=lambda i: i[0]) # stable; writes to same memory location are kept in order
    instructions.reverse()

    lastaddr_sum = functools.reduce(
        # state = (last_addr, current_sum)
        # instr = (address, value, mask)
        lambda state, instr: (instr[0], state[1] + (0 if instr[0] == state[0] else instr[1])),
        instructions,
        (-1, 0)
    )

    print(lastaddr_sum[1])
