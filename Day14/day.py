import timeit
import re
import numpy as np

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# crt 
def find_min_x(num, rem):
    prod = 1
    for n in num:
        prod *= n

    result = 0
    for i in range(len(num)):
        prod_i = prod // num[i]
        _, inv_i, _ = gcd_extended(prod_i, num[i])
        result += rem[i] * prod_i * inv_i

    return result % prod        

def solve(robots, part2=False):
    m = 101
    n = 103

    def move_forward(robot):
        currX = robot[0]
        currY = robot[1]
        x = robot[2]
        y = robot[3]
        nextX = (currX + x) % m
        nextY = (currY + y) % n
        robot[0] = nextX
        robot[1] = nextY

    var1 = []
    var2 = []
    xi = None
    yi = None
    for i in range(0, max(m,n)):
        xa = [r[0] for r in robots]
        ya = [r[1] for r in robots]
        var1.append(np.var(xa))
        var2.append(np.var(ya))
        if np.var(xa) < 400:
            xi = i
        if np.var(ya) < 400:
            yi = i
    
        for robot in robots:
            move_forward(robot)
    return find_min_x([101, 103], [xi, yi])

def ints(string):
    regex = r"(?<!\.)-?\d+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ int(match.group(0)) for n, match in enumerate(matches, start=1)]


def readInput(filename):
    with open(filename) as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            
            robot = ints(f)
            return robot

        rows = [ sanitize(row) for row in csvfile.readlines()]
        return rows

m = readInput('input.txt')

print(timeit.timeit(lambda: print(solve(m, True)), number=1))