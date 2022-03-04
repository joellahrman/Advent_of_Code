import itertools
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# Import csv
data_file_loc = 'C:/Users/jlahrman/OneDrive - LMI/Documents/Advent_of_Code/Week02_Day06/'

column = ['answers']
# Keep the blank lines, I'm going to use that as my delineator between groups
day6data = pd.read_csv(data_file_loc + 'day_06_input.csv', header = None, names = column, skip_blank_lines=False)

# Create a group column, fill with all 0s
day6data['group'] = 0
day6data['characters'] = np.empty((len(day6data), 0)).tolist()

#assign groups
group_number = 1

#assign groups, and convert character string to a list of individual characters
for x in range(len(day6data)):
    if (pd.isnull(day6data.iloc[x]['answers'])):
    # If value is null, increment the group number and save the blank row's group number as 999. Create a blank list based on the group number
        day6data['group'].iloc[x] = 999
        group_number +=1
    else:
    # If value is not null, apply the current group number. Split the text and append it to the group-specific list
        day6data['group'].iloc[x] = group_number
#        day6data['characters'].iloc[x] = split(day6data['answers'].iloc[x])
        day6data['characters'].iloc[x] = list(day6data['answers'].iloc[x])
        
        # Now build one group-specific list, find out how many unique values are in each list, and keep a running counter
puzzle_1_answer = 0

# Create a blank data frame that will answer both questions
# It will contain the following:
    # instances - the number of instances of each character occurring within each group
    # group_size - the number of people in each group
    # If the group_size matches the instances, that means that everybody in the group answered yes to the question
    # group - just there for documentation
puzzle_answer_df = pd.DataFrame(columns=['instances', 'group_size', 'group'])

for x in range(day6data['group'].max()):
    # filter the data down to each individual group
    subset = day6data[day6data.group == x]
    # create a blank list for the group
    group_list = []
    for y in range(len(subset)):
        # Add the characters list to the existing group_list to compile all the characters by group
        group_list.extend(subset['characters'].iloc[y])
    # Create a dictionary that will count the number of instances of each character within the group
    counts = {}
    for item in group_list:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    # Now convert that dictionary to a data frame, rename the column
    df = pd.DataFrame(counts, index=[0]).T
    df.rename(columns={df.columns[0]: 'instances'},inplace = True)
    # The group_size is the length of the subset, which is the number of people in the group
    df['group_size'] = len(subset)
    # Insert the group name
    df['group'] = x
    # Append the group-specific df to the overall df
    puzzle_answer_df = puzzle_answer_df.append(df)

# The length of the df is the answer to puzzle 1 - it's how many unique group/character combinations we have
print('puzzle_1_answer:', len(puzzle_answer_df))

# To answer the second puzzle, just filter the df to only those rows where instances match the group_size and find the length
print('puzzle_2_answer:', len(puzzle_answer_df[puzzle_answer_df.instances == puzzle_answer_df.group_size]))