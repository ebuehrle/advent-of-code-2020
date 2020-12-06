def read_answers(src):
    ans = [set()]
    idx = 0
    for line in map(str.strip, src):
        if not line:
            ans.append(set())
            idx += 1
            continue
        
        ans[idx] = ans[idx].union(set(line))
    
    return ans

if __name__ == '__main__':
    import sys
    import functools
    import operator

    answers = read_answers(sys.stdin)
    count = map(len, answers)
    print(functools.reduce(operator.add, count))
    