'''
Binary Search in English:
1) Sort the list.

2) Let i = length / 2

3) Compare term at index i to your key.

a. If they are equal, return the index.

b. If key is greater than this term, repeat 3 (recurse) on upper half of list i = (i + length) / 2 (or (i + top) / 2 depending how you implement)

c. If key is less than this term, repeat 3 on lower half i = i/2 or (i + bottom)/2

4) Stop recursion if/when the new i is the same as the old i. This means you've exhausted the search. Return -1

Tips: Be careful for off-by-one errors, which can make you exclude certain terms by mistake, or cause infinite recursion, but this is the general idea. Pretty straightforward.

Think of it as playing 'Guess the number' for the numbers 1 through 100. 

You take a guess, I tell you higher or lower. 
You say 50, I say lower. 
You say 25, I say higher. 
You say 37, etc...

1) Write a binary search algorithm

2) Bonus: Write a binary search algorithm recursively
'''



def binary_search(value, data):
	data.sort()
	print "Sorted data:", data
	choice = ''
	index = 0
	while choice != value:
		length = len(data)/2
		choice = data[length]
		if choice > value:
			data = data[:length]
		else:
			index += length
			data = data[length:]	
	print data
	return choice, index

def recursive_binary_search(value, data):
	data.sort()
	length = len(data)/2
	choice = data[length]
	if choice == value:
		return choice, length
	elif choice > value:
		choice, index = recursive_binary_search(value, data[:length])
	else:
		choice, index = recursive_binary_search(value, data[length:])
		index += length
	return choice, index


print binary_search(5, [1,2,3,4,7,8,9,5,6,22,7,8,2,3,2,10,99,8,6,7,3,3,2])

print recursive_binary_search(5, [1,2,3,4,7,8,9,5,6,22,7,8,2,3,2,10,99,8,6,7,3,3,2])

print binary_search(1, [1,2,3,4,7,8,9,5,6,22,7,8,2,3,2,10,99,8,6,7,3,3,2])

print recursive_binary_search(1, [1,2,3,4,7,8,9,5,6,22,7,8,2,3,2,10,99,8,6,7,3,3,2])


