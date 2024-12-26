import copy
import timeit
import re

def print_instru(inst):

    def combo_of(operand):
        if operand <= 3:
            return operand
        else:
            return 'r' + str(operand - 4)


    opcode, operand = inst
    comp_value = combo_of(operand)
    match opcode:
            #adv
            case 0:
                print('r0 = ' + 'r0 / 2**' + str(comp_value) )
            # bxl
            case 1:
                print('r1' + ' = ' + 'r1 ^ ' + str(operand))
            # bst
            case 2:
                print('r1' + ' = '  + str(comp_value) +  ' % 8 ')
            # jnz    
            case 3:
                print('jmp to ' + str(operand) + ' if r0 != 0')
            # bxc
            case 4:
                print('r1 = r1 ^ r2')
            # out
            case 5:
                 print('print(' + str(comp_value) + '%8)')
             #  bdv  
            case 6:
                print('r1 = ' + 'r0 / 2**' + str(comp_value))
            # cdv
            case 7:
                print('r2 = ' + 'r0 / 2**' + str(comp_value))

def solve(input, part2=False):
    if part2 == False:
        return run_program1(input)
    return solve_regstA(input)

def solve_regstA(input):
    def prog(a):
        out = []
        # python code for the actual program
        while a > 0:
            partial = (a % 8) ^ 4
            out.append(((partial ^ (a >> partial)) ^ 4) % 8)
            a //= 8
        return out
    
    registers = []
    for row in input:
        if len(row) == 0:
            break
        registers.append(row[0])
    program_input = input[len(input) - 1]

    uindex = 0
    instructions = []
    while uindex + 1 < len(program_input):
        instructions.append((program_input[uindex], program_input[uindex + 1]))
        uindex += 2

    for ins in instructions:
        print_instru(ins)

    success_width = 1
    A = 1
    while success_width < 17:
        outs = prog(A)
        if outs == program_input:
            return A
        while outs[-success_width:] == program_input[-success_width:]:
            success_width += 1
            # Jump forward - keeps already correct last bits
            A *= 8
        else:
            print(str(len(outs)) + ' - ' + str( A) + ' - ' + str(outs))
            A += 1
        if A > 10000000000000000:
            return None

def run_program1(input):
    registers = []
    for row in input:
        if len(row) == 0:
            break
        registers.append(row[0])
    program_input = input[len(input) - 1]
    uindex = 0
    instructions = []
    while uindex + 1 < len(program_input):
        instructions.append((program_input[uindex], program_input[uindex + 1]))
        uindex += 2
    out = []

    ip = 0
 
    def combo_of(operand):
        if operand <= 3:
            return operand
        else:
            return registers[operand - 4]
  
    def execute_instr(inst, ip2):
        print(inst)
        print(ip2)
        opcode, operand = inst
        comp_value = combo_of(operand)
        match opcode:
            #adv
            case 0:
                numerator = registers[0]
                denominator  = 2**comp_value
                registers[0] = int(numerator // denominator)
            # bxl
            case 1:
                registers[1] = registers[1] ^ operand
            # bst
            case 2:
                registers[1] = comp_value % 8
            # jnz    
            case 3:
                if registers[0] != 0:
                    ip2 = operand - 1
            # bxc
            case 4:
                registers[1] = registers[1] ^ registers[2]
            # out
            case 5:
                 out.append(comp_value % 8)
             #  bdv  
            case 6:
                numerator = registers[0]
                denominator  = 2**comp_value
                registers[1] = int(numerator // denominator)
            # cdv
            case 7:
                numerator = registers[0]
                denominator  = 2**comp_value
                registers[2] = int(numerator // denominator)
        return ip2
    while ip < len(instructions):
        ip = execute_instr(instructions[ip], ip)
        ip += 1
    return ','.join([str(o) for o in out])

def ints(string):
    regex = r"(?<!\.)\d+(?!\.)"
    matches = re.finditer(regex, string, re.MULTILINE)

    return [ int(match.group(0)) for n, match in enumerate(matches, start=1)]

def readInput():
    with open('input.txt') as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            return ints(f)

        rows = [ sanitize(row) for row in csvfile.readlines()]
        return rows

m = readInput()

print(timeit.timeit(lambda: print(solve(m, False)), number=1))
print(timeit.timeit(lambda: print(solve(m, True)), number=1))