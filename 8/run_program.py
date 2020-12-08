def run_program(program):
    executed = set()
    ip = 0
    acc = 0

    while True:
        if ip == len(program):
            return (True, acc)
        elif ip > len(program) or ip in executed:
            return (False, acc)

        instr = program[ip].split()
        executed.add(ip)

        if instr[0] == 'nop':
            ip += 1
        elif instr[0] == 'jmp':
            ip += int(instr[1])
        elif instr[0] == 'acc':
            acc += int(instr[1])
            ip += 1
        else:
            raise ValueError('Unknown instruction ' + instr)

def fix_program(program):
    for idx, instr in enumerate(program):
        if instr.startswith('nop'):
            yield program[:idx] + [instr.replace('nop', 'jmp')] + program[idx+1:]
        elif instr.startswith('jmp'):
            yield program[:idx] + [instr.replace('jmp', 'nop')] + program[idx+1:]
