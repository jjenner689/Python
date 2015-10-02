# Write a recursive algorithm that goes into a nested hash structure and sums all key, value pairs - where the value is not a hash

test_hash = {1:2,3:{4:5}}

def sum_hash(hash_):
	sum_ = 0
	for i in hash_:
		if type(hash_[i]) != type({}):
			sum_ += i + hash_[i]
		else:
			sum_ += i +sum_hash(hash_[i])
	return sum_

r = sum_hash(test_hash)
assert r == 15

# Write a recursive algorithm that goes into a nested array with integers and sums all the integers.

array = [1,2,3,[4,5,6,[2,3,4,5]]]

def sum_array(array):
	s = 0
	for i in array:
		if type(i) != type([]):
			s += i
		else:
			s += sum_array(i)
	return s

r = sum_array(array)
assert r == 35


# Write a function permute such that:
# permute('abc') returns ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
def permute(string):
	array = []
	copy = string[:]
	copy2 = string[:]
	for a in string:
		for b in copy:
			for c in copy2:
				if a != b and a != c and b != c:
					array.append(a + b +c)
	array = set(array)
	return array

def permute2(string):
	array = []

	if len(string) == 1:
		return [string]

	for i in string:
		for b in permute2(string.replace(i, '', 1)):
			array.append(i+b)

	return array

# Write a function that computes factorials using tail call recursion

def tail_factorial(n, sum_ = 1):

	if n == 1:
		return sum_

	sum_ *= n

	return tail_factorial(n-1, sum_)

# Write a function that returns the greatest common denominator of two numbers using tail call recursion

def greatest_common_denom(n, k):

	if n%k == 0:
		return k

	if k%n == 0:
		return n

	if n%k == n:
		return greatest_common_denom(k, k%n)
	else:
		return greatest_common_denom(k, n%k)

print permute2('abcd')
