
'''

A good use for OOP is to create new data types. So let's do that. We are going to create a new data type to handle fractions.

Fix the following code to be able to add and equate fractions.

'''

def gcd(m,n):
     """ Greatest Common Divisor """
     while m%n != 0:
          oldm = m
          oldn = n

          m = oldn
          n = oldm%oldn
     return n

class Fraction:
     def __init__(self, top, bottom):
          self.top = top
          self.bottom = bottom
          self.reduce()

     def reduce(self):
          great_com_div = gcd(self.top, self.bottom)
          self.top /= great_com_div
          self.bottom /= great_com_div

     def __str__(self):
          return "%s/%s" % (self.top, self.bottom)

     def __add__(self,otherfraction):
          if self.bottom == otherfraction.bottom:
               new_top = self.top + otherfraction.top
               new_bottom = self.bottom
          else:
               new_top = self.top*otherfraction.bottom + otherfraction.top*self.bottom
               new_bottom = self.bottom*otherfraction.bottom
          
          return Fraction(new_top, new_bottom)

     def __eq__(self, other):
          if self.top == other.top and self.bottom == other.bottom:
               return True
          else:
               return False

  
x = Fraction(1,2)
y = Fraction(2,3)
z = Fraction(20,10)
assert x+y == Fraction(7,6)




