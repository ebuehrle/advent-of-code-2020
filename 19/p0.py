import itertools

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

def genmsgs(rules, ruleno=0):
    content = rules[ruleno]
    if type(content) is str:
        yield content
        return

    for alt in content:
        yield from map(''.join, itertools.product(*(genmsgs(rules, r) for r in alt)))

if __name__ == '__main__':
    import sys
    import re
    rules = parse_rules(sys.stdin)
    messages = set(genmsgs(rules))
    correct_messages = [m in messages for m in map(str.strip, sys.stdin)]
    print(sum(correct_messages))
