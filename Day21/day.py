from functools import cache
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

def get_min(*values):
    return min(i for i in values if i is not None)

def is_dir(start, dest, change):
    return (change < 0 and dest < start) or (change > 0 and dest > start)


def solve3(codes):
    keypad_moves= {0: '^', 1: '<', 2: '>', 3: 'v', 4: 'A'}
    numeric_pad_map = [['7', '8', '9'],['4', '5', '6'],['1', '2', '3'],['', '0', 'A']]
    keypad_map = [['', '^', 'A'], ['<', 'v', '>']]

    x = [-1, 0, 0, 1]
    y = [ 0,-1, 1, 0]

    @cache
    def is_on_map(node, pad_id):
        pad = keypad_map if pad_id == 0 else numeric_pad_map
        m = len(pad)
        n = len(pad[0])
        return (node[0] >= m or node[0] < 0 or node[1] >= n or node[1] < 0) == False
    
    @cache
    def find_pos(pad_id, symbol):
        pad = keypad_map if pad_id == 0 else numeric_pad_map
        for i in range(0, len(pad)):
            for e in range(0, len(pad[0])):
                if pad[i][e] == symbol:
                    return (i,e)
        return None

    @cache
    def iterate_throug_neighbor_nondiag(node):
        nei = []
        for dir in range(0, len(x)):
            nextX = node[0] + x[dir]
            nextY = node[1] + y[dir]
            next = (nextX, nextY)
            nei.append((next, dir))
        return nei

    @cache
    def find_min_from_path(path, levels):
        if levels == 1:
            return len(path)
        curr = find_pos(0, 'A')
        result = 0
        for letter in path:
            target = find_pos(0, letter)
            result += find_min_moves_robot(0, curr, target, levels-1)
            curr = target
        return result


    @cache
    def find_min_moves_robot(pad_id, start, target, levels):

        invalid_pos = find_pos(pad_id, '')
        result = None

        queue = [(start, '')]

        while len(queue) > 0:
            curr, path = queue.pop(0)

            if curr == target:
                result = get_min(result, find_min_from_path(path + 'A', levels))
            elif curr != invalid_pos:
                for next, dir in iterate_throug_neighbor_nondiag(curr):
                    if is_on_map(next, pad_id):
                        next_path = path + keypad_moves[dir]
                        if is_dir(curr[0], target[0], x[dir]) or is_dir(curr[1], target[1], y[dir]):
                            queue.append((next, next_path))
        return result
    
    ret = 0
    for code in codes:
        curr = find_pos(1, 'A')
        result = 0
        for letter in code:
            target = find_pos(1, letter)
            result += find_min_moves_robot(1, curr, target, 26)
            curr = target
        num = int(str(digits(code)[0]))
        ret += result * num
    return ret

def digits(string):
    regex = r"(?<!\.)[0-9]+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ str(match.group(0)) for n, match in enumerate(matches, start=1)]


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
            return str(f)

        return [parse_row(row) for row in csvfile.readlines()]

m = readInput('input.txt')
print(timeit.timeit(lambda: print(solve3(m)), number=1))