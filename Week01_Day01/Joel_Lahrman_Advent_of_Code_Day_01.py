import itertools
import requests
import pandas as pd
import numpy as np

# I thought I'd try to get fancy and import directly from the URL
# But all I get is a message that says 'Puzzle inputs differ by user.  Please log in to get your puzzle input.'
url = "https://adventofcode.com/2020/day/1/input"
text = requests.get(url).text
print(text)

# So instead I saved the data to a csv and import it
data_file_loc = 'C:/Users/jlahrman/OneDrive - LMI/Documents/Advent_of_Code/Day01/'
day1data = pd.read_csv(data_file_loc + 'day_01_input.csv', header = None)

# Then change it to a list
day1datalist = day1data.values.tolist()

target_sum = 2020

counter = 0
matches = 0

# x starts at the first item, then y iterates through every higher index.
# In the end this will loop through every combination
# Yes this is horribly ugly and inefficient! Just add a third loop for part 2 of the challenge

for x in range(len(day1datalist)):
    for y in range(x+1,len(day1datalist)):
        num1 = np.array(day1datalist[x])
        num2 = np.array(day1datalist[y])
        total = num1 + num2
        counter +=1
        if total == target_sum:
            matches += 1
            print('First Half')
            print('first index', x, ', second index', y, 'first number:', num1, 'second number:', num2)
            product = num1 * num2
            print(product)
print('Tried ', counter, 'combinations. Found ', matches, 'matches')

# Some folks were using itertools.
# When I tried that (I actually did this in a Jupyter notebook) I couldn't get anything to show in my all_combos
# Perhaps a Python version issue?

all_combos = itertools.combinations(day1data,2)
print('all_combos:',type(all_combos))
print(all_combos)

list_all_combos = list(all_combos)
print('list_all_combos:',type(list_all_combos))
print(list_all_combos)
            
