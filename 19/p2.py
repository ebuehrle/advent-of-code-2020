def parse_rules(src):
    rules = {}
    for rule in map(str.strip, src):
        if not rule:
            break

        number, contents = rule.split(': ')
        
        if contents.startswith('"'):
            rules[int(number)] = contents[1:-1]
            continue

        rules[int(number)] = [tuple(map(int, s.split())) for s in contents.split('|')]

    return rules

def parenthesize(regex):
    return '(' + regex + ')'

def make_regex(rules, ruleno=0):
    if ruleno == 8:
        return parenthesize(make_regex(rules, 42)) + '+'
    if ruleno == 11:
        return '(%R11%)'

    content = rules[ruleno]
    if type(content) is str:
        return content
    
    return parenthesize('|'.join([
        ''.join(make_regex(rules, chain) for chain in alt) for alt in content
    ]))

def generate_r11(rules, maxreps):
    r42 = make_regex(rules, 42)
    r31 = make_regex(rules, 31)
    for reps in range(1, maxreps):
        yield r42 * reps + r31 * reps

if __name__ == '__main__':
    import sys
    import re
    
    rules = parse_rules(sys.stdin)
    regex = '^' + make_regex(rules, 0) + '$'

    num_correct_messages = 0
    for i, message in enumerate(sys.stdin):
        print(i)
        for r11 in generate_r11(rules, len(message)):
            final_re = regex.replace('%R11%', r11)
            if re.match(final_re, message):
                num_correct_messages += 1
                break

    print(num_correct_messages)
