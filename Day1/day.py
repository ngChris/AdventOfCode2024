import csv

def readInput():
    list = []
    with open('input.txt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|', skipinitialspace=True)
        for row in spamreader:
            list.append(row)
    return list

def distance_list(rows):
    listA = sorted([int(r[0]) for r in rows])
    listB = sorted([int(r[1]) for r in rows])

    return sum([abs(listA[i] - listB[i]) for i in range(0, len(listA)) ])


def solve_2(rows):
    listA = sorted([int(r[0]) for r in rows])
    listB = sorted([int(r[1]) for r in rows])

    mem = {}

    def count(index):
        valA = listA[index]
        if valA in mem:
            return mem.get(valA)
        else:
            occurs = listB.count(valA)
            mem[valA] = valA * occurs
            return mem[valA]

    return sum([count(i) for i in range(0, len(listA)) ])


inputList = readInput()

print(solve_2(inputList))