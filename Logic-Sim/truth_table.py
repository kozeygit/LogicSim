from itertools import permutations
from os import system as sys

# executes the boolean expression
def do(exp, d, n):
    new_d = d
    perm = []
    for i in range(n):
        x = exp
        for ii in d:
            x = x.replace(ii, str(d[ii][i]))
            #print(x)
            #print(d)
        end = eval(x)
        perm.append(end)
    new_d['OUT'] = perm
    #print(new_d)
    return new_d


def generateTruthTable(expression):
  
    # string manipulation to replace words with operators that can be executed
    exp = expression.lower()
    exp = exp.replace("not ", "2+~ ")
    exp = exp.replace("not", "2+~ ")
    exp = exp.replace("and", "&")
    exp = exp.replace("xor", "^")
    exp = exp.replace("or", "|")
    
    operators = ["2+~", "&", "^", "|", "(", ")"]
    variables = []

    # gets list of variables in expression
    temp_exp = exp.replace("(", "").replace(")", "")
    for i in temp_exp.split(" "):
        if i not in operators and i not in variables:
            #print(i)
            variables.append(i)

    no_variables = len(variables)

    # gets a list of 
    temp = [0 for i in range(no_variables)] + [1 for i in range(no_variables)]
    p = permutations(temp, no_variables)
    perm = []
    for i in p:
        if i not in perm:
            perm.append(i)
    #print(perm)

    v = dict()
    for i,j in enumerate(variables):
        v[j] = [ii[i] for ii in perm]
    #print(v)

    final = do(exp, v, len(perm))

    print("Boolean Expression: " + expression.upper())
    print()
    for i in final:
        if i.lower() == 'out':
            print(f"|{i}", end='')
        else:
            print(f"| {i} ", end='')
    print('|')
    for i in range(len(perm)):
        for ii in final:
            print(f"| {final[ii][i]} ", end='')
        print('|')



if __name__ == '__main__':
    sys('clear')
    e = input('Here: ')
    generateTruthTable(e)
    print()


    """NOT ((A and B) or (c and not B))"""


