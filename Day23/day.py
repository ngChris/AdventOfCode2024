from collections import defaultdict
import timeit
import re

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def inter_connection_count(conn, network):
    connection = conn.split(',')
    count = 0
    for i, c1 in enumerate(connection):
        for j, c2 in enumerate(connection[i + 1 :], i + 1):
            if c2 in network[c1]:
                count += 1
    return count

def solve1(connections,part2=False):
    network = defaultdict(list)
    all_sets = defaultdict(list)
    for connection in connections:
        network[connection[0]].append(connection[1])
        network[connection[1]].append(connection[0])
        inter = intersection(network[connection[0]], network[connection[1]])
        if len(inter) > 0:
            l = [connection[0], connection[1]]
            for it in inter:
                l.append(it)
            k = ','.join(sorted(l))
            all_sets[len(k)].append(k)
    
    best_conns_index = max(all_sets)
    inter_conns = [(inter_connection_count(f, network),f) for f in all_sets[best_conns_index]]
    best = max(inter_conns)
    return best[1]
 
def digits(string):
    regex = r"(?<!\.)[0-9]+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ str(match.group(0)) for n, match in enumerate(matches, start=1)]


def letters(string):
    regex = r"(?<!\.)[A-Z]+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ str(match.group(0)) for n, match in enumerate(matches, start=1)]

def ints(string):
    regex = r"(?<!\.)-?\d+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ int(match.group(0)) for n, match in enumerate(matches, start=1)]


def readInput(filename):
    with open(filename) as csvfile:

        def parse_row(row):
            f = row.replace('\n', '').split('-')
            return (f[0], f[1])

        return [parse_row(row) for row in csvfile.readlines()]

m = readInput('input.txt')

print(timeit.timeit(lambda: print(solve1(m)), number=1))