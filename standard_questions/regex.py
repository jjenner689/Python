'''

Regular expressions are a powerful tool to identify patterns in text.

This can be used to:

1) search,
2) validate,
3) extract, and
4) replace data.

edit the regex variable so that the assert statement passes

'''



import re



#find the number in this text

a = "In the year 2000"

regex = "(\d+)"

assert re.search(regex,a).groups()[0] == '2000'


#use match to see if the input is valid

a = "<html>"

regex = "<[a-z]+>"

assert re.match(regex,a).group()

a = "</html>"
regex = "</[a-z]+>"

assert re.match(regex,a).group()


a = "me@awesome.com"
regex = "[a-z]+@[a-z]+.[a-z]+"

assert re.match(regex,a)group()

#find and group all the numbers in this text

a = "10 20 30"

regex = "\d+"

assert re.findall(regex,a) == ['10', '20', '30']


#Using regex pull out all the theater numbers

a = '''Theater 1
Theater 2
'''

regex = "\d"

assert re.findall(regex,a) == ['1','2']


#using regex print out all the movie names

a = '''Theater 1: Jurasic Park
Theater 2: Fight Club
Theater 3: Skyfall
'''

regex = r"(\d): ([A-Za-z ]+)"

assert re.findall(regex,a) == [('1', 'Jurasic Park'), ('2', 'Fight Club'), ('3', 'Skyfall')]








