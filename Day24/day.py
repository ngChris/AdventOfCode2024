from collections import defaultdict
import copy
from functools import cache, lru_cache
from heapq import heappop, heappush
from itertools import groupby
from math import floor, log10
import timeit
from typing import Callable, Iterable, Any, Dict, Optional
import re
import numpy as np

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

def get_numbers(state):
    x = ''
    y = ''
    for c in sorted(state, reverse=True):
        if c.startswith('x'):
            x += str(state[c])
        elif c.startswith('y'):
            y += str(state[c])
    
    return int(x, 2), int(y, 2)

def get_bit(x, n):
    return 1 if is_set(x,n) else 0

def is_set(x, n):
    return x & 2 ** n != 0 

    # a more bitwise- and performance-friendly version:
    #return x & 1 << n != 0

def solve1(initial_wires, gates,part2=False):
    state = {x[0]:x[1] for x in initial_wires}
    number1, number2 = get_numbers(state)
    goal = number1 + number2
    print(goal)

    gate_map = defaultdict(list)
    for g in gates:
       gate_map[g[0]].append(g)
       gate_map[g[2]].append(g)
     
    def find_and_expect(wire1, wire2, operator):
        for wg in gate_map[wire1]:
            if wg[0] in [wire1, wire2] and wg[2] in [wire1, wire2] and wg[1] == operator:
                return wg[3]
        return None

    invalid_bits = []

    def check_bit(bit, in_c):
        key = str(bit).zfill(2)
        xkey = 'x' + key
        ykey = 'y' + key
        zkey = 'z' + key
        node1 = find_and_expect(xkey, ykey, 'XOR')
        if node1 == None:
            invalid_bits.append((bit, 'node1'))
        node2 = find_and_expect(xkey, ykey, 'AND')
        if node2 == None:
            invalid_bits.append((bit, 'node2'))
        if node1 != None and in_c != None:
            node3 = find_and_expect(node1, in_c, 'XOR')
            if node3 != zkey:
                invalid_bits.append((bit, 'node3 - misses ' + node1 + ' XOR ' + in_c + ' = '))
                #check node 2
            node4 = find_and_expect(node1, in_c, 'AND')
            if node4 == None:
                invalid_bits.append((bit, 'node4 - misses ' + node1 + ' AND ' + in_c))
            if node4 != None and node2 != None:
                node5 = find_and_expect(node2, node4, 'OR')
                if node5 == None:
                    invalid_bits.append((bit, 'node5 - misses ' + node2 + ' OR ' + node4))
                return node5
        elif node2 != None:
            return node2
        return None

    c = None
    for bit in range(0, 45):
        c= check_bit(bit, c)

    print(invalid_bits)
    calculated, zwires = process_gates(state, gates)
    wrong_z = []
    for zwire in zwires:
    
        index = ints(zwire)[0]
        if is_set(goal, index) != is_set(calculated, index):
            wrong_z.append(zwire)

    print(wrong_z)
    return calculated, zwire
    
def process_gates(state, gates):

    ready_gates = []
    waiting_gates = defaultdict(list)
    gate_map = defaultdict(list)
    for g in gates:
       gate_map[g[0]].append(g)
       gate_map[g[2]].append(g)
       if g[0] in state and g[2] in state:
           ready_gates.append(g)
       else:
            waiting_gates[g[0]].append(g)
            waiting_gates[g[2]].append(g)
    
    while len(ready_gates) > 0:
        gate = ready_gates.pop()

        wire1_val = state[gate[0]]
        wire2_val = state[gate[2]]

        result = None
        if gate[1] == 'AND':
            result = wire1_val & wire2_val
        elif gate[1] == 'OR':
            result = wire1_val | wire2_val
        else:
            result = wire1_val ^ wire2_val
        
        target_wire = gate[3]
        state[target_wire] = result
        if target_wire in waiting_gates:
            for wg in list(waiting_gates[target_wire]):
                if wg[0] in state and wg[2] in state:
                    ready_gates.append(wg)
                    waiting_gates[wg[0]].remove(wg)
                    waiting_gates[wg[2]].remove(wg)

    n = ''
    zwires = []
    for wire in sorted(state, reverse=True):
        if wire.startswith('z'):
            n += str(state[wire])
            zwires.append(wire)
    return int(n, 2), zwires
 
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
    with open(filename) as file:

        parts = file.read().split('\n\n')

        def wire(input):
            x = input.split(':')
            return (x[0], int(x[1].strip()))

        initial_wires = [wire(x) for x in parts[0].split('\n')]

        def gate(input):
            x = input.split(' ')
            return (x[0], x[1], x[2], x[4])

        gates = [gate(x) for x in parts[1].split('\n')]

        return initial_wires, gates

m,g = readInput('input.txt')

print(timeit.timeit(lambda: print(solve1(m, g)), number=1))