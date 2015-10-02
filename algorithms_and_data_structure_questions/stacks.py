'''

These are some useful data structures. 

Sets are just like mathmatical sets. You can turn an array/list into a set with the set() function. A set contains a unique set of elements, no duplicates. It supports operations
like union, intersetion and difference between two sets.

They both can work with a basic array. It is just how they are used.

A queue is just like a line a a register in a shop. One person is at the register and new customers line up behind them. When the one person leaves the next person moves to the register.
A queue is also referred to as FIFO (First in, first out)


Read up through the balanced parenthesis section: 
http://interactivepython.org/runestone/static/pythonds/BasicDS/WhatisaStack.html

Additional info:
https://docs.python.org/2/tutorial/datastructures.html

A stack is an array/list, but all operations happen to the end of the list.

Example from python docs

>>> stack = [3, 4, 5]
>>> stack.append(6)
>>> stack.append(7)
>>> stack
[3, 4, 5, 6, 7]
>>> stack.pop()
7
>>> stack
[3, 4, 5, 6]
>>> stack.pop()
6
>>> stack.pop()
5
>>> stack
[3, 4]

What follows below is an actual interview question I got. The "trick" to this question is to use a stack. Using a stack is so common in interview questions. Armed with that knowledge try to solve it.


Write a program that determines if a string is valid or invalid. In lieu of a formal definition, generalize from the following examples.

Examples of valid strings include:

[]
()
()[]
[()]
a(b[c]d)e

Examples of invalid strings include:

[
)
[(])
[(])[]

For example, a command-line program is-string-valid, should produce the following outputs for the given inputs:

$ is-string-valid '[]'
true
$ is-string-valid '['
false

'''

# Build methods, using the stack concept and the above code examples, to make these asserts pass

def valid(string):
	array = []
	for i in string:
		if i in ('(', '['):
			array.append(i)
		elif i== ')':
			if array.pop() != '(':
				return False
		elif i == ']':
			if array.pop() != '[':
				return False
	if array == []:
		return True
	else:
		return False



assert valid("()")

assert valid("[[()]]")

assert not valid('[(])[]')

assert not valid("(")

assert not valid("([(])")



