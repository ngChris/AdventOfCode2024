import csv
from itertools import groupby
import math

def flatten(xss):
    return [x for xs in xss for x in xs]

def group_by(data, key_func):
    """
    Groups items in `data` by the value returned by `key_func`.
    
    Parameters:
    - data: Iterable of items to be grouped.
    - key_func: Function to extract the grouping key from each item.
    
    Returns:
    - A dictionary where keys are the grouping values and values are lists of items in each group.
    """
    # Sort data by key_func to ensure groupby works correctly
    sorted_data = sorted(data, key=key_func)
    
    # Use groupby to group the data
    grouped_data = {
        key: list(group) for key, group in groupby(sorted_data, key=key_func)
    }
    
    return grouped_data

def solve_1(rules_rows, pages_rows):


    rules_dict = group_by(rules_rows, lambda x: x[0])
    for r in rules_dict:
        rules_dict[r] = [ b[1] for b in rules_dict[r]]


    def is_valid_row(page_row):

        m = len(page_row)

        def check_pages(i):
            val_i = page_row[i]
            for j in range(0, m):
                if i != j:
                    val_j = page_row[j]
                    if val_j in rules_dict:
                        j_afters = rules_dict[val_j]
                        if val_i in j_afters:
                            if i < j:
                                return False
            return True

        for i in range(0, m):
            if check_pages(i) == False:
                return False
                
        return True
    
    def get_middle_page(page_row):
        m = math.ceil(len(page_row) / 2)
        return page_row[m-1]

    
    valid_pages = list(filter(is_valid_row, pages_rows))

    middle_pages_numbers = [ get_middle_page(v) for v in valid_pages]

    return sum(middle_pages_numbers)

def solve_2(rules_rows, pages_rows):


    rules_dict = group_by(rules_rows, lambda x: x[0])
    for r in rules_dict:
        rules_dict[r] = [ b[1] for b in rules_dict[r]]


    def is_invalid_row(page_row):

        m = len(page_row)

        def check_pages(i):
            val_i = page_row[i]
            for j in range(0, m):
                if i != j:
                    val_j = page_row[j]
                    if val_j in rules_dict:
                        j_afters = rules_dict[val_j]
                        if val_i in j_afters:
                            if i < j:
                                return True
            return False

        for i in range(0, m):
            if check_pages(i) == True:
                return True
                
        return False
    
    def get_middle_page(page_row):
        m = math.ceil(len(page_row) / 2)
        return page_row[m-1]
    
    def fix_invalid_page(page_row):

        m = len(page_row)

        def swap(i,j):
            page_row[i], page_row[j] = page_row[j], page_row[i]

        def fix_page(i):
            val_i = page_row[i]
            for j in range(0, m):
                if i != j:
                    val_j = page_row[j]
                    if val_j in rules_dict:
                        j_afters = rules_dict[val_j]
                        if val_i in j_afters:
                            if i < j:
                                swap(i,j)
                                return True
            return False

        def try_fixing():
            for i in range(0, m):
                if fix_page(i) == True:
                    return True
            return False
        
        while try_fixing():
            None
                
        return page_row
    
    invalid_valid_pages = list(filter(is_invalid_row, pages_rows))

    invalid_valid_pages_fixed = [fix_invalid_page(v) for v in invalid_valid_pages]

    middle_pages_numbers = [ get_middle_page(v) for v in invalid_valid_pages_fixed]

    return sum(middle_pages_numbers)


def readInput():
    with open('input.txt') as csvfile:

        def sanitize(row):
            f = row.replace('\n', '')
            return f

        rows = [ sanitize(row) for row in csvfile.readlines()]
        rules_rows = []
        pages_rows = []
        for r in rows:
            if '|' in r:
                rules_rows.append([ int(s) for s in r.split('|')])
            elif ',' in r:
                pages_rows.append([ int(s) for s in r.split(',')])
        return rules_rows, pages_rows

a,b = readInput()

print(solve_2(a,b))