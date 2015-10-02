'''Write a function which implements the Pascal's triangle:

			    1
			  1    1
		    1    2    1
		  1    3    3    1
	    1    4    6    4    1
   1    5    10    10    5    1
1     6    15    20    15   6     1 

The desired output should be a list of lists where each internal list contains one row of the triangle. Like so:

[[1], [1, 1], [1, 2, 1]...]'''

def pascal(n):

	if n == 1:
		return [[1]]
	
	array = [1]
	x = pascal(n-1)

	for i in range(len(x[-1])-1):
		array.append(x[-1][i] + x[-1][(i+1)])

	array.append(1)

	return x + [array]
	
print pascal(5)