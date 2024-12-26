import timeit
import re
import numpy as np

def evaluate_cost(presses):
    return presses[0] * 3 + presses[1]

def solve_eq(eq, part2):
    button_a = eq[0]
    button_b = eq[1]
    target = eq[2]
    target[0] += 10000000000000 if part2 else 0
    target[1] += 10000000000000 if part2 else 0

    nx = np.linalg.solve(np.stack((button_a, button_b)).T, target)
    is_integral = all(np.abs(np.round(nx) - nx) < 1e-3)
    if is_integral:
        return evaluate_cost((nx[0], nx[1]))
    
    return None
        

def solve(eqList, part2=False):
    equations = toEquFormat(eqList)
  
    res = [solve_eq(e, part2) for e in equations]
  
    return sum(filter(lambda x: x != None, res))

def ints(string):
    regex = r"(?<!\.)\d+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ int(match.group(0)) for n, match in enumerate(matches, start=1)]

def toEquFormat(eqS):
    eqList = []
    cur = []
    for i in range(0, len(eqS)):
        if len(eqS[i]) > 0:
            cur.append(eqS[i])
        else:
            eqList.append(cur)
            cur = []
    if len(cur) > 0:
        eqList.append(cur)
    return eqList

def readInput(filename):
    with open(filename) as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            
            return ints(f)

        rows = [ sanitize(row) for row in csvfile.readlines()]
        return rows

m = readInput('input.txt')

print(timeit.timeit(lambda: print(solve(m, True)), number=1))