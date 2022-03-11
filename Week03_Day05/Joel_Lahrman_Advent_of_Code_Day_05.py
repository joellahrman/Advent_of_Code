import pandas as pd
import numpy as np

# Import csv
data_file_loc = 'C:/Users/jlahrman/OneDrive - LMI/Documents/Advent_of_Code/Week03_Day07/'

column = ['input']
day7data = pd.read_csv(data_file_loc + 'day_07_input.csv', 
                       header = None, 
                       names = column 
                      )

# I'm not liking hard-coding the length of the characters but I'll leave it for now.
row_length = 7

# Is there a better way to add columns to a data frame?
day7data['row_char'] = np.empty((len(day7data), 0)).tolist()
day7data['seat_char'] = np.empty((len(day7data), 0)).tolist()
day7data['row'] = ""
day7data['seat'] = ""
day7data['seat_id'] = ""

for x in range(len(day7data)):
    # Has to be a better way to fill in the columns! Oh do I feel like an idiot with all this iloc business.
    # Row characters come first, then convert to base 2
    day7data['row_char'].iloc[x] = day7data['input'].iloc[x][:row_length]
    day7data['row_char'].iloc[x] = day7data['row_char'].iloc[x].replace("F", "0")
    day7data['row_char'].iloc[x] = day7data['row_char'].iloc[x].replace("B", "1")
    # Then the seat characters
    day7data['seat_char'].iloc[x] = day7data['input'].iloc[x][row_length:]
    day7data['seat_char'].iloc[x] = day7data['seat_char'].iloc[x].replace("L", "0")
    day7data['seat_char'].iloc[x] = day7data['seat_char'].iloc[x].replace("R", "1")
    # Now convert the binaries from base 2 to base 10
    day7data['row'].iloc[x] = int(day7data['row_char'].iloc[x],2)
    day7data['seat'].iloc[x] = int(day7data['seat_char'].iloc[x],2)
    # Calculate the seat_id
    day7data['seat_id'].iloc[x] = day7data['row'].iloc[x] * 8 + day7data['seat'].iloc[x]

part_1_answer = int(day7data['seat_id'].max())

print('Part 1 answer:',part_1_answer)

seat_id_list = day7data['seat_id'].tolist()
seat_id_list = [int(item) for item in seat_id_list]

# This is hacky but if there is a missing seat_id, check to see if there is a seat_id for either side. If yes we've found our missing seat.

for x in range(part_1_answer):
    if x not in seat_id_list:
        if x-1 in seat_id_list:
            if x+1 in seat_id_list:
                print('Part 2 answer:',x)

