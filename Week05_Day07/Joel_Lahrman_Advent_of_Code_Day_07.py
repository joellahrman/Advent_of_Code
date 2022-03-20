import itertools
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import collections
import re

# Challenge: https://adventofcode.com/2020/day/7

# Import csv
data_file_loc = 'C:/Users/jlahrman/OneDrive - LMI/Documents/Advent_of_Code/Advent_of_Code/Week05_Day07/'

column = ['luggage_rules']
day7data = pd.read_csv(data_file_loc + 'day_07_input_small.csv', 
                       header = None, 
                       names = column, 
                       skip_blank_lines=False
                      )

bag_parents = []
bag_children = []
luggage_rule_string = 'contain'
characters_to_remove = [' bags', ' bag', '.']
#,'1','2','3','4','5','6','7','8','9','  ']

for x in range(len(day7data)):
    # First, find the position of the separator between key and value
    position = day7data.iloc[x]['luggage_rules'].index(luggage_rule_string)
    # Now take the left-most number of characters based on that value
    bag_parent = day7data.iloc[x]['luggage_rules'][:position].strip()
    # The value is made up of the right characters, probably an easier way to do this but I'm rolling with it
    bag_child = day7data.iloc[x]['luggage_rules'][-(len(day7data.iloc[x]['luggage_rules'])-position-len(luggage_rule_string)):].strip()
    # From both columns, remove a list of strings that we'll no longer need - ' bag', ' bags','.', all numbers
    # Has to be an easier way!
    for char in characters_to_remove:
        bag_parent = bag_parent.replace(char, '').strip()
        bag_child = bag_child.replace(char, '').strip()
    # turn the values into a list
    bag_child = bag_child.split(',')
    bag_parents.append(bag_parent)
    bag_children.append(bag_child)

day7data['bag_parents'] = bag_parents
day7data['bag_children'] = bag_children


# Now break apart the lists of children into individual rows
pairwise_df = pd.DataFrame()
bag_quantity_list = []
bag_parent_list = []
bag_child_list = []

for x in range(len(day7data)):
    for z in range(len(day7data.iloc[x]['bag_children'])):
        bag_parent_list.append(day7data.iloc[x]['bag_parents'])
        position = day7data.iloc[x]['bag_children'][z].strip().index(' ')
        # Separate the quantity from the name of the color, same exercise as above
        bag_quantity_list.append(day7data.iloc[x]['bag_children'][z].strip()[:position])        
        bag_child_list.append(day7data.iloc[x]['bag_children'][z].strip()[-(len(day7data.iloc[x]['bag_children'][z].strip())-position-1):].strip())

pairwise_df['bag_parent'] = bag_parent_list
pairwise_df['bag_child'] = bag_child_list
pairwise_df['bag_quantity'] = bag_quantity_list

# Replace 'no' with zero in the bag_quantity field
pairwise_df['bag_quantity'] = pairwise_df['bag_quantity'].replace(['no'],0)
# Then make sure it's an integer
pairwise_df['bag_quantity'] = pairwise_df['bag_quantity'].astype(int)



# for part 1:

def number_of_bags(bag_color,master_list):
    # parents will keep a list of all the parents of the bag color we're looking up so that we can rerun the fuction
    # master_list is the overall list of all bag colors that could contain the original bag color
    parents = []
    for z in range(len(bag_color)):
        # filter pairwise_df up to any rows that have the bag color as the child
        subset = pairwise_df[pairwise_df.bag_child == bag_color[z]]
        # Add the parents to the list of parents, and keep the list unique
        parents.extend(subset['bag_parent'].tolist())
        parents = list(set(parents))
        # The master_list just keeps growing with the number of parents
        master_list.extend(parents)
    # If there are parents we need to look up, run the function again and pass in master_list as the second argument
    # This clears out the list of parents for the next iteration when the function starts, but keeps the master list
    if len(parents) > 0:
        number_of_bags(parents,master_list)
    return(list(set(master_list)))

final_master_list = number_of_bags(['shiny gold'],[])
print('Part 1 answer:',len(final_master_list))


# for part 2

# Start by passing creating a dictionary made from all the bags that have no bags in them.
# Those are the only bags that we initially know the contents of (0 bags).
# This is the lowest level, we'll work our way up to determine how many bags are in every bag by color
# The trick is we have to iterate upwards, and can only determine the total of the bags inside after
# we know how many bags are inside ALL of its children
# We will create a dictionary that gets populated with the final number of bags contained by each colored bag

# Start by creating a dictionary with each of the bags that have no bags inside them
# They go into the dictionary with a value of zero in the dictionary
zero_dict = {}
lowest_level = pairwise_df[pairwise_df['bag_quantity'] == 0]
for k in range(len(lowest_level)):
    if lowest_level.iloc[k]['bag_parent'] not in zero_dict:
        zero_dict[lowest_level.iloc[k]['bag_parent']] = 0

def bag_quantities(quantity_dict,color,iterations):
    iterations +=1
    # Make a list of all parents who have a child in the dictionary.
    parent_candidates = list(set(pairwise_df[pairwise_df['bag_child'].isin(quantity_dict)]['bag_parent'].tolist()))
    # Remove parent_candidates who are already in the dictionary, we don't need to do them again
    filtered_parent_candidates = []
    for a in parent_candidates:
        if a not in quantity_dict:
            filtered_parent_candidates.append(a)
    # Create a temporary dictionary just for each iteration, we'll append it to the quantity_dict at the end
    temp_dict={}
    # Now go through each parent in the filtered parent candidates individually
    for j in range(len(filtered_parent_candidates)):
        # Filter the data to all entries for each parent, not just the entries with children already in the dictionary
        parent_df = pairwise_df[pairwise_df['bag_parent'] == filtered_parent_candidates[j]]
        # Turn the list of the parent's children into a list
        parent_list = list(set(parent_df['bag_child'].tolist()))
        # If ALL the children of this parent are already in the dictionary, then we can calculate the total quantity and add this parent to the dictionary
        if all(x in quantity_dict.keys() for x in parent_list):
#            print("Yay! We can do", filtered_parent_candidates[j])
            quantity = 0
            for x in range(len(parent_list)):
                # So for each parent, we want to add the quantity of each child bag
                # PLUS the number of bags each of those child bags contain (which we already know from the dictionary)
                quantity += parent_df.iloc[x]['bag_quantity'] * (1+quantity_dict[parent_df.iloc[x]['bag_child']])
            # Then append this entry to the temporary dictionary
            temp_dict[parent_df.iloc[x]['bag_parent']] = quantity
    # We can't append the temp_dict to the quantity_dict until after we've gone through all the parent candidates
    # Otherwise it could mess up the next candidate in the list
    quantity_dict.update(temp_dict)
    # probably inefficient but now we need to determine whether to run it through again, repeating the top step to see if there are still parents to test.
    parent_candidates = list(set(pairwise_df[pairwise_df['bag_child'].isin(quantity_dict)]['bag_parent'].tolist()))
    # Remove parent_candidates who are already in the dictionary, we don't need to do them again
    filtered_parent_candidates = []
    for a in parent_candidates:
        if a not in quantity_dict:
            filtered_parent_candidates.append(a)
    if (len(filtered_parent_candidates)) > 0:
        color = color
        bag_quantities(quantity_dict,color,iterations)
    return(quantity_dict[color])

part_2_answer = bag_quantities(zero_dict,'shiny gold',0)
print('Part 2 answer:',part_2_answer)

# To have a look at all answers, convert the dictionary to a data frame and then write to a csv.
#pd.DataFrame(quantity_dict.items(), columns=['bag', 'total_bags_inside']).to_csv(csv_name +'_quantity_dict.csv', index=False)


