import struct
import math
import itertools
from math import sqrt

def nearest_neighbor(file_name):
    #finding number of columns
    read_first = open(file_name, "r")

    first_line = next(read_first)
    col_num = len(first_line.split())

    #close it back to reset the line we're on for reading
    read_first.close()

    text_file = open(file_name, "r")

    f = text_file.readlines()
    result = []
    first_row = []
    classes_total = []
    total = 0

    for a in f:
        first = struct.pack('f', float(a.split()[0]))
        first_row.append(struct.unpack('f', first)[0])

    for curr_col in range(1, col_num):
        for i in f:
            s = struct.pack('f', float(i.split()[curr_col]))
            result.append(struct.unpack('f', s)[0])

        total = 0
        for z, x in enumerate(result):
            nearest_neighbor_distance = math.inf
            curr_class = math.inf

            for y, k in enumerate(result):
                if x == k:
                    continue
                temp_dist = sqrt((x - k) ** 2)
                if temp_dist < nearest_neighbor_distance:
                        nearest_neighbor_distance = temp_dist
                        curr_class = first_row[y]

            if first_row[z] == curr_class:
                total += 1

        classes_total.append(total)
        result = []

    return classes_total

def backward_selection(list, file_name, file_count):
    #finding number of columns
    read_first = open(file_name, "r")

    first_line = next(read_first)
    col_num = len(first_line.split())
    
    #close it back to reset the line we're on for reading
    read_first.close()

def forward_selection(list, file_name, file_count):

    #finding number of columns
    read_first = open(file_name, "r")

    first_line = next(read_first)
    col_num = len(first_line.split())

    #close it back to reset the line we're on for reading
    read_first.close()
    
    full_total, total, best_value, subset_place, combination, loop_round, best_subset, best_accuracy, prevAccuracy = 0, 0, 0, 0, 0, 0, 0, 0, 0
    set_list = []
    print("\nThis dataset has", col_num - 1, "features, with", file_count, "instances.\n")
    for i in (list):
        full_total += i

    print("Running nearest neighbor algorithm with all ", col_num - 1, " features I get an accuracy of ", (str([(full_total / (file_count * (col_num - 1))) * 100])[1:5]), "%\n", sep="")
    for i in range(1, len(list)):
        set_number = 0
        for subset in itertools.combinations(list, i):
            for x in subset:
                for y in set_list:
                    if x == y:
                        combination += 1
            if combination == loop_round:
                set_number += 1
                for place in subset:
                    total += place
                print("Using feature(s) ", subset, " accuracy is ", round(((int(total) / (file_count * len(subset))) * 100), 2), "%", sep="")
                sorted_subset = sorted(subset, reverse=True)
                if (int(sorted_subset[subset_place]) / file_count) > best_value:
                    best_value = (int(sorted_subset[subset_place]) / file_count)
                    best_accuracy = ((int(total) / (file_count * len(subset))) * 100)
                    best_subset = subset
            
            combination = 0
            total = 0
        if prevAccuracy > best_accuracy:
            print("\n", "Warning, accuracy lowered, continuing search", sep="")
        print("\n", "Feature set", best_subset, " was the best, accuracy is ", round(best_accuracy, 2), "%", "\n", sep="")
        subset_place += 1
        loop_round += 1
        set_list.append(best_value * file_count)
        best_value = 0
        prevAccuracy = best_accuracy

def main():
    file_length = 0
    print("Welcome to my nearest neighbor feature selection algorithm.\n")
    file_to_open = input("Type in the name of your file: ")
    if (file_to_open.find("Large") != -1):
        file_length = 1000
    else:
        file_length = 500
    test_list = nearest_neighbor(file_to_open)
    algorithm = input("Type in algorithm you want to run (1 Forward Selection, 2 Backward Elimination): ")
    
    if algorithm == "1":
        forward_selection(test_list, file_to_open, file_length)

main()