from functools import cache
import timeit
import re

def solve(patterns, towels, part=False):
    return sum([is_possible(patterns, t) for t in towels])


def is_possible(patterns, towel):

    possible_patterns = list(filter(lambda x : x in towel, patterns))

    @cache
    def is_possible_rek(curr):
        if curr == '':
            return 1
        count = 0
        for p in possible_patterns:
            if curr.startswith(p):
                possible = is_possible_rek(curr[len(p):])
                count += possible
        return count

    return is_possible_rek(towel)
    
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

        input = csvfile.read().split('\n\n')

        patterns = input[0].split(', ')
        #print(patterns)

        return patterns, [str(row.replace('\n', '')) for row in input[1].split('\n')]

m, s = readInput('input.txt')
print(timeit.timeit(lambda: print(solve(m, s, True)), number=1))