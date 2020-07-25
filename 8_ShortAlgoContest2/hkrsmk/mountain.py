# for splat
from __future__ import print_function

# for reg match
import re

# N
test_cases = int(input())

# empty arrays for data
total_mountains = []
heights = []
result = []
indexl = []

# find peak for each mountain for 1 case
def search_forward(vals, rev = 0):
    max = 1

    # flip backwards mountains
    if rev == 1:
        vals.reverse()
        # print('reversed array is {}'.format(vals))

    # count consecutive increments of 1, only
    for i in range(len(vals)-1):
        if (vals[i] + 1) == (vals[i+1]):
            max += 1
            # print('forward max is {}'.format(max))
        
        # once it is no longer consecutive, don't bother counting the rest
        else:
            break
    
    return max

# grab all the input and process
for i in range(test_cases):

    # ignore first newline
    newline = input()

    # total steps length L
    total_mountains.append(input())

    # H of each step
    heights.append(input().split())

    # convert heights to int
    int_heights = list(map(int, heights[i]))

    # non-mountains get -1 -1
    if '1' not in heights[i]:
        result.append(-1)
        indexl.append(-1)

    else:
        # total '1's in the list

        # total_ones = array of [index of ones for heights[i]]
        total_ones = [k for k, x in enumerate(heights[i]) if x == "1"]
        highest = []

        # for each '1' in the list,
        for k in range(len(total_ones)):

            # start looking for height from position of '1' in the array
            one_location = total_ones[k]

            # slice to ignore everything before '1'
            start_looking = heights[i][one_location:]

            # to check backwards, slice to ignore everything after the '1'
            look_back = heights[i][:one_location+1]

            # if 1 is at the start of all the mountains, don't bother with backwards search
            if one_location == 0:
                forward_max = search_forward(list(map(int,start_looking)))
                highest.append(forward_max)
                
            else:
                forward_max = search_forward(list(map(int,start_looking)))

                # print('look back is {}'.format(look_back))
                backward_max = search_forward(list(map(int,look_back)), rev = 1)

                # look backwards and forwards, then see which one is the highest
                highest.append(max(int(forward_max), int(backward_max)))

        # add height to results array
        result.append(max(highest))

        # index of highest mountain. I think this defaults to first instance of max height (left most mountain)
        height_loc = heights[i].index(str(max(highest)))

        # add index of highest mountain into indexl
        indexl.append(height_loc)

# for each case, print each result and index
for j in range(test_cases):
    print ("Case #{}: {} {}".format(j+1, result[j], indexl[j]))