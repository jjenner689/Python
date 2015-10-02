'''

Create a File System and simple terminal emulator.


A filesystem has a root, and on a unix based system the root is /

Thre can then be directories and files underneath each path.

/
users/
     steve/
          budget.csv
     racheal/
          books.txt
lib/
   shared/
   		stuff/
        	man.so


Mimic an fs using basic Python data structures.

Then allow a user through a simple input

ls
pwd
cd .. or cd <name>

Bonus: 

Create a directory.
Allow commands to work with ../../<name>

'''


class File:

	def __init__(self, name, parent):	
		self.name = name
		self.parent = parent

	def pwd(self):
		directories = []
		folder=self
		directories.append(self.name)

		while folder.parent != None:
			folder = folder.parent
			directories.append(folder.name)
		
		if len(directories) == 1:
			return '/'
		else:
			return '/'.join(reversed(directories))	

class Directory(File):

	def __init__(self, name, parent = None):
		File.__init__(self, name, parent)
		self.children = {}

	def create_child_directory(self, name):
		directory = Directory(name, self)
		self.children[name] = directory
		return directory

	def add_child_file(self, name):
		file_ = File(name, self)
		self.children[name] = file_
		return file_

	def list_children(self):
		return list(self.children)
		
	def change_directory(self, directory):
		if directory == '..':
			return self.parent
		elif directory in self.children and type(directory) == Directory:
			return self.children[directory]
		else:
			print '%s is not a directory.......' % directory
			return self


def handle_answer(answer, cwd):

	no_arg_commands =  {'pwd': cwd.pwd,
						'ls': cwd.list_children}
	one_arg_commands = {'mkdir': cwd.create_child_directory,
						'cd': cwd.change_directory,
						'touch': cwd.add_child_file} #may make cd a special command

	words = answer.split(' ')

	if words[0] in no_arg_commands or words[0] in one_arg_commands:

		if len(words) == 1:
			if words[0] in no_arg_commands:
				print no_arg_commands[words[0]]()
			else:
				print 'Too few arguments..........'

		elif len(words) == 2:
			if words[0] in one_arg_commands:
				if words[0] in ('mkdir', 'touch'):
					one_arg_commands[words[0]](words[1])
				else:
					cwd = one_arg_commands[words[0]](words[1])
			else:
				print 'Too many or too few arguments........'

		else:
			print 'Too many arguments.....'
	else:
		print 'Unable to recognise command "%s"' % words[0]

	return cwd

def play():
	answer=''
	cwd = root
	commands = {'pwd': cwd.pwd,
				'ls': cwd.list_children}
	while answer != 'q':
		answer = raw_input('> ')
		cwd = handle_answer(answer, cwd)

root = Directory('')

users = root.create_child_directory('users')
lib = root.create_child_directory('lib')

steve = users.create_child_directory('steve')
rachael = users.create_child_directory('racheal')

shared = lib.create_child_directory('shared')

stuff = shared.create_child_directory('stuff')
hello = stuff.add_child_file('hello.txt')

play()









