'''Quick sort

Quicksort is a divide and conquer algorithm. 
Quicksort first divides a large array into two smaller sub-arrays: the low elements and the high elements. Quicksort can then recursively sort the sub-arrays.

The steps are:
1) Pick an element, called a pivot, from the array.
2) Reorder the array so that all elements with values less than the pivot come before the pivot, while all elements with values greater than the pivot come after it (equal values can go either way). After this partitioning, the pivot is in its final position. This is called the partition operation.
3) Recursively apply the above steps to the sub-array of elements with smaller values and separately to the sub-array of elements with greater values.
4) The base case of the recursion is arrays of size zero or one, which never need to be sorted. 

'''

# Bonus: Write the quicksort algorithm recursively
# Tip: You may need a helper method to help with the partition of the array

def quicksort(data):

	if len(data) < 2:
		return data

	pivot = data.pop()

	data_small = []
	data_big = []

	for i in data:
		if i < pivot:
			data_small.append(i)
		elif i >= pivot:
			data_big.append(i)


	if len(data_big) ==0:
		data_big.append(pivot)
	else:
		data_small.append(pivot)

	return quicksort(data_small) + quicksort(data_big)

print quicksort([1,6,9,23,5,2,3,4,9,9,4,124,7,7,8,3,4,7,890,76,4,1,1,1,908,1.2])
print quicksort([5,2])
