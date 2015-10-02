
'''The Fibonacci numbers are the numbers of the following sequence of integer values: 

0,1,1,2,3,5,8,13,21,34,55,89, ... 

The Fibonacci numbers are defined by: 
Fn = Fn-1 + Fn-2 
with F0 = 0 and F1 = 1 

The Fibonacci sequence is named after the mathematician Leonardo of Pisa, who is better known as Fibonacci. In his book "Liber Abaci" (publishes 1202) he introduced the sequence as an exercise dealing with bunnies. His sequence of the Fibonacci numbers begins with F1 = 1, while in modern mathematics the sequence starts with F0 = 0. But this has no effect on the other members of the sequence. 

The Fibonacci numbers are easy to write as a Python function. It's more or less a one to one mapping from the mathematical definition:
'''

# Solve this iteratively
def fib_iter(n):
	array = [1]
	old_num = 1
	num = 2
	sum_ = 1
	while num < n:
		sum_ += num
		new_num = old_num + num
		old_num = num
		num = new_num
	return sum_

# Solve this recursively

def fib_rec(n):
	if n == 2 or n == 1:
		return 1
	return fib_rec(n-1) + fib_rec(n-2)

def fib_rec_array(n):

	if n==1 or n ==2:
		return [fib_rec(n)]
		
	return fib_rec_array(n-1) + [fib_rec(n)]

print fib_rec_array(10)

# Trace through the algorithm to understand it - using tree diagrams

# Tip: Step through the algorithm here:
# http://pythontutor.com/visualize.html#mode=display

# Bonus: Use timeit to see how long each algorithm takes: http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
