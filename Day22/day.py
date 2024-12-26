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

def mix(number, secret):
    return number ^ secret

def prune(number):
    return number % 16777216

def mix_prune(number, secret):
    m = mix(number, secret)
    return prune(m)

def process(secret):
    m1 = mix_prune(secret * 64, secret)
    m2 = mix_prune(m1//32, m1)
    m3 = mix_prune(m2*2048, m2)
    return m3        

def solve_secret(initial_secret):
    current_secret = initial_secret
    
    for i in range(0, 2000):
        current_secret = process(current_secret)
    return current_secret

def get_digit(secret):
    return secret % 10


def get_digits(initial_secret):
    current_secret = initial_secret
    seq = []
    for i in range(0, 2000):
        last_secret_digit = get_digit(current_secret)
        current_secret = process(current_secret)
        new_scret_digit = get_digit(current_secret)
        seq.append((new_scret_digit, new_scret_digit - last_secret_digit))
    return seq

def solve2(initial_secrets,part2=False):
    total_sequences = dict()
    for secret in initial_secrets:
        seq_t = get_digits(secret)
        seq = [t[1] for t in seq_t]
        seq_n = [t[0] for t in seq_t]
        already_seen = set()
        for i in range(0, len(seq) - 4):
            s = tuple(seq[i:i+4])
            if s in already_seen:
                continue
            already_seen.add(s)
            if s in total_sequences:
                total_sequences[s] = total_sequences[s] + seq_n[i+3]
            else:
                total_sequences[s] = seq_n[i+3]

    return max(total_sequences.values())

def solve1(initial_secrets,part2=False):
    solutions = []
    for secret in initial_secrets:
        solutions.append(solve_secret(secret))
    return sum(solutions)

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
            return ints(f)[0]

        return [parse_row(row) for row in csvfile.readlines()]

m = readInput('input.txt')
print(timeit.timeit(lambda: print(solve2(m)), number=1))