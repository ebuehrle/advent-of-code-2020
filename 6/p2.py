def read_answers(src):
    ans = [set('abcdefghijklmnopqrstuvwxyz')]
    idx = 0
    for line in map(str.strip, src):
        if not line:
            ans.append(set('abcdefghijklmnopqrstuvwxyz'))
            idx += 1
            continue
        
        ans[idx] = ans[idx].intersection(set(line))
    
    return ans

if __name__ == '__main__':
    import sys
    import functools
    import operator

    answers = read_answers(sys.stdin)
    count = map(len, answers)
    print(functools.reduce(operator.add, count))