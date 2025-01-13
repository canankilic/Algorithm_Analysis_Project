# Question 1: Divide and Conquer
# Esmanur Yorulmaz - 210201008
# Canan Kılıç - 220201037

import pandas as pd
import time

# loading dataset
df = pd.read_csv('product_info.csv')  # read the CSV data file to a DataFrame

# relevant columns and clean data ( extracting )
dataset = df[['product_id', 'loves_count', 'rating']].dropna().values.tolist()  # extract required columns, drops rows with missing values, and converts to list

# implementation of Merge Sort  
def merge_sort(data, key_1, key_2):
  # recursively splits the data in two (halves) and merges it in a sorted order
    if len(data) > 1:
        mid = len(data) // 2
        left_part = data[:mid]  # left part of the split
        right_part = data[mid:]  # right part of the split

    # recursive call to right and left
        merge_sort(left_part, key_1, key_2)  
        merge_sort(right_part, key_1, key_2) 

        i = j = k = 0  # starting indices for merging

        # merge the two part in sorted order
        while i < len(left_part) and j < len(right_part):
            if (left_part[i][key_2], left_part[i][key_1]) >= (right_part[j][key_2], right_part[j][key_1]):
                data[k] = left_part[i]
                i += 1
            else:
                data[k] = right_part[j]
                j += 1
            k += 1

        # adding remaining elements of the left half
        while i < len(left_part):
            data[k] = left_part[i]
            i += 1
            k += 1

        # adding remaining elements of the right half
        while j < len(right_part):
            data[k] = right_part[j]
            j += 1
            k += 1

# iterative Quick Sort Implementation!
def quick_sort(data, key_1, key_2):
    # a stack for iterative sorting instead of recursion
    stack = [(0, len(data) - 1)]  # initialize stack with the full data range

    while stack:
        low, high = stack.pop()  # take the current range to sort
        if low < high:
            index_pivot = partition(data, low, high, key_1, key_2)  # split the data and get the pivot index
            stack.append((low, index_pivot - 1))  # push left side of the pivot to the stack
            stack.append((index_pivot + 1, high))  # push right side of the pivot to the stack

def partition(data, low, high, key_1, key_2):
    # split the data around a pivot element
    pivot = (data[high][key_2], data[high][key_1])  #  last element = pivot
    i = low - 1  # index for smaller element
    for j in range(low, high):
        if (data[j][key_2], data[j][key_1]) >= pivot:  # comparing
            i += 1
            data[i], data[j] = data[j], data[i]  # swap elements
    data[i + 1], data[high] = data[high], data[i + 1]  # put the pivot element in the right position
    return i + 1

# calculating the execution time
def calculate_time(sorting_func, dataset, key_1, key_2):
    # the time taken to sort the dataset
    starting_time = time.time()  # starting time
    sorting_func(dataset, key_1, key_2)  # execute the sorting func.
    ending_time = time.time()  # ending time
    return ending_time - starting_time  # return the elapsed time

# dataset sizes and sorting keys
size_of_datas = [1000, 5000, 10000]  # different sizes
key_1, key_2 = 1, 2  # key_1: loves_count, key_2: rating (columns)

result = []  # store result of sorting algorithms
merge_times = []  # store E.T for merge sort
quick_times = []  # store E.T times for quick sort

for size in size_of_datas:
    subset = dataset[:size]  # subset of the dataset 

    ### Merge Sort
    merge_subset = subset.copy()  # copy sub to merge sort
    merge_time = calculate_time(merge_sort, merge_subset, key_1, key_2)  # calculate E.T
    merge_times.append(merge_time)  # add the time in list

    # Saving Merge Sort result
    merge_sorted_df = pd.DataFrame(merge_subset, columns=['product_id', 'loves_count', 'rating'])  # DataFrame from sorted data
    merge_sorted_df = merge_sorted_df.sort_values(by=['rating', 'loves_count'], ascending=[False, False])  # ensure sorting consistency
    merge_sorted_df.to_csv(f'merge_sorted_{size}.csv', index=False)  # save sorted data 

    ### Quick Sort
    quick_subset = subset.copy()  # copy the subset to quick sort
    quick_time = calculate_time(quick_sort, quick_subset, key_1, key_2)  # calculate execution time
    quick_times.append(quick_time)  # add the time in list

    # saving Quick Sort result to CSV
    quick_sorted_df = pd.DataFrame(quick_subset, columns=['product_id', 'loves_count', 'rating'])  # DataFrame from sorted data
    quick_sorted_df = quick_sorted_df.sort_values(by=['rating', 'loves_count'], ascending=[False, False])  # ensure sorting consistency
    quick_sorted_df.to_csv(f'quick_sorted_{size}.csv', index=False)  # save sorted data 

    result.append(["Merge Sort", size, merge_time])  # recording result for merge sort
    result.append(["Quick Sort", size, quick_time])  # recording result for quick sort

# show result
result_df = pd.DataFrame(result, columns=["Algorithm", "Dataset Size", "Execution Time (seconds)"]) 
print(result_df)  

# Graph part
# comparison with graph
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6)) 
plt.plot(size_of_datas, merge_times, marker='o', label='Merge Sort')  
plt.plot(size_of_datas, quick_times, marker='o', label='Quick Sort')  
plt.title('Execution Time Comparison')  
plt.xlabel('Dataset Size')
plt.ylabel('Execution Time (seconds)') 
plt.legend() 
plt.grid() 
plt.savefig('execution_time_comparison.png') 
plt.show()  
