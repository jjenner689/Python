'''

Recursively walk a filesystem.

'''

import os

def print_files(name, indent = 0):
	array = os.listdir(name)
	for i in array:
		path = os.path.join(name, i)
		if os.path.isdir(path):
			print "---"*indent + i
			print_files(path, indent+1)
		else:
			print "---"*indent  + i

def delete_files(name):
	array = os.listdir(name)
	for i in array:
		path = os.path.join(name, i)
		if os.path.isdir(path):
			delete_files(path)
			os.rmdir(path)
			#delete directory after all files deleted
		else:
			os.remove(path)
			#delete files

print_files('/home/josh/Desktop')
