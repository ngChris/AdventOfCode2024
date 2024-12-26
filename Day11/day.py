from functools import cache
from itertools import groupby
from math import floor, log10
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

@cache
def digits(num):
    return floor(log10(num)) + 1

@cache
def blink_stone(stone, it):
    if it == 75:
        return 1
    if stone == 0:
           return blink_stone(1, it + 1)
    else:
        num_digits = floor(log10(stone)) + 1
        if num_digits % 2 == 0:
            n = int(num_digits/2)
            a = int(str(stone)[:n])
            b = int(str(stone)[n:])
            return blink_stone(a, it + 1) + blink_stone(b, it + 1)
        else:
            return blink_stone(stone * 2024, it + 1)

def solve(stones, part2=False):
    return sum([blink_stone(s, 0) for s in stones])


def readInput(filename):
    with open(filename) as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            return [int(x) for x in f.split(' ')]

        rows = [ sanitize(row) for row in csvfile.readlines()]
        return rows[0]

m = readInput('input.txt')

print(timeit.timeit(lambda: print(solve(m, True)), number=1))