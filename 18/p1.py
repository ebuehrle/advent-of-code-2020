import operator

def eval(tokenstream):
    res = None
    op = None

    def augres(res, op, val):
        return val if res is None else op(res, val)

    for token in tokenstream:
        if token.isdecimal():
            res = augres(res, op, int(token))
        elif token == '+':
            op = operator.add
        elif token == '*':
            op = operator.mul
        elif token == '(':
            res = augres(res, op, eval(tokenstream))
        elif token == ')':
            break
    
    return res

def tokenize(expr):
    return expr.replace('(', '( ').replace(')', ' )').split()

if __name__ == '__main__':
    import sys
    results = [eval(iter(tokenize(l))) for l in sys.stdin]
    print(sum(results))
