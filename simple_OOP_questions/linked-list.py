'''

A very common data strucutre is a linked list. It is a way of creating a list of data when you don't
know the size of the array ahead of time.

Python does this internally for many data structures.

We can easily mimic them in Python with a class.

A linked list has nodes.

Each node can have a value, and then a pointer or link to the next node. 

write as functions or possibly methods

print all the nodes, can be done recursively or iteratively 

add node - takes a root and find then end, add a new node to the end.

insert - takes a root, and new node, and a value to find, when found it inserts that value before
i.e. 1 -> 3. insert LL(2) to make 1->2->3

remove takes the root, and a value to remove from the list

'''

class LL():
    def __init__(self):
        self.value = None
        self.next = None

def add_node(root, value):
	node = root
	while node.next != None:
		node = node.next

	next_value = LL()
	next_value.value = value
	next_value.next = None
	node.next = next_value

def print_nodes(root):
	node = root
	while node.next != None:
		print node.value
		node = node.next
	print node.value

def insert(root, value, ind):
	node = root
	index = 0
	while index != ind-1:
		node = node.next
		index +=1

	next_value = LL()
	next_value.value = value
	next_value.next = node.next
	node.next = next_value

def remove(root, value):
	node = root
	while node.next.value != value:
		node = node.next

	to_remove = node.next
	node.next = to_remove.next

	del to_remove

root = LL()
root.value = 1



