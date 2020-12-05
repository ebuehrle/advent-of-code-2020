def get_value(desc, takeupper, takelower):
    vrange = (0, 2**len(desc) - 1)
    for d in desc:
        mid = (vrange[0] + vrange[1]) // 2
        if d == takeupper:
            vrange = (mid + 1, vrange[1])
        elif d == takelower:
            vrange = (vrange[0], mid)
        else:
            raise ValueError('Unknown character')
    
    assert vrange[0] == vrange[1]
    return vrange[0]

def seat_id(seat):
    row = get_value(seat[:7], 'B', 'F')
    col = get_value(seat[7:], 'R', 'L')
    return row * 8 + col

if __name__ == '__main__':
    import sys
    ids = list(map(seat_id, map(str.strip, sys.stdin)))
    print('Max. ID', max(ids))
    
    sorted_ids = list(sorted(ids))
    for i, sid in enumerate(sorted_ids[:-1]):
        next_sid = sorted_ids[i + 1]
        if next_sid - sid == 2:
            print('missing seat ID', sid + 1)