# for splat
from __future__ import print_function

# for reg match
import re

class SearchEngine:
    def __init__(self):
        pass
    
    #get the numbers needed
    def get_total_lines(self):
        first_line = input()
        n_and_q = list( map(int, first_line.strip().split()) )
        n = n_and_q[0]
        q = n_and_q[1]

        total_lines_per_case = n + q

        return total_lines_per_case, n, q
    
    # put database and query into two lists, then try to match
    def process_data(self):
        all_lines = self.get_total_lines()
        n = all_lines[1]
        q = all_lines[2]
        database = []
        queries = []
        match = 0
        all_matches = []

        for i in range(n):
            current_line = input()
            database.append(current_line)

        for i in range(q):
            current_line = input()
            queries.append(current_line)
        
        for i in range(q):
            match = 0
            for j in range(n):
                # need to fix this condition to reject ALL partial matches
                # https://blog.finxter.com/how-to-match-an-exact-word-in-python-regex-answer-dont/

                if (queries[i] in database[j]) and (not re.search(r'\bapp\b', queries[i])):
                    match += 1
            
            all_matches.append(match)

        # print(database, queries)

        return all_matches

# run code
test_cases = int(input())
output = []

# get each case of results as a list
for i in range(test_cases):
    test = SearchEngine()
    lines = test.process_data()
    output.append(lines)

# for each case, print each result
for j in range(test_cases):
    print ("Case {}:".format(j+1))
    for k in range(len(output[j])):
        print (output[j][k], sep = '\n')