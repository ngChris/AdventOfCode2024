from itertools import groupby
import re
import timeit
from typing import Callable, Iterable, Any, Dict, Optional

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

def search_trailheads(maze):
    heads = []
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == '0':
                heads.append(( i, j))
    return heads

def solve(maze, part2=False):
    m = len(maze)
    n = len(maze[0])
    heads = search_trailheads(maze)

    def is_on_map(node):
        return (node[0] >= m or node[0] < 0 or node[1] >= n or node[1] < 0) == False

    def find_trails(curr_a):
        trails = []
        def find_trails_rek(curr, trail):
        
            currX, currY = curr[0], curr[1]
            trail += str(curr)
        
            x = [-1, 0,  1, 0]
            y = [0,  1, 0, -1]

            if is_on_map(curr):
                if maze[currX][currY] == '9':
                    trails.append(trail)
                    return 1
                else:
                    s = 0
                    for dir in range(0, len(x)):

                        nextX = currX + x[dir]
                        nextY = currY + y[dir]
                        next = (nextX, nextY)
                        if is_on_map(next):
                            if int(maze[currX][currY]) + 1 == int(maze[nextX][nextY]):
                                s += find_trails_rek(next, trail)
                    return s      
            return 0
        find_trails_rek(curr_a, '')
        return len(trails)

    return sum([find_trails(t) for t in heads])
            
def ints(string):
    regex = r"(?<!\.)\d+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ int(match.group(0)) for n, match in enumerate(matches, start=1)]

def readInput(filename):
    with open(filename) as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            return list(f)

        rows = [ sanitize(row) for row in csvfile.readlines()]
        return rows

m = readInput('input.txt')

print(timeit.timeit(lambda: print(solve(m, True)), number=1))