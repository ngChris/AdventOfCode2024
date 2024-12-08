from itertools import groupby
from typing import Callable, Iterable, Any, Dict, Optional
import copy

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

def search_start(maze):
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == '^':
                return i, j

def solve_1(maze):
    return len(walk_maze(maze))

def walk_maze(maze):
    m = len(maze)
    n = len(maze[0])
    currX, currY = search_start(maze)
    dir = 0
    x = [-1, 0,  1, 0]
    y = [0,  1, 0, -1]

    visited_loc = set()

    while (currX >= m or currX < 0 or currY >= n or currY < 0) == False:

        nextX = currX + x[dir]
        nextY = currY + y[dir]

        if (nextX >= m or nextX < 0 or nextY >= n or nextY < 0) == False:
            while maze[nextX][nextY] == '#':
                dir = (dir + 1) % 4
                nextX = currX + x[dir]
                nextY = currY + y[dir]
        
        if not (currX, currY) in visited_loc:
            visited_loc.add((currX, currY))
        
        currX = currX + x[dir]
        currY = currY + y[dir]

    return visited_loc

def solve_2(maze):
    solutions = 0
    paths = walk_maze(maze)
    for p in paths:
        maze_p = copy.deepcopy(maze)
        i = p[0]
        j = p[1]
        if maze_p[i][j] == '.':
           maze_p[i][j] = 'O'
           if find_loops(maze_p) == True:
            solutions = solutions + 1
    return solutions

def find_loops(maze):
    m = len(maze)
    n = len(maze[0])
    currX, currY = search_start(maze)
    dir = 0
    x = [-1, 0,  1, 0]
    y = [0,  1, 0, -1]
    dir_sign = ['|', '-', '|', '-']

    visited_loc = dict()

    while (currX >= m or currX < 0 or currY >= n or currY < 0) == False:

        nextX = currX + x[dir]
        nextY = currY + y[dir]

        if (nextX >= m or nextX < 0 or nextY >= n or nextY < 0) == False:
            while maze[nextX][nextY] == '#' or maze[nextX][nextY] == 'O':
                dir = (dir + 1) % 4
                nextX = currX + x[dir]
                nextY = currY + y[dir]

        if (nextX >= m or nextX < 0 or nextY >= n or nextY < 0) == False:
            if maze[currX][currY] == '.':
                maze[currX][currY] = dir_sign[dir]
            elif maze[currX][currY] == '|' or maze[currX][currY] == '-':
                maze[currX][currY] = '+'
        
        if (currX, currY) in visited_loc:
            if dir in visited_loc[(currX, currY)]:
                return True
            visited_loc[(currX, currY)].append(dir)
        else:
            visited_loc[(currX, currY)] = [dir]
        
        currX = currX + x[dir]
        currY = currY + y[dir]

    return False


def readInput():
    with open('input.txt') as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            return list(f)

        rows = [ sanitize(row) for row in csvfile.readlines()]
        return rows

m = readInput()

print(solve_2(m))