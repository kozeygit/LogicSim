from Logic_Gates import *
from Board import *
import random
import os
# import ui



# class Queue:
#   def __init__(self, *args):
#     self.q = list(args)

# s1 = Switch()
# s2 = Switch()
# o1 = Or_Gate()
# o2 = Or_Gate()
# n1 = Not_Gate()
# n2 = Not_Gate()
# out = Output()


# o1.connectNode(1, s1)
# o1.connectNode(2, s2)
# s1.flip()
# out.connectNode(o1)
# out.printOutput()


# class Simulation():
#     def __init__(self):
#         self.board = Board


s1 = Switch()
s2 = Switch()
a1 = And_Gate()
a2 = And_Gate()
n1 = Not_Gate()
o1 = Output()


a1.connectNode(1, s1)
a1.connectNode(2, s2)

print(a1.name+':', a1.getOutput())

s1.flip()
print(a1.name+':', a1.getOutput())

s2.flip()
print(a1.name+':', a1.getOutput())

n1.connectNode(1, a1)

print(n1.name+':', n1.getOutput())
print(s1.name)

print(a1.getExpression())
print(n1.getExpression())

a2.connectNode(1, n1)
a2.connectNode(2, s1)

o1.connectNode(a2)

ex = o1.getExpression()

print(ex)
print()
o1.truthTable()

