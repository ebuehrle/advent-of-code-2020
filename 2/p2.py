def password_valid(policy, passwd):
    lohi, letter = policy.split(' ')
    lo, hi = lohi.split('-')
    i1 = int(lo) - 1
    i2 = int(hi) - 1
    return (passwd[i1] == letter) != (passwd[i2] == letter)

if __name__ == '__main__':
    from sys import stdin
    r = map(lambda q: password_valid(*q.split(': ')), stdin)
    print(sum(r))
