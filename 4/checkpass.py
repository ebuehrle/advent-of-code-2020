import re

def passport_valid(passport):
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    return all(f in passport for f in required_fields)

def passport_valid2(passport):
    required_fields_present = passport_valid(passport)
    validator = {
        'byr': byr_validator,
        'iyr': iyr_validator,
        'eyr': eyr_validator,
        'hgt': hgt_validator,
        'hcl': hcl_validator,
        'ecl': ecl_validator,
        'pid': pid_validator,
    }
    fields_valid = [validator[f](v) for f, v in passport.items() if f in validator]
    return required_fields_present and all(fields_valid)

def byr_validator(v):
    return re.match('^\d{4}$', v) and 1920 <= int(v) <= 2002

def iyr_validator(v):
    return re.match('^\d{4}$', v) and 2010 <= int(v) <= 2020

def eyr_validator(v):
    return re.match('^\d{4}$', v) and 2020 <= int(v) <= 2030

def hgt_validator(v):
    matchr = re.match('^(\d+)(cm|in)$', v)
    if not matchr:
        return False

    num, unit = matchr.groups()
    if unit == 'cm':
        return 150 <= int(num) <= 193
    elif unit == 'in':
        return 59 <= int(num) <= 76
    
    return False

def hcl_validator(v):
    return re.match('^#[0-9a-f]{6}$', v)

def ecl_validator(v):
    return re.match('^(amb|blu|brn|gry|grn|hzl|oth)$', v)

def pid_validator(v):
    return re.match('^\d{9}$', v)

def read_passports(src):
    passports = [{}]
    current_index = 0
    for line in map(str.strip, src):
        if not line:
            passports.append({})
            current_index += 1
        
        entries = line.split()
        kvpairs = [e.split(':') for e in entries]
        passports[current_index].update({k: v for k, v in kvpairs})
    
    return passports