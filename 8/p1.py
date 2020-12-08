import sys
from run_program import run_program, fix_program

program = list(map(str.split, map(str.strip, sys.stdin)))
print('P1:', run_program(program))

for fixed_program in fix_program(program):
    terminates, acc = run_program(fixed_program)
    if terminates:
        print('P2:', (terminates, acc))
