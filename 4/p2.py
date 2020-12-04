from sys import stdin
from checkpass import passport_valid2, read_passports

v = map(passport_valid2, read_passports(stdin))    
print(sum(v))