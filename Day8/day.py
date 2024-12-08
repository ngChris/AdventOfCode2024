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


def get_freq(maze):
    feq = dict()
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] != '.':
                if maze[i][j] in feq:
                    feq[maze[i][j]].append((i,j))
                else:
                    feq[maze[i][j]] = [(i,j)]
    return feq

def solve_maze_1(maze):
    m = len(maze)
    n = len(maze[0])
    feq_map = get_freq(maze)

    maze_antinodes = copy.deepcopy(maze)

    def get_dist(a1, a2):
       return (a1[0] - a2[0], a1[1]- a2[1]) 
    
    def add_node(a1, a2):
        return (a1[0] + a2[0], a1[1] + a2[1]) 
    
    def sub_node(a1, a2):
        return (a1[0] - a2[0], a1[1] - a2[1]) 
    
    def is_on_map(node):
        return (node[0] >= m or node[0] < 0 or node[1] >= n or node[1] < 0) == False

    for fq, v in feq_map.items():
        for i in range(0, len(v)):
            for e in range(i + 1, len(v)):
                dist = get_dist(v[i], v[e])
                anti_node_loc1 = add_node(v[i], dist)
                anti_node_loc2 = sub_node(v[e], dist)
                if is_on_map(anti_node_loc1):
                    maze_antinodes[anti_node_loc1[0]][anti_node_loc1[1]] = '#'
                if is_on_map(anti_node_loc2):
                    maze_antinodes[anti_node_loc2[0]][anti_node_loc2[1]] = '#'    

    def print_anti_nodes():
        s = ''
        for i in range(0, m):
            row = maze_antinodes[i]
            s = s + ''.join(row) + '\n'
        print(s)
        print('   ')
    print_anti_nodes()

    count = 0
    for i in range(0, m):
        for e in range(0, n):
            if maze_antinodes[i][e] == '#':
                count = count + 1

    return count

def solve_maze_2(maze):
    m = len(maze)
    n = len(maze[0])
    feq_map = get_freq(maze)

    maze_antinodes = copy.deepcopy(maze)

    def get_dist(a1, a2):
       return (a1[0] - a2[0], a1[1]- a2[1]) 
    
    def add_node(a1, a2):
        return (a1[0] + a2[0], a1[1] + a2[1]) 
    
    def sub_node(a1, a2):
        return (a1[0] - a2[0], a1[1] - a2[1]) 
    
    def is_on_map(node):
        return (node[0] >= m or node[0] < 0 or node[1] >= n or node[1] < 0) == False

    for fq, v in feq_map.items():
        for i in range(0, len(v)):
            for e in range(i + 1, len(v)):
                dist = get_dist(v[i], v[e])
                anti_node_loc1 = add_node(v[i], dist)
                anti_node_loc2 = sub_node(v[i], dist)
                maze_antinodes[v[i][0]][v[i][1]] = '#'
                while(is_on_map(anti_node_loc1)):
                    maze_antinodes[anti_node_loc1[0]][anti_node_loc1[1]] = '#'
                    anti_node_loc1 = add_node(anti_node_loc1, dist)
                while(is_on_map(anti_node_loc2)):
                    maze_antinodes[anti_node_loc2[0]][anti_node_loc2[1]] = '#'    
                    anti_node_loc2 = sub_node(anti_node_loc2, dist) 

    def print_anti_nodes():
        s = ''
        for i in range(0, m):
            row = maze_antinodes[i]
            s = s + ''.join(row) + '\n'
        print(s)
        print('   ')
    print_anti_nodes()

    count = 0
    for i in range(0, m):
        for e in range(0, n):
            if maze_antinodes[i][e] == '#':
                count = count + 1

    return count
                

def readInput():
    with open('input.txt') as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            return list(f)

        rows = [ sanitize(row) for row in csvfile.readlines()]
        return rows

m = readInput()

print(solve_maze_2(m))