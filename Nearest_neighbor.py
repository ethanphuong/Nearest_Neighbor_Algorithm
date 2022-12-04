import struct
import math
import itertools
from math import sqrt

#function to find number of columns in text file
def num_columns(open_file):
    #open file
    read_first = open(open_file, "r")

    #method to find number of columns by reading each line
    first_line = next(read_first)
    col_num = len(first_line.split())
    
    #close file
    read_first.close()

    #return number of columns
    return col_num

def nearest_neighbor(file_name):
    
    #get number of columns
    col_num = num_columns(file_name)

    #open file
    text_file = open(file_name, "r")

    #get all the text from the file
    f = text_file.readlines()
    result, first_col, classes_total = [], [], []
    total = 0

    #split the first column from the rest to get the classes
    for a in f:
        first = struct.pack('f', float(a.split()[0]))
        first_col.append(struct.unpack('f', first)[0])

    #split the rest of the columns and work on features one by one
    for curr_col in range(1, col_num):
        #append current feature to result
        for i in f:
            s = struct.pack('f', float(i.split()[curr_col]))
            result.append(struct.unpack('f', s)[0])

        total = 0
        #nearest neighbor algorithm
        for z, x in enumerate(result):
            nearest_neighbor_distance = math.inf
            curr_class = math.inf

            #iterate through current feature in result list
            for y, k in enumerate(result):
                #make sure we're not comparing the same current element in the column
                if x == k:
                    continue
                #euclidean distance
                temp_dist = sqrt((x - k) ** 2)
                #find the smallest euclidean distance
                if temp_dist < nearest_neighbor_distance:
                        nearest_neighbor_distance = temp_dist
                        curr_class = first_col[y]
            #keep track of total that are correctly classified
            if first_col[z] == curr_class:
                total += 1
        #list of total correctly classified for each feature
        classes_total.append(total)
        #reset result list to work on next feature
        result = []
    #return list of correctly classified
    return classes_total

#backwards selection search
def backward_selection(list, file_name, file_count):
    #get column number
    col_num = num_columns(file_name)
    
    full_total, total, prevAccuracy, maxAccuracy = 0, 0, 0, 0
    #dataset summary
    print("\nThis dataset has", col_num - 1, "features, with", file_count, "instances.\n")
    for i in (list):
        full_total += i

    #initial accuracy with all the features
    print("Running nearest neighbor algorithm with all ", col_num - 1, " features I get an accuracy of ", (str([(full_total / (file_count * (col_num - 1))) * 100])[1:5]), "%\n", sep="")

    clone_list = list.copy()
    curr_subset, print_list, max_list = [], [], []
    #iterate through the list eliminating the lowest correctly classified feature each iteration
    for i in range(1, len(clone_list)):
        #removed one feature
        col_num -= 1
        for j in clone_list:
            temp = clone_list[0]
            clone_list.pop(0)
            total = sum(clone_list)
            #accuracy is the total current correctly classified in the list divided by the total number of features in the current list
            accuracy = ((int(total) / (file_count * (col_num - 1))) * 100)
            #preventing spurious precision by ending the string at 4
            for a in clone_list:
                curr_subset.append(list.index(a) + 1)
            print("Using feature(s) ", curr_subset, " accuracy is ", (str(accuracy)[0:4]), "%")
            if i == (len(list)) - 2:
                if prevAccuracy < accuracy:
                    prevAccuracy = accuracy
                    maxAccuracy = accuracy
                    max_list = clone_list.copy()
            clone_list.append(temp)
            curr_subset = []
        #remove the minimum feature in each iteration
        clone_list.remove(min(clone_list))
        print("\n")
    prevAccuracy = 0
    for i in max_list:
        print_list.append(list.index(i) + 1)
    print("Finished search! The best feature subset is ", print_list, " which has an accuracy of ", (str(maxAccuracy)[0:4]), "%", sep="")

#forward selection search
def forward_selection(list, file_name, file_count):

    #get column number
    col_num = num_columns(file_name)
    
    full_total, total, best_value, subset_place, combination, loop_round, best_subset, best_accuracy, prevAccuracy = 0, 0, 0, 0, 0, 0, 0, 0, 0, 
    set_list, curr_subset, print_subset = [], [], []

    #dataset summary
    print("\nThis dataset has", col_num - 1, "features, with", file_count, "instances.\n")
    for i in (list):
        full_total += i

    #initial accuracy with all the features
    print("Running nearest neighbor algorithm with all ", col_num - 1, " features I get an accuracy of ", (str([(full_total / (file_count * (col_num - 1))) * 100])[1:5]), "%", sep="")
    #forward selection by choosing the highest combination accuracy each time
    for i in range(1, len(list)):
        set_number = 0
        #subset of list because we start with 1 and move on to 2, 3...
        for subset in itertools.combinations(list, i):
            for x in subset:
                for y in set_list:
                    if x == y:
                        combination += 1
            #was dealing with some edge cases
            if combination == loop_round:
                set_number += 1
                for place in subset:
                    total += place
                #same way to find accuracy as backwards search
                accuracy = ((int(total) / (file_count * len(subset))) * 100)
                #print out different combinations
                for a in subset:
                    curr_subset.append(list.index(a) + 1)
                print("Using feature(s) ", curr_subset, " accuracy is ", (str(accuracy)[0:4]), "%", sep="")
                #sort current subset in descending order to make it easier to figure out which combo has the best value
                sorted_subset = sorted(subset, reverse=True)
                if (int(sorted_subset[subset_place]) / file_count) > best_value:
                    #record best feature in the current subset
                    best_value = (int(sorted_subset[subset_place]) / file_count)
                    #record best accuracy
                    best_accuracy = ((int(total) / (file_count * len(subset))) * 100)
                    #change the best subset to the current subset
                    best_subset = subset
            
            curr_subset, print_subset = [], []
            combination, total = 0, 0
        print("\n")
        #checking if the accuracy was lowered
        if prevAccuracy > best_accuracy:
            print("\n", "Warning, accuracy lowered, continuing search", sep="")
        
        subset_place += 1
        loop_round += 1
        set_list.append(best_value * file_count)
        prevAccuracy = best_accuracy

    #print the best combination from the current list that has been selected
    for a in best_subset:
        print_subset.append(list.index(a) + 1)
    print("Feature set ", print_subset, " was the best, accuracy is ", (str(best_accuracy)[0:4]), "%", "\n", sep="")

def main():
    file_length = 0
    print("Welcome to my nearest neighbor feature selection algorithm.\n")
    file_to_open = input("Type in the name of your file: ")
    #figuring out if it is a large file or a small file to find out the number of rows
    #(this only works because teh files are standardized)
    if (file_to_open.find("Large") != -1):
        file_length = 1000
    else:
        file_length = 500
    test_list = nearest_neighbor(file_to_open)
    algorithm = input("Type in algorithm you want to run (1 Forward Selection, 2 Backward Elimination): ")
    
    #which algorithm to use
    if algorithm == "1":
        forward_selection(test_list, file_to_open, file_length)
    elif algorithm == "2":
        backward_selection(test_list, file_to_open, file_length)

main()