import timeit
import re

def to_pin_heigts(key, symbol):
    m = len(key)
    n = len(key[0])
    pin = [0,0,0,0,0]
    for i in range(0, n):
        for e in range(1, m-1):
            if key[e][i] == symbol:
                pin[i] += 1
    return pin

def overlap(kpin, lpin):
    for i in range(0, len(kpin)):
        if kpin[i] + lpin[i] >= 6:
            return True
    return False

def solve1(keys, locks,part2=False):
    lock_pins = [to_pin_heigts(l, '#') for l in locks]
    key_pins = [to_pin_heigts(k, '#') for k in keys]
    
    count = 0
    for lock_pin in lock_pins:
        for key_pin in key_pins:
            if overlap(key_pin, lock_pin) == False:
                count += 1


    return count
 
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

        keys = []
        locks = []

        for part in file.read().split('\n\n'):
            rows = part.split('\n')
            if rows[0].startswith('#'):
                locks.append(list(rows))
            else:
                keys.append(list(rows))
        return keys, locks

m,g = readInput('input.txt')

print(timeit.timeit(lambda: print(solve1(m, g)), number=1))