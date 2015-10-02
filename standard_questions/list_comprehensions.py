'''

Manipulating lists of data is such a common practice that Python has some extra special abilities for working with lists. 

These abilities are called list comprhensions. 

They are great for transforming data in a list. A list goes in and a list comes out.

List comprehensions are a good way to define and create lists in Python in just one line of code.

Here is some additional reading that provides helpful examples and refactor of code:

http://www.pythonforbeginners.com/lists/list-comprehensions-in-python/

'''

#write a for loop that squares every number in the list a and creates a new list r with the results

a = [1, 2, 3]

r =[x**2 for x in a]

assert r == [1, 4, 9]

#now do the same thing but with a list comprehension

a = [1, 2, 3]

r = [x**2 for x in a]

assert r == [1, 4, 9]


#A common thing in web apps is displaying only the first letter of a name for privacy. Lets say we have a list of first names, the code that displays the names also takes a list, but we want that list to be just the first letter. Use a list comprehension to transform the data.

a = ["Bob","Jane","Joe"]

r = [x[0] for x in a]

assert r == ['B', 'J', 'J']

#can you change the list comprehension to include a '.' after the initial?

r = [x[0] + '.' for x in a]

assert r == ['B.', 'J.', 'J.']


#Now what usually happens is we have two lists from the database, a list of first names and last names, we want to combine them to create the display name. Create a list comprehension to do this.

a = ["Bob","Jane","Joe"]
b = ['Newhart','Ritter','Newcastle']

r = [a[x][0] + '. ' + b[x] for x in range(len(a))]

print r

assert r == ['B. Newhart', 'J. Ritter', 'J. Newcastle']


#Lets say there are seats in a small theater. Three rows (a-c) and three seats (1-3) and we want build a list of all the seats. Use a list comprehension to build this list

a = ['a','b','c']
b = ['1','2','3']


r = [x + y for x in a for y in b] 

assert r == ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']


#use a dictionary comprehension to create a dictionary where the keys are 2,3,4 and the values are the keys squared

r = {x:x**2 for x in range(2,5)}

assert r == {2: 4, 3: 9, 4: 16}


print "Great Job"
