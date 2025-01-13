# Question 3: Dynamic Programming
# Esmanur Yorulmaz - 210201008
# Canan Kılıç - 220201037

import csv ## to read .csv files

def read_csv_file(dataset): # read .csv files function
    texts = [] # we have 2 different datasets
    with open(dataset, 'r', encoding='utf-8') as file:
        read_file = csv.DictReader(file)
        for row in read_file:
            texts.append(row['text'])
    return texts

def longest_common_subsequence_func(text1, text2): # find longest common subsequence in a given array
    m, n = len(text1), len(text2)
    dp = [["" for _ in range(n + 1)] for _ in range(m + 1)] # we have dynamic programming as dp

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]: # it compares each of the text to find lcs
                dp[i][j] = dp[i - 1][j - 1] + text1[i - 1]
            else:
                dp[i][j] = dp[i - 1][j] if len(dp[i - 1][j]) > len(dp[i][j - 1]) else dp[i][j - 1]

    lcs_length = len(dp[m][n])
    return dp[m][n], lcs_length

def main():

    dataset1 = read_csv_file('document1.csv') # read datasets
    dataset2 = read_csv_file('document2.csv')

    list_of_lcs = [] # initialize the list of lcs results

    for i, (doc1, doc2) in enumerate(zip(dataset1, dataset2), start=1):
        lcs, lcs_length = longest_common_subsequence_func(doc1, doc2)
        list_of_lcs.append((lcs, lcs_length, i)) # add found lcs' to the list
        print(f"Comparison {i}:")
        print(f"Document 1: {doc1}")
        print(f"Document 2: {doc2}")
        print(f"LCS: {lcs}")
        print(f"LCS Length: {lcs_length} characters")
        print("-" * 50)

    list_of_lcs.sort(key=lambda x: x[1], reverse=True) # sort the lcs results by their length by descending order

    max_length = list_of_lcs[0][1] if list_of_lcs else 0 # find the longest lcs

    longest_lcs = [lcs for lcs in list_of_lcs if lcs[1] == max_length] # filter LCS results that have the maximum length

    if len(longest_lcs) > 1: # check if there are duplicates in the longest LCS
        matchless_lcs = {}
        for lcs, length, line in longest_lcs:
            if lcs in matchless_lcs:
                matchless_lcs[lcs].append(line)
            else:
                matchless_lcs[lcs] = [line]

        print("Longest common subsequences (LCS) with duplicates:") # prompt user and print all the lcs'
        for lcs, lines in matchless_lcs.items():
            print(f"LCS: {lcs}")
            print(f"Length: {max_length} characters")
            print(f"Lines: {', '.join(map(str, lines))}")
            print()
    else:
        print("Longest common subsequence (LCS):")
        for lcs, length, line in longest_lcs:
            print(f"LCS: {lcs}")
            print(f"Length: {length} characters")
            print(f"Line: {line}")
            print()

if __name__ == "__main__":
    main()
