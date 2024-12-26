from heapq import heappop, heappush
from itertools import groupby
import timeit
from typing import Callable, Iterable, Any, Dict, Optional
import re

def flatten(xss):
    return [x for xs in xss for x in xs]

def to_map(
    items: Iterable[Any],
    key_func: Callable[[Any], Any],
    collision_func: Optional[Callable[[Any, Any], Any]] = None
) -> Dict[Any, Any]:
    """
    Maps items to a dictionary based on a key function, with optional collision handling.

    :param items: Iterable of items to be mapped.
    :param key_func: Function to extract the key from an item.
    :param collision_func: Optional function to resolve key collisions. 
                           Takes two arguments (current_value, new_value) and returns the resolved value.
    :return: A dictionary mapping keys to values.
    """
    result = {}
    for item in items:
        key = key_func(item)
        if key in result:
            if collision_func:
                result[key] = collision_func(result[key], item)
            else:
                raise ValueError(f"Collision detected for key '{key}' with no collision_func provided.")
        else:
            result[key] = item
    return result

def group_by(data, key_func):
    """
    Groups items in `data` by the value returned by `key_func`.
    
    Parameters:
    - data: Iterable of items to be grouped.
    - key_func: Function to extract the grouping key from each item.
    
    Returns:
    - A dictionary where keys are the grouping values and values are lists of items in each group.
    """
    # Sort data by key_func to ensure groupby works correctly
    sorted_data = sorted(data, key=key_func)
    
    # Use groupby to group the data
    grouped_data = {
        key: list(group) for key, group in groupby(sorted_data, key=key_func)
    }
    
    return grouped_data

def print_maze(m):
        s = ''
        for i in range(0, len(m)):
            s += ''.join(m[i]) + '\n'
        print(s)   

def solve2(maze, part2=False):
    m = len(maze)
    n = len(maze[0])
    cheat_dur = 2 if part2 == False else 20
    start = None
  
    stop = None
    walls = []
    for i in range(0,m):
        for e in range(0, n):
            if maze[i][e] == 'S':
                start = (i,e)
            if maze[i][e] == 'E':
                stop = (i,e)
            if maze[i][e] == '#':
                walls.append((i, e))
                
    cost_map, solutions = dikstra(maze, start, stop)
    baseline = min(solutions)

    def node_diff(node1, node2):
        return (abs(node1[0] - node2[0]), abs(node1[1]- node2[1]))

    def evaluate_cost(nodestart, nodeend):
        diff = cost_map[nodeend] - cost_map[nodestart]
        return baseline - diff

    cheats = []
    for path in cost_map:
        for reachable in cost_map:
            diff = sum(node_diff(path, reachable)) 
            if diff >= 2 and diff <= cheat_dur and cost_map[reachable] > cost_map[path]:
                new_cost = evaluate_cost(path, reachable) + diff
                #print(str(path) + ' -> ' + str(reachable) + ' = ' + str(new_cost))
                if new_cost < baseline:
                        cheats.append(baseline - new_cost)
    cheat_stat = list(filter(lambda x: x >= 100, cheats))
    g =  group_by(cheat_stat, lambda x: x)
    s = sum([len(g[k]) for k in g])
    return s

def dikstra(maze, start, stop):
    m = len(maze)
    n = len(maze[0])

    def is_on_map(node):
        return (node[0] >= m or node[0] < 0 or node[1] >= n or node[1] < 0) == False
    
    curr = start
  
    target = stop

    def iterate_throug_neighbor_nondiag(node):
        x = [-1, 0, 0, 1]
        y = [ 0,-1, 1, 0]
        nei = []
        for dir in range(0, len(x)):
            nextX = node[0] + x[dir]
            nextY = node[1] + y[dir]
            next = (nextX, nextY)
            nei.append(next)
        return nei
    
    visited_loc = dict()
    queue = [(0, curr)]
    solutions = []
    while len(queue) > 0:
        steps, curr = heappop(queue)

        if curr in visited_loc and visited_loc[curr] <= steps:
            continue
        visited_loc[curr] = steps
        if curr == target:
           solutions.append(steps)

        nei = iterate_throug_neighbor_nondiag(curr)

        for w in nei:
            if is_on_map(w) and maze[w[0]][w[1]] != '#':
                heappush(queue, (steps + 1, w))
    return visited_loc, solutions
    
def letters(string):
    regex = r"(?<!\.)[A-Z]+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ str(match.group(0)) for n, match in enumerate(matches, start=1)]

def ints(string):
    regex = r"(?<!\.)\d+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ int(match.group(0)) for n, match in enumerate(matches, start=1)]


def readInput(filename):
    with open(filename) as csvfile:

        def parse_row(row):
            f = row.replace('\n', '')
            return list(f)

        return [parse_row(row) for row in csvfile.readlines()]

m = readInput('input.txt')
print(timeit.timeit(lambda: print(solve2(m, False)), number=1))
print(timeit.timeit(lambda: print(solve2(m, True)), number=1))