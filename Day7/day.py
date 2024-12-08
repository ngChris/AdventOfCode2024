from itertools import groupby
from typing import Callable, Iterable, Any, Dict, Optional
import copy
from collections import deque
from itertools import product

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

def try_solve_equation_with_rek_tree(equation):
    target = equation[0]
    operands = equation[1]
    n = len(operands)

    def solve_rek(index, sum):
        if target < sum:
            return False
        if index == n and target == sum:
            return True
        if index < n:
            return solve_rek(index + 1, sum + operands[index]) == True or solve_rek(index + 1, sum * operands[index]) == True or solve_rek(index + 1, int(str(sum) + str(operands[index]))) == True
        return False
    
    return solve_rek(0, 0)

def solve_2(equations):
    count = 0
    for eq in equations:
        if try_solve_equation_with_rek_tree(eq) == True:
            count = count + eq[0]
    return count

def readInput():
    with open('input.txt') as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            l = f.split(':')

            return  [int(l[0]), [int(x) for x in list(filter(lambda x : x != ' ' and x != '', l[1].split(' ')))]]

        rows = [ sanitize(row) for row in csvfile.readlines()]
        return rows

m = readInput()

print(solve_2(m))