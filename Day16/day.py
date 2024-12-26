from heapq import heappop, heappush
import timeit
import re


def print_maze(m):
        s = ''
        for i in range(0, len(m)):
            s += ''.join(m[i]) + '\n'
        print(s)            

def solve(maze, part2=False):
    m = len(maze)
    n = len(maze[0])

    x = [-1, 0,  1, 0]
    y = [0,  1, 0, -1]

    def is_on_map(node):
        return (node[0] >= m or node[0] < 0 or node[1] >= n or node[1] < 0) == False

    curr = None
  
    target = None
    for i in range(0,m):
        for e in range(0, n):
            if maze[i][e] == 'S':
                curr = (i,e)
            if maze[i][e] == 'E':
                target = (i,e)
    visited_loc = dict()
    queue = [(0, curr, 1, {curr})]
    solutions = set()
    minSolution = 100000000000000000000
    while len(queue) > 0:
         cost, curr, dir, tiles = heappop(queue)
         if minSolution < cost:
             continue
         if curr == target:
            if minSolution >= cost:
                minSolution = cost
                solutions |= tiles

         if (curr, dir) in visited_loc and visited_loc[(curr, dir)] < cost:
            continue
         visited_loc[(curr, dir)] = cost

         nextX = curr[0] + x[dir]
         nextY = curr[1] + y[dir]
         next = (nextX, nextY)
         if is_on_map(next) and maze[nextX][nextY] != '#':
             heappush(queue, (cost + 1 , next, dir, tiles | {next}))
         heappush(queue, (cost + 1000 , curr, (dir - 1) % 4, tiles))
         heappush(queue, (cost + 1000 , curr, (dir + 1) % 4, tiles))
 
    return len(solutions)

def ints(string):
    regex = r"(?<!\.)-?\d+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ int(match.group(0)) for n, match in enumerate(matches, start=1)]


def readInput(filename):
    with open(filename) as csvfile:

        def parse_row(row):
            f = row.replace('\n', '')
            return list(f)

        return [parse_row(row) for row in csvfile.readlines()]

m = readInput('input.txt')
print(timeit.timeit(lambda: print(solve(m, True)), number=1))