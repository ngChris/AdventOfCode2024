import copy
from heapq import heappop, heappush
import timeit

def solve(corruptions, part=False):
    min_path = set()
    # going backwards is faster
    for i in range(len(corruptions)-1, 0, -1):
            min_path = find_byte(corruptions, i)
            if min_path != None:
                return corruptions[i]
    return None

def find_byte(corruptions, start_corr):
    m = 71
    n = m

    def is_on_map(node):
        return (node[0] >= m or node[0] < 0 or node[1] >= n or node[1] < 0) == False
    
    def iterate_throug_neighbor_nondiag(node):
        x = [-1, 0, 0, 1]
        y = [ 0,-1, 1, 0]
        nei = []
        for dir in range(0, len(x)):
            nextX = node[0] + x[dir]
            nextY = node[1] + y[dir]
            next = (nextX, nextY)
            nei.append(next)
        return nei
    
    visited_loc = dict()
    queue = [(0, (0,0), set())]
    goal = (m-1, n - 1)

    while len(queue) > 0:
        steps, curr, path = heappop(queue)
      
        if curr in visited_loc and visited_loc[curr] <= steps:
            continue
        visited_loc[curr] = steps
        path = copy.copy(path)
        path.add(curr)
        if goal == curr:
            return path

        nei = iterate_throug_neighbor_nondiag(curr)

        def canVisit(node):
            return is_on_map(node) and node not in corruptions[:start_corr]

        walkable = filter(canVisit, nei)
       
        for w in walkable:
            heappush(queue, (steps + 1, w, path))
          
    return None
    

def ints(string):
    regex = r"(?<!\.)\d+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ int(match.group(0)) for n, match in enumerate(matches, start=1)]

def readInput():
    with open('input.txt') as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            u = ints(f)

            return (u[0], u[1])

        rows = [ sanitize(row) for row in csvfile.readlines()]
        return rows

m = readInput()
print(timeit.timeit(lambda: print(solve(m, True)), number=1))