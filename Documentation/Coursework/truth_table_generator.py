from itertools import permutations
from os import system as sys

# executes the boolean expression
def do(exp, *args):
  for i,j in enumerate(args):
    exp = exp.replace(str(chr(97 + i)), str(j))
  end = eval(exp)
  return end

def generateTruthTable(expression, variables=2):
  
  # string manipulation to replace words with operators that can be executed
  exp = expression.lower()
  exp = exp.replace("not", "not ")
  exp = exp.replace("not ", "2+~")
  exp = exp.replace("and", "&")
  exp = exp.replace("xor", "^")
  exp = exp.replace("or", " |")

  # checks how many unique variables in expression
  temp = []
  for i in exp:
    if ord(i) > 96 and ord(i) < 123:
      temp.append(i)
  variables = len(set(temp))
  

  temp = [0 for i in range(variables)] + [1 for i in range(variables)]
  
  # gets 
  o = permutations(temp, variables)
  l = []
  for i in o:
    if i not in l:
      l.append(i)


  print("Boolean Expression: " + expression.upper())
  print()
  for i in range(variables):
    print(f"| {str(chr(65 + i))} ", end='')
  print('|OUT|')
  for i in l:
    for ii in range(variables):
      print(f"| {i[ii]} ", end='')
    print(f'| {do(exp, *i)} |')

sys('clear')
generateTruthTable("NOT ((A and B) or (D and not C))", 2)
print()

  
"""NOT ((A and B) or (c and not B))"""
