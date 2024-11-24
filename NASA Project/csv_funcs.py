import math


def get_from_csv(keeper=1, file="middle-school-data.csv", cols=['Link Budget WPSA', 'Link Budget DS54', 'Link Budget DS24', 'Link Budget DS34']):
    import pandas as pd
    keepers = [keeper]
    file=pd.read_csv(file, usecols=cols).loc[keepers]
    l = [list(row) for row in file.values]
    return l[0]

def find_index_of_highest_value(list_of_values):
    l = list_of_values
    l2 = [x for x in l if (not math.isnan(x))]
    if l2:
        max_var = max(l2)
        return l.index(max_var)
    else:
        return 4

def num_to_antenna(num):
    if num == 0:
        return "WPSA"
    elif num == 1:
        return "DS54"
    elif num == 2:
        return "DS24"
    elif num == 3:
        return "DS34"
    elif num == 4:
        return "None active"
    else:
        raise TypeError("Number out of reach")

def csv_to_antenna(number):
    return num_to_antenna(find_index_of_highest_value(get_from_csv(number)))

def look_forwards(rows, current_number):
    what_you_see = []
    for i in range(0, rows):
        what_you_see.append(csv_to_antenna(current_number + i))
    cleansed = [x for x in what_you_see if (not x == 'None active')]
    ds34 = cleansed.count("DS34")
    ds54 = cleansed.count("DS54")
    wpsa = cleansed.count("WPSA")
    ds24 = cleansed.count("DS24")
    total_counts = [wpsa, ds54, ds24, ds34]
    if cleansed:
        max_value = max(total_counts)
        index = total_counts.index(max_value)
        antenna = num_to_antenna(index)
        return antenna
    else:
        return num_to_antenna(4)