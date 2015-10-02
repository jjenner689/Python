
'''

Using what you've learned about defining classes, create a new class 
called FileHandler that will:

1) Take in a filename on initialization

fh = FileHandler("filename.txt")

It has two instance variables - filename and filedata

2) Parse the file using readlines and store it in an instance variable called filedata

You might want to create your own dummy text file to test this.

3) Has three methods:

i) A method that writes data to file

fh.write_new_data(data_in_array_format)

ii) A method that splits current file based on line_number passed into it.  

The first part of the file gets stored in the original filedata/filename.

The second part of the file is returned in an array of strings format.

fh.splitfile(line_number)

iii) A method that prints out the current file data into console

fh.__print

The reason why we call it '__print()' as opposed to 'print()' is because of Python conventions.

Python engineers often add '__' in front of a method name to make it 'private'.  

The name scrambling is used to ensure that subclasses don't accidentally override the attributes of their superclasses. 

In this case, we don't want to override or conflict with the print() method.

You can reference code from exercise 10-file-io-1.

'''

class FileHandler:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
        	self.filedata = f.readlines()

    def write_data(self, data_array):
    	data = ''.join(data_array)
        with open(self.filename, 'w') as f:
        	f.write(data)
        self.__print()

    def write_new_file(self, new_file):
    	data = ''.join(self.filedata)
    	with open(new_file, 'w') as f:
        	f.write(data)

    def split_file(self, line_number):
    	new_data = self.filedata[line_number:]
    	self.write_data(self.filedata[:line_number])
    	self.filedata = new_data
    	return self.filedata


    def __print(self):
    	print self.filedata 

fh = FileHandler('file.txt')
fh.split_file(3)
fh.write_new_file('file2.txt')
#fh.__print

# Bonus: Write an additional method:
# 1) A method that takes in a new file and appends the data to the stored file and saves it




