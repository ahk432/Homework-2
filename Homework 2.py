import os
import re
#Opening File by line
#https://realpython.com/introduction-to-python-generators/
proposal = '2005proposal.pdf1.txt'

def txt_reader(file):
    for row in open(proposal, "r"):
        yield row
text = txt_reader(proposal)
text = list(text)


#Extracting rows from tables 
def get_data(x):
    with open(proposal, 'r') as data:
        for row in data:
            if x not in row:
                yield row
            elif x in row:
                break

#Taking out all rows after page 46
b = 'B-46'              
tables = get_data(b)
tables = list(tables)
            

words_list = ('%', 'Metropolitan', 'Naval', 'Base', 'Station', 'Center', 'County', 'Finance', 'Airport', 'Headquarters', 
              'Micropolitan', 'Navy', 'Fort', 'Depot', 'Research', 'Army', 'Field', 'General', 'Air Force')
words_list = list(words_list)

#Appending filtered list
#https://www.geeksforgeeks.org/python-filter-a-list-based-on-the-given-list-of-strings/#

new_list = []
for n in tables:
    for i in words_list:
        if i in n:
            new_list.append(n)
 
#https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/
new_list = [i for n, i in enumerate(new_list) if i not in new_list[:n]]

#Dropping rows with 'total' in them
def drop_value(file,x):
    for row in file:
        if x in row:
            continue
        else:
            yield row

x = 'Total'
dropped_total = drop_value(new_list, x)
dropped_total = list(dropped_total)

#Replacing values
dropped = '\n'.join(dropped_total)
dropped = dropped.replace('\n',' ')
dropped = dropped.replace(',', '')
dropped = dropped.replace('  ', ' ')
dropped = dropped.replace('(', '-')
dropped = dropped.replace(')', '')
dropped = dropped.replace('Area', 'Area,').replace('Gain', ', Gain,').replace('Close', ', Close,').replace('Realign', ', Realign,') 

#Chat GPT
pattern = '(\D\d+)'
final_product = re.sub(pattern, r'\1,', dropped)

final_product = final_product.replace(',.', '.').replace(', ,', ',').replace(',%', '%').replace('%', '% \n')


def add_string(file, msa):
    for row in file.split('\n'):
        if msa not in row:
            yield 'MSA Continued,' + row
        elif msa in row:
            yield row 
            
final_string = add_string(final_product, 'polit')           
final_string = list(final_string)
final_product = '\n'.join(final_string)


#Adding columns
columns = 'msa, base,action, mil_out, civ_out, mil_in, civ_in, mil_net, civ_net,net_contractor, direct, indirect, total, ea_emp, ch_as_percent\n '
final_product = ''.join((columns, final_product))

#Making a csv file
with open('Homework2.csv', 'w') as ofile:
    ofile.write(final_product)
    

