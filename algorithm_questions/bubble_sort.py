'''
The bubble sort algorithm compares every two items which are next to each other, 
and swaps them if they are in the wrong order. 

1) write the bubble sort algorithm
'''


def bubble_sort_recursive(data):

	original = data
	for i in range(len(data)-1):
		if data[i] > data[i+1]:
			data = data[:i] + [data[i+1]] + [data[i]] +data[i+2:]
	if data != original:
		return bubble_sort_recursive(data)
	else:
		return data

def bubble_sort_iterative(data):

	flag = False
	while flag is not True:
		original = data
		for i in range(len(data)-1):
			if data[i] > data[i+1]:
				data = data[:i] + [data[i+1]] + [data[i]] +data[i+2:]
		if data == original:
			flag = True
	return data

print bubble_sort_iterative([6,4,7,8,1,2,3])
print bubble_sort_recursive([6,4,7,8,1,2,3])



