import string
import os
"""
Content Indexing Engine Capstone Project

You have a bunch of files in the file system!  How can we index these files to make them easily searchable by keyword?

Indexing is a way of moving work 'upfront' so that when the user searches, less work is needed to get them the right search results.

Tips:

Look into array .extend() method
Look into string module , and .punctuation
Look into the set() builtin data type

Example index:
index = {'cat':['filename1','filename2','filename3'],'dog':['filename2',filename3]}

"""


#Tip: upgrade your recursive find code from a previous exercise to return a list of files 

def recursive_find(name, index = {}):

    array = os.listdir(name)
    for i in array:
        path = os.path.join(name, i)
        if os.path.isdir(path):
            recursive_find(path, index)
        else:
            data_string = read_data(path)
            data_string = strip_punctuation(data_string)
            data = split_data_string(data_string)
            index = add_to_index(data, i, index)
    return index

stop_words = ['a','an','and','i']

def read_data(filename):
    with open(filename,"r") as f:
        return f.read()

def strip_punctuation(data_string):

    punctuation = ["\n",",","'","/","\"","?","+","*","(",")","#","!", "-"]

    for i in punctuation:
        data_string = data_string.replace(i, ' ')

    return data_string

def split_data_string(data_string):

    data = data_string.split(" ")
    data = list(set(data))
    data = map(lambda x: x.lower(), data)
    if '' in data:
        data.remove('')
    return data

        
def add_to_index(words,filename,index):
    
    for i in words:
        if i in index:
            index[i].append(filename)
        else:
            index[i] = [filename]

    return index

def handle_words(response, index):

    words = response.split(' ')
    both = ''

    if set(words).issubset(set(index)):
        for i in range(len(words)-1):
            print index[words[i]], '/', index[words[i+1]]
            both = list(set(index[words[i]]) & set(index[words[i+1]]))
        if both == '':
            both = index[words[0]]
        print '\n%s found in files %s' % (words, both)

    else:
       print '\n%s not found....' % list(set(words) - set(index))


def run_interactive():
    print '''\n***Welcome to Josh's content index!***\n'''

    #index = recursive_find('/home/josh/Desktop/text_files')
    response_1 = ''
    response_2 = ''
    while not os.path.isdir(response_1):
        if response_1 == 'q':
            return
        response_1 = raw_input('Please enter a valid directory to index or press q to quit > ')

    index = recursive_find(response_1)
    while response_2 != 'q':

        response_2 = raw_input('\nEnter the item/s (separated by spaces) you would like to search or press q to quit > ')
        
        if response_2 == 'q':
            break

        handle_words(response_2, index)
        
    print "\nThankyou for using Josh's content index.......\n"

run_interactive()

        

