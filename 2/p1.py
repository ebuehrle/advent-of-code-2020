def password_valid(policy, passwd):
    lohi, letter = policy.split(' ')
    lo, hi = lohi.split('-')
    return int(lo) <= passwd.count(letter) <= int(hi)

if __name__ == '__main__':
    from sys import stdin
    r = map(lambda q: password_valid(*q.split(': ')), stdin)
    print(sum(r))
