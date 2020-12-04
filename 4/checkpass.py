import re

def passport_valid(passport):
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    return all(f in passport for f in required_fields)

def passport_valid2(passport):
    required_fields_present = passport_valid(passport)

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

    validator = {
        'byr': lambda v: re.match('^\d{4}$', v) and 1920 <= int(v) <= 2002,
        'iyr': lambda v: re.match('^\d{4}$', v) and 2010 <= int(v) <= 2020,
        'eyr': lambda v: re.match('^\d{4}$', v) and 2020 <= int(v) <= 2030,
        'hgt': hgt_validator,
        'hcl': lambda v: re.match('^#[0-9a-f]{6}$', v),
        'ecl': lambda v: re.match('^(amb|blu|brn|gry|grn|hzl|oth)$', v),
        'pid': lambda v: re.match('^\d{9}$', v),
    }
    
    fields_valid = [validator[f](v) for f, v in passport.items() if f in validator]
    return required_fields_present and all(fields_valid)

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