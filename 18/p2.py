import operator

def ev(tokenlist, start=0):
    # print(tokenlist)

    if len(tokenlist) == 1:
        return tokenlist[0]

    if tokenlist[start] == '(' and type(tokenlist[start+1]) is int and tokenlist[start+2] == ')':
        # print('Reducing simple parenthese')
        tokenlist = tokenlist[:start] + [tokenlist[start+1]] + tokenlist[start+3:]
        if start > 0:
            return tokenlist
    
    if tokenlist[start] == '(':
        # print('Reducing in parenthese')
        tokenlist = ev(tokenlist, start + 1)
        return ev(tokenlist, start)
    
    assert type(tokenlist[start]) is int

    if start + 1 >= len(tokenlist) or tokenlist[start+1] == ')':
        # cannot further reduce left
        # print('Done reducing')
        return tokenlist

    assert start + 2 < len(tokenlist)
    assert tokenlist[start + 1] in {'+', '*'}

    if tokenlist[start + 2] == '(':
        # print('Reducing parenthese right of operand')
        tokenlist = ev(tokenlist, start + 2)
    
    assert type(tokenlist[start + 2]) is int

    if tokenlist[start + 1] == '+':
        # int, +, int (, ...)
        # takes precedence
        # print('+ takes precedence')
        tokenlist = tokenlist[:start] + [tokenlist[start] + tokenlist[start+2]] + tokenlist[start+3:]
        return ev(tokenlist, start)
    else:
        # print('* has lower precedence')
        tokenlist = ev(tokenlist, start + 2)
        tokenlist = tokenlist[:start] + [tokenlist[start] * tokenlist[start+2]] + tokenlist[start+3:]
        return ev(tokenlist, start)


def tokenize(expr):
    split_tokens = expr.replace('(', '( ').replace(')', ' )').split()
    make_ints = [int(t) if t.isdecimal() else t for t in split_tokens]
    return make_ints

if __name__ == '__main__':
    import sys
    results = [ev(tokenize(l)) for l in sys.stdin]
    print(sum(results))
