import itertools
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import itertools
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import collections

# Challenge: https://adventofcode.com/2020/day/4#part1

# Import csv
data_file_loc = 'C:/Users/jlahrman/OneDrive - LMI/Documents/Advent_of_Code/Advent_of_Code/Week04_Day04/'

column = ['passport_data']
day4data = pd.read_csv(data_file_loc + 'day_04_input.csv', 
                       header = None, 
                       names = column, 
                       skip_blank_lines=False
                      )

day4data['passport_no'] = 0
# Start an iterator for the passport number
passport_number = 1

for x in range(len(day4data)):
    if (pd.isnull(day4data.iloc[x]['passport_data'])):
    # If value is null, increment the passport number
        passport_number +=1
        day4data['passport_no'].iloc[x] = 0
    else:
    # If value is not null, apply the current group number
        day4data['passport_no'].iloc[x] = passport_number

manifesto = pd.DataFrame()

# For manifesto, start two blanks lists that we'll append to, then they can become dataframe columns
passport_number = []
# Passport detail will be the concatenated text for each individual passport
passport_detail = []

# Go through each passport number, subsetting the data to get all the passport entries into one cell
# Setting the range this way to get rid of the zeroes, I can't do the range based on the length of the data frame
for x in range(1,day4data['passport_no'].max()+1):
    passport_number.append(x)
    subset = day4data[day4data.passport_no == x]
    passport_string = ''
    for y in range(len(subset)):
        passport_string = passport_string + ' ' + str(subset.iloc[y]['passport_data'])
    passport_detail.append(passport_string.strip())
        
# Now append those lists as columns
manifesto['passport_number'] = passport_number
manifesto['passport_detail'] = passport_detail

# End result is a list of all passport numbers, with all of the fields in one line



# For the first challenge, go through that passport_detail field and see if each field name is found

# Entries is a counter for how many of the fields are found for each passport
entries = []
# For the second part of the challenge, I'm going to create a dictionary that should make it easy to extract the value associated with each key
passport_dict = []
search_list = ['byr:','iyr:','eyr:','hgt:','hcl:','ecl:','pid:']


for z in range(len(manifesto)):
    # build a dictionary by splitting at spaces, then separating the key from value using the colon
    d = dict(x.split(":") for x in manifesto.iloc[z]['passport_detail'].split(" "))
    entry = 0
    # count the number of passport fields for the passport
    for search_item in search_list:
        if search_item in manifesto.iloc[z]['passport_detail']:
            entry +=1
    entries.append(entry)
    passport_dict.append(d)
    
manifesto['passport_dict'] = passport_dict
manifesto['entries'] = entries
#I don't need that passport detail field now that I've converted it to a dictionary.
del manifesto['passport_detail']
        
# The number of rows with the same valid fields as the length of the search_list is the correct answer
print('part 1 answer:',len(manifesto[manifesto.entries == len(search_list)]))



# For the second challenge, set up individual functions to call and test each of the requirements

#byr (Birth Year) - four digits; at least 1920 and at most 2002.
def byr_test(byr_value):
    if int(byr_value) >= 1920 and int(byr_value) <= 2002:
        valid = 1
    else:
        valid = 0
    return(valid)

#iyr (Issue Year) - four digits; at least 2010 and at most 2020.
def iyr_test(iyr_value):
    if int(iyr_value) >= 2010 and int(iyr_value) <= 2020:
        valid = 1
    else:
        valid = 0
    return(valid)

#eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
def eyr_test(eyr_value):
    if int(eyr_value) >= 2020 and int(eyr_value) <= 2030:
        valid = 1
    else:
        valid = 0
    return(valid)

#ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
def ecl_test(ecl_value):
    ecl_list = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    if ecl_value in ecl_list:
        valid = 1
    else:
        valid = 0
    return(valid)

#hgt (Height) - a number followed by either cm or in:
#If cm, the number must be at least 150 and at most 193.
#If in, the number must be at least 59 and at most 76.
def hgt_test(hgt_value):
    try:
        system = hgt_value[-2:]
        measurement = int(hgt_value[:-2])
        if system == 'cm':
            if measurement >= 150 and measurement <= 193:
                valid = 1
            else:
                valid = 0
        elif system == 'in':
            if measurement >= 59 and measurement <= 76:
                valid = 1
            else:
                valid = 0
        else:
            valid = 0
    except:
        valid = 0
    return(valid)

#hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
def hcl_test(hcl_value):
    character_list = '0123456789abcdef'
    first_char = hcl_value[:1]
    rest_of_chars = hcl_value[1:]
    if first_char == '#' and len(rest_of_chars) == 6 and all(item in list(character_list) for item in list(rest_of_chars)) is True:
        valid = 1
    else:
        valid = 0
    return(valid)

#pid (Passport ID) - a nine-digit number, including leading zeroes.
def pid_test(pid_value):
    if len(pid_value) == 9 and pid_value.isdecimal() is True:
        valid = 1
    else:
        valid = 0
    return(valid)

search_list = ['byr:','iyr:','eyr:','hgt:','hcl:','ecl:','pid:']

# The creation of the dictionary removed colons, so that also needs to be done to loop through the keys
new_search_list = [s.replace(":", "") for s in search_list]

# valid_entries keeps a counter of how many passport properties are valid according to the conditions in their functions
valid_entries = []
# key_counter keeps a list of how many times each individual passport property
key_counter = []
# key_pass_counter keeps a list of how many times each property passes, so we can check if a certain property is always failing
key_pass_counter = []

for z in range(len(manifesto)):
    valid_counter = 0
    for key in new_search_list:
        if key in manifesto.iloc[z]['passport_dict']:
            key_counter.append(key)
            function_name = key + '_test'
            function_parameter = manifesto.iloc[z]['passport_dict'][key]
            # if the key exists, eval will run the key-specific function with value for its parameter
            valid = eval(function_name+'("'+function_parameter+'")')
            if valid == 1:
                key_pass_counter.append(key)
            valid_counter += valid
    valid_entries.append(valid_counter)

# Now just append that list of valid entry counts to the manifesto data frame
manifesto['valid_entries'] = valid_entries

# Answer is the number of records where all keys in the search list have valid entries
print('part 2 answer:',len(manifesto[manifesto.valid_entries == len(search_list)]))

key_counter=collections.Counter(key_counter)
key_pass_counter=collections.Counter(key_pass_counter)

# And for a final bonus available only to my premium subscribers, let's get a success rate for the individual passport fields

# Turn the counters into regular dictionaries
key_counter = dict(key_counter)
key_pass_counter = dict(key_pass_counter)
key_pass_rate = {}

# Create a third dictionary of the % success rate
for key in key_pass_counter:
    key_pass_rate[key] = round(key_pass_counter[key]/key_counter[key]*100,2)
print(key_pass_rate)