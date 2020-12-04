from sys import stdin
from checkpass import passport_valid, read_passports

v = map(passport_valid, read_passports(stdin))    
print(sum(v))