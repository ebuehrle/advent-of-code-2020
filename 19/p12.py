import functools

def parse_rules(src):
    rules = {}
    for rule in map(str.strip, src):
        if not rule:
            break

        number, contents = rule.split(': ')
        
        if contents.startswith('"'):
            rules[int(number)] = contents.strip('"')
            continue

        rules[int(number)] = [tuple(map(int, s.split())) for s in contents.split('|')]

    return rules

class Matcher:
    def __init__(self, rules):
        self.rules = rules

    @functools.cache
    def matchrule(self, ruleno, string):
        content = self.rules[ruleno]
        if type(content) is str:
            return string == content
        
        for chain in content:
            if chain == (ruleno,):
                continue # no progress to be made
            if self.matchchain(chain, string):
                return True

        return False

    @functools.cache
    def matchchain(self, chain, string):
        if len(chain) == 1:
            return self.matchrule(chain[0], string)
        
        for s in range(1, len(string)):
            if self.matchrule(chain[0], string[:s]) and self.matchchain(chain[1:], string[s:]):
                return True
        
        return False

if __name__ == '__main__':
    import sys
    rules = parse_rules(sys.stdin)
    messages = list(map(str.strip, sys.stdin))

    # 29s on Intel Core i7-3632QM
    print('Please allow up to 60 seconds')

    m1 = Matcher(rules)
    matching1 = [m1.matchrule(0, m) for m in messages]
    print('P1:', sum(matching1))

    # Part 2
    rules[8] = [(42,), (42, 8)]
    rules[11] = [(42, 31), (42, 11, 31)]

    m2 = Matcher(rules)
    matching2 = [m2.matchrule(0, m) for m in messages]
    print('P2:', sum(matching2))
