def readInput():
    with open('input.txt') as csvfile:

        def sanitize(row):
            f = list(row.replace('\n', ''))
            return f

        return [ sanitize(row) for row in csvfile.readlines()]

def search2D(grid, row, col, word):
    m = len(grid)
    n = len(grid[0])

  
    if grid[row][col] != word[0]:
        return []

    lenWord = len(word)

    x = [-1, -1,  1, 1]
    y = [-1,  1, -1, 1]

    hits = []
    for dir in range(4):

        currX, currY = row + x[dir], col + y[dir]
        k = 1
        ax = None
        ay = None
        while k < lenWord:

            if currX >= m or currX < 0 or currY >= n or currY < 0:
                break

            if grid[currX][currY] != word[k]:
                break
            if grid[currX][currY] == 'A':
                ax = currX
                ay = currY
       
            currX += x[dir]
            currY += y[dir]
            k += 1

        if k == lenWord:
            hits.append((ax, ay))

    return list(dict.fromkeys(hits))


def flatten(xss):
    return [x for xs in xss for x in xs]

def searchWord(grid, word):
    m = len(grid)
    n = len(grid[0])

    ans = []

    for i in range(0, m):
        for j in range(0, n):
            res = search2D(grid, i, j, word)
            if len(res) > 0:
                ans.append(res)

    return ans

def solve_2(field):

    res = flatten(searchWord(field, 'MAS'))
    mem = dict()
    for r in res:
        if r in mem:
            mem[r] = mem[r] + 1
        else:
            mem[r] = 1
    return sum([ 1 if v > 1 else 0 for k, v in mem.items()])

inputList = readInput()

print(solve_2(inputList))