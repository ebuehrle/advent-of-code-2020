import sys
import functools
import operator

def parse_input(src):
    input_lines = map(str.strip, src)

    rules = []
    for rule in input_lines:
        if not rule:
            break
        
        name, values = rule.split(': ')
        ranges = values.split(' or ')
        ranges = [r.split('-') for r in ranges]
        ranges = [(int(r1), int(r2)) for (r1, r2) in ranges]
        rules.append((name, ranges))
    
    assert next(input_lines) == 'your ticket:'
    my_ticket = [int(v) for v in next(input_lines).split(',')]

    assert next(input_lines) == ''
    assert next(input_lines) == 'nearby tickets:'
    nearby_tickets = []
    for nearby_ticket in input_lines:
        nearby_tickets.append([int(v) for v in nearby_ticket.split(',')])
    
    return (rules, my_ticket, nearby_tickets)

def reduce_intervals(intervals_list):
    def make_set(interval):
        return set(range(interval[0], interval[1]+1))

    return functools.reduce(
        lambda union, interval: union.union(make_set(interval)),
        intervals_list,
        set()
    )

def ticket_error(ticket, valid_values):
    invalid_values = [v for v in ticket if v not in valid_values]
    return -1 if not invalid_values else sum(invalid_values)

def possible_permutations(candidates, partial_assignment=None):
    """Use a CSP library next time."""
    if not partial_assignment:
        partial_assignment = [None] * len(candidates)

    used = set(partial_assignment)
    if None not in used:
        yield partial_assignment
        return
    
    # Assign fields with fewest candidates first
    _, next_idx = min((len(c), i) for i, c in enumerate(candidates) if not partial_assignment[i])
    # It might be more efficient to try the candidates in order of
    # the number fields they are candidates for (not done here).
    for c in filter(lambda c: c not in used, candidates[next_idx]):
        partial_assignment[next_idx] = c
        yield from possible_permutations(candidates, partial_assignment)

    partial_assignment[next_idx] = None

if __name__ == '__main__':
    (rules, my_ticket, nearby_tickets) = parse_input(sys.stdin)

    reduced_intervals = [(name, reduce_intervals(ranges)) for name, ranges in rules]
    valid_values = functools.reduce(set.union, (r for _, r in reduced_intervals))
    ticket_errors = [ticket_error(t, valid_values) for t in nearby_tickets]
    
    print('Ticket Scanning Error Rate (P1)', sum(e for e in ticket_errors if e != -1))

    valid_nearby_tickets = [t for (t, e) in zip(nearby_tickets, ticket_errors) if e == -1]
    occurring_values = functools.reduce(
        lambda occ, tkt: [o.union({t}) for (o, t) in zip(occ, tkt)],
        [my_ticket] + valid_nearby_tickets,
        [set()] * len(my_ticket)
    )

    # For each field, find candidate field names
    # based on the occurring and allowed values.
    candidates = [
        {name for name, rnge in reduced_intervals if o.issubset(rnge)} for o in occurring_values
    ]

    for p in possible_permutations(candidates):
        print('Possible permutation:', p)
        relevant_values = [n for f, n in zip(p, my_ticket) if f.startswith('departure')]
        print('  Resulting product (P2):', functools.reduce(operator.mul, relevant_values))
