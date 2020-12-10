def parse_rule(rule):
    container_color, content = rule.split(' bags contain ')
    content = content.split(', ')
    content = [c.split() for c in content]
    content = [(0 if c[0] == 'no' else int(c[0]), c[1] + ' ' + c[2]) for c in content]
    return (container_color, content)

def add_rule(graph, rule):
    graph.update({rule[0]: rule[1]})
    return graph

def add_invrule(graph, rule):
    if not rule[1]:
        return graph

    container_color = rule[0]

    for n, bag_color in rule[1]:
        if bag_color not in graph:
            graph[bag_color] = {container_color}
        else:
            graph[bag_color].add(container_color)

    return graph

def get_containers(bag_color, inv_digraph):
    visited = set()
    found = set()

    def dfs(bag_color, inv_digraph, visited, found):
        if bag_color in visited or bag_color not in inv_digraph:
            return
        
        visited.add(bag_color)

        for container_color in inv_digraph[bag_color]:
            found.add(container_color)
            dfs(container_color, inv_digraph, visited, found)
    
    dfs(bag_color, inv_digraph, visited, found)
    return found

def count_inside_bags(bag_color, digraph):
    if bag_color not in digraph:
        return 0
    
    count = 0
    for n, c in digraph[bag_color]:
        count += n
        count += n * count_inside_bags(c, digraph)
    
    return count

if __name__ == '__main__':
    import sys
    import functools

    rules = list(map(parse_rule, map(str.strip, sys.stdin)))
    digraph = functools.reduce(add_rule, rules, dict())
    inv_digraph = functools.reduce(add_invrule, rules, dict())

    containers = get_containers('shiny gold', inv_digraph)
    print('P1:', len(containers))

    num_inside_bags = count_inside_bags('shiny gold', digraph)
    print('P2:', num_inside_bags)