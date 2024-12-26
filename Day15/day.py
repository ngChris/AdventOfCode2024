import timeit
import re

def flatten(xss):
    return [x for xs in xss for x in xs]


def solve(input, part2=False):
    maze, movements = input

    m = len(maze)
    n = len(maze[0])

    x = [-1, 0,  1, 0]
    y = [0,  1, 0, -1]

    move_map = {'^': 0, '>': 1, 'v': 2, '<': 3}

    def is_on_map(node):
        return (node[0] >= m or node[0] < 0 or node[1] >= n or node[1] < 0) == False
    
    def try_move(node, dir, testOnly=False):

        name = maze[node[0]][node[1]]
        nextX = node[0] + x[dir]
        nextY = node[1] + y[dir]
        next = (nextX, nextY)
        if is_on_map(next):
            if maze[nextX][nextY] == '.':
                if testOnly == False:
                    maze[nextX][nextY] = name
                    maze[node[0]][node[1]] = '.'
                return next
            if maze[nextX][nextY] in ['[',']']:
                if dir == 0 or dir == 2:
                    otherNext = (nextX, nextY + 1) if maze[nextX][nextY] == '[' else (nextX, nextY - 1)
                    res = try_move(next, dir, True)
                    resOther = try_move(otherNext, dir, True)
                    if res != next and resOther != otherNext:
                        if testOnly == False:
                            try_move(next, dir, testOnly)   
                            try_move(otherNext, dir, testOnly) 
                            maze[nextX][nextY] = name
                            maze[node[0]][node[1]] = '.'
                        return next
                else:
                    res = try_move(next, dir, testOnly)
                    if res != next:
                        maze[nextX][nextY] = name
                        maze[node[0]][node[1]] = '.'
                        return next
                    return node
        return node   

    curr = None
    for i in range(0,m):
        for e in range(0, n):
            if maze[i][e] == '@':
                curr = (i,e)
    
    stop = 0
    for move in movements:
        dir = move_map[move]
        curr = try_move(curr, dir)
   
        stop += 1

    sum = 0
    for i in range(0, m):
        for e in range(0, n):
            if maze[i][e] == '[':
                sum += (100 * i) + e
    
    return sum

def ints(string):
    regex = r"(?<!\.)-?\d+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ int(match.group(0)) for n, match in enumerate(matches, start=1)]


def readInput(filename):
    with open(filename) as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            f = f.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
            return list(f)

        maze = []
        movements = []
        for row in csvfile.readlines():
            if row.startswith('#'):
                maze.append(sanitize(row))
            elif '<' in row or '^' in row or '>' in row or 'v' in row:
                movements.append(sanitize(row))
        movements = flatten(movements)
        return (maze, movements)

m = readInput('input.txt')
print(timeit.timeit(lambda: print(solve(m, True)), number=1))