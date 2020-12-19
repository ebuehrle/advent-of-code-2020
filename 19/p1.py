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
    content = rules[ruleno]
    if type(content) is str:
        return content
    
    return parenthesize('|'.join([
        ''.join(make_regex(rules, chain) for chain in alt) for alt in content
    ]))

if __name__ == '__main__':
    import sys
    import re
    rules = parse_rules(sys.stdin)
    regex = '^' + make_regex(rules) + '$'
    correct_messages = [bool(re.match(regex, message)) for message in sys.stdin]
    print(sum(correct_messages))
