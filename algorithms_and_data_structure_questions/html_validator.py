#Stack Challenge 2: Build an html validator using a stack data structure

test_html = '''<html><body><div><h1>Test Html</h1><p></p></div></body></html>'''
test_bad_html = '''<html><body><div><h1>Test Html</h1><p></div></body></html>'''
test_bad_html2 = "</div>"
test_bad_html3 = "<div>"

#Tip: You can consider using regex, but it is not recommended at this point because we have not taught it.  It is not necessary to solve this problem.
import re

def get_tokens(html):
    """Converts a string of html into an array of tokens"""
    array = []
    for i in range(len(html)):

    	if html[i] == '<':
    		flag = i
    	elif html[i] == '>':
    		array.append(html[flag:i+1])

    return array


def valid_html(tokens):
    """takes an array of tokens parsed from html, and validates correct ordering of open/close"""
    array = []
    for i in tokens:
    	if i[1] == '/':
    		if array == []:
    			return False
    		elif array.pop()[1:] == i[2:]:
    			pass
    		else:
    			return False
    	else:
    		array.append(i)

    return True


assert valid_html(get_tokens(test_html)) == True
assert valid_html(get_tokens(test_bad_html)) == False
assert valid_html(get_tokens(test_bad_html2)) == False



        
    


