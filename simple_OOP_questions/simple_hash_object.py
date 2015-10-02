'''

Build your own hash implementation using the simple_hash_function.


'''

def simple_hash_function(key,array_size):
    """ simple_hash_function takes a key, and the size of the array """
    ret = 0
    for i in key:
        ret = 31*ret + ord(i)
    return ret % array_size


#create your one miny hash table, using the simple_hash function.


class Hash():
    def __init__(self):
        self.size = 100
        self.array = [None for x in range(self.size)]

    def __getitem__(self, key):
        index = simple_hash_function(key, self.size)
        return self.array[index]
        

    def __setitem__(self, key, item):
        index = simple_hash_function(key, self.size)
        self.array[index] = item
        


h = Hash()

h['test'] = 5

assert h['test'] == 5




    
    

