'''

A recursive function is one that calls itself. Using this technique can make it easier and cleaner to solve certain problems.


The most common example is writing a function to compute factorials

4! = 4 * 3 * 2 * 1 

This is an example of linear recursion.  Recursion is a method in programming where a function calls itself one or more times in its body.

Linear recursion solutions often contain a base case.

A base case is the first/most basic case in the problem.  

E.g. In computing factorials, the base case is computing the factorial of 1.  The program should return 1.  Base cases allow the recursive solution to avoid ending up in an infinite loop.

Example: 

4! = 4 * 3!
3! = 3 * 2!
2! = 2 * 1 

Replacing the calculated values gives us the following expression 

4! = 4 * 3 * 2 * 1

'''
import time

#iterative version - meaning using standard looping constructs - write a function that takes n and returns factorial
def fact_iter(num):
	sum_ = 1
	for i in range(num, 0, -1):
		sum_*= i
	return sum_

#recursive version - write a function that takes n and returns factorial - don't forget the base case!

a = time.time()
print fact_iter(3)
b = time.time() - a
print b

def fact_rec(num):
	if num == 1:
		return 1
	else:
		return num*fact_iter(num-1)

a = time.time()
print fact_rec(3)
b = time.time() - a
print b

#trace through the algorithm to understand it

#add print statements where appropriate so you can debug it easily

# Bonus: Use timeit to see how long each algorithm takes: http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python

# Using a for loop, sum the values in a

total = 0
d = [1,2,7,9]
a = time.time()

for i in d:
	total += i

b = time.time() - a
print b

assert total == sum(d)


#Now write a recursive function that takes a list and returns the sum of that list

#Trace through the algorithm to understand it

#Add print statements where appropriate so you can debug it easily

g = [2,47,8,10]

def recursive_sum(vals):

	if len(vals) == 1:
		return vals[0]
	else:
		return vals[0] + recursive_sum(vals[1:])


assert recursive_sum(g) == sum(g)

a = time.time()
print recursive_sum(g)
b = time.time() - a
print b

# Bonus: Use timeit to see how long each algorithm takes: http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
