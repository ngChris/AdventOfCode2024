from itertools import groupby
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


def solve(block_input, part2=False):

    def generate_files():
        id = 0
        blocks = []
        first_free_block_pos = -1
        for i in range(0, len(block_input)):
            if i % 2 == 0:
                repeats = block_input[i]
                for k in range(0, repeats):
                    blocks.append(id)
                id += 1
            else:
                if first_free_block_pos == -1:
                    first_free_block_pos = len(blocks)
                repeats = block_input[i]
                for k in range(0, repeats):
                    blocks.append('.')
        return blocks, first_free_block_pos
    
    blocks, first_free_block_pos = generate_files()

    def swap(i, j):
        blocks[i] , blocks[j] = blocks[j] , blocks[i]

    if part2 == False:
        for i in reversed(range(0, len(blocks))):
            if blocks[i] != '.':
                if(first_free_block_pos < i):
                    swap(first_free_block_pos, i)
                    for k in range(first_free_block_pos, len(blocks)):
                        if blocks[k] == '.':
                            first_free_block_pos = k
                            break
    else:
        def next_block(pos):
            id = blocks[pos]
            while blocks[pos] == id and pos >= 0:
                pos -= 1
            return pos + 1
        curr_i = len(blocks) - 1

        def find_next_free(size):
            for i in range(0, len(blocks)):
                if blocks[i] == '.':
                    count = 0
                    for e in range(i, len(blocks)):
                        if blocks[e] == '.' and count < size:
                            count += 1
                        else:
                            break
                    if count == size:
                        return i
            return -1

        while curr_i >= 0 :

            if blocks[curr_i] != '.':
                start_pos = next_block(curr_i)
                size = curr_i - start_pos + 1
                start_free = find_next_free(size)
                if start_free > 0 and start_free < start_pos:
                    for i in range(0, size):
                        swap(start_free + i, start_pos + i)   
                curr_i -= size
        
            else:     
                curr_i -= 1     

    checksum = 0
    for i in range(0, len(blocks)):
        if(blocks[i] != '.'):
            checksum += blocks[i] * i
    return checksum
            


def readInput():
    with open('input.txt') as csvfile:


        return [int(x) for x in list(csvfile.readlines()[0])]

m = readInput()

print(solve(m, True))