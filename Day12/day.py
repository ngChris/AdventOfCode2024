import timeit

def solve(maze, part2=False):
    visited_loc = set()
    m = len(maze)
    n = len(maze[0])

    def is_on_map(node):
        return (node[0] >= m or node[0] < 0 or node[1] >= n or node[1] < 0) == False

    def visit(node):
        visited_loc.add(node)
        currX, currY = node[0], node[1]
        perimeter = 0
        checkC = False
        corner = 0
        area = 1
        x = [-1, 0,  1, 0]
        y = [0,  1, 0, -1]
        c = [0,0,0,0]
        dirs = [ (-1, -1), (-1, 0), (-1, 1),   ( 0, 1), ( 1, 1), ( 1, 0),   ( 1, -1), ( 0, -1)]

        for dir in range(0, len(x)):
            nextX = currX + x[dir]
            nextY = currY + y[dir]
            next = (nextX, nextY)
            if is_on_map(next):
                if maze[nextX][nextY] == maze[currX][currY]:
                    if next not in visited_loc:
                        nextPeri, nextArea, nextC = visit(next)
                        perimeter += nextPeri
                        area += nextArea
                        corner += nextC
                    checkC = False
                    c[dir] = 0
                else:
                    perimeter += 1
                    if(checkC == True):
                        corner += 1
                    checkC = True
                    c[dir] = 1
                 
            else:
                perimeter += 1
                if(checkC == True):
                    corner += 1
                checkC = True
                c[dir] = 1
        if c[0] == 1 and c[3] == 1:
            corner += 1

        d = 0
        while d < 8:
            nextX = currX + dirs[d%8][0]
            nextY = currY + dirs[d%8][1]
            next = (nextX, nextY)
            if is_on_map(next):
                if maze[nextX][nextY] != maze[currX][currY]:
            
                    if maze[currX + dirs[(d-1) % 8][0]][currY + dirs[(d-1) % 8][1]] == maze[currX][currY] and maze[currX + dirs[(d+1) % 8][0]][currY + dirs[(d+1) % 8][1]] == maze[currX][currY]:
                        corner += 1
            d += 2

        return perimeter, area, corner
    
    found = []
    for i in range(0, m):
        for j in range(0, n):
            if (i,j) not in visited_loc: 
             p, a, s = visit((i,j))
             found.append(s*a)
                 
    return sum(found)


def readInput(filename):
    with open(filename) as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            return list(f)

        rows = [ sanitize(row) for row in csvfile.readlines()]
        return rows

m = readInput('input.txt')

print(timeit.timeit(lambda: print(solve(m, True)), number=1))