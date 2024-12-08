import re

def readInput():
    with open('input.txt') as csvfile:
        return csvfile.read()


def solve_2(test_str):
    regex = r"mul\(\d+,\d+\)|don't\(\)|do\(\)"
    matches = re.finditer(regex, test_str, re.MULTILINE)

    m = []
    enabled = True
    for matchNum, match in enumerate(matches, start=1):
    
        if str(match.group()) == "do()":
            enabled = True
        elif str(match.group()) == "don't()":
            enabled = False
        else:
            if enabled:
                matchNumbers = [ int(d) for d in re.findall(r"\d+", match.group())]
                m.append(matchNumbers[0] * matchNumbers[1])
    return sum(m)

inputList = readInput()

print(solve_2(inputList))