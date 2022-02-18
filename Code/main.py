from logic.gates import *
from logic.board import *
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
or1 = Or_Gate()
a1 = And_Gate()
a2 = And_Gate()
n1 = Not_Gate()
o1 = Output()


b = Board()
print("1")
b.addGate(s1,s2,a1,a2,n1,o1)
print("2")
b.connectGate(a1, s1)
print("3")
b.connectGate(a1, s2)
print("4")
b.connectGate(n1, a1)
print("5")
b.connectGate(o1, n1)
print("6")
print(o1.getOutput())
print("7")
print(o1.getExpression())
print("8")#
b.disconnectGate(or1,s1)
print(b.getTruthTable(o1))