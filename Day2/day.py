import csv

def readInput():
    list = []
    with open('input.txt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|', skipinitialspace=True)
        for row in spamreader:
            list.append(row)
    return list


def solve_2(rows):

    def is_valid(report):
        expectedSortOrder = 'DESC' if report[0] < report[1] else 'ASC'
        for i in range(0, len(report) - 1):
              sortOrder = 'DESC' if report[i] < report[i+1] else 'ASC'
              if sortOrder != expectedSortOrder:
                  return i
              diff = abs(report[i] - report[i+1])
              if diff <= 0 or diff > 3:
                  return i
        return -1
    def is_valid_with_retry(index):
        report = [int(s) for s in rows[index]]
        res = is_valid(report)
        if res == -1:
            return 1
        for restart_index in range(0, len(rows[index])):
            report = [int(s) for s in rows[index]]
            del report[restart_index]
            res = is_valid(report)
            if(res == -1):
                return 1
        return 0

    return sum([is_valid_with_retry(i) for i in range(0, len(rows)) ])


inputList = readInput()

print(solve_2(inputList))