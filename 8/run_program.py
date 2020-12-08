def run_program(program):
    executed = [False for i in program]
    ip = 0
    acc = 0

    while True:
        if ip == len(program):
            return (True, acc)
        elif ip > len(program) or executed[ip]:
            return (False, acc)

        instr = program[ip]
        executed[ip] = True

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
        if instr[0] == 'nop':
            yield program[:idx] + [['jmp'] + instr[1:]] + program[idx+1:]
        elif instr[0] == 'jmp':
            yield program[:idx] + [['nop'] + instr[1:]] + program[idx+1:]
