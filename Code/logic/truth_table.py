from itertools import permutations
from os import system as sys

# executes the boolean expression
def getOutputs(expression, dictionary, num_permutations):
    truth_dictionary = dictionary
    list_of_outputs = []
    for i in range(num_permutations):
        expression_with_variables = expression
        for variable in truth_dictionary:
            expression_with_variables = expression_with_variables.replace(variable, str(dictionary[variable][i]))
        output = eval(expression_with_variables)
        list_of_outputs.append(output)
    truth_dictionary['OUT'] = list_of_outputs
    return truth_dictionary


def generateTruthTable(expression):
  
    # string manipulation to replace words with operators that python can evaluate
    # making words operators also help when finding variables
    input_expression = expression
    expression = expression.lower()
    expression = expression.replace("not ", "2+~ ")
    expression = expression.replace("not", "2+~ ")
    expression = expression.replace("and", "&")
    expression = expression.replace("xor", "^")
    expression = expression.replace("or", "|")
    
    operators = ["2+~", "&", "^", "|", "(", ")"]
    variables = []

    # gets list of the differnt variables in the expression
    temp_exp = expression.replace("(", "").replace(")", "")
    for i in temp_exp.split(" "):
        if i not in operators and i not in variables:
            variables.append(i)
    num_variables = len(variables)

    # gets a list of permutations based on the number of variables, also removes repeats
    temp = [0 for i in range(num_variables)] + [1 for i in range(num_variables)]
    p = permutations(temp, num_variables)
    variable_permutations = []
    for i in p:
        if i not in variable_permutations:
            variable_permutations.append(i)


    dictionary = dict()
    for i,j in enumerate(variables):
        dictionary[j] = [ii[i] for ii in variable_permutations]

    final_dictionary = getOutputs(expression, dictionary, len(variable_permutations))

    final_string = ''
    final_string = final_string + str("Boolean Expression: " + input_expression.upper() + "\n")
    for i in final_dictionary:
        if i.lower() == 'out':
            final_string = final_string + (f"|{i}")
        else:
            final_string = final_string + (f"| {i} ")
    final_string = final_string + ('|\n')
    for i in range(len(variable_permutations)):
        for ii in final_dictionary:
            final_string = final_string + (f"| {final_dictionary[ii][i]} ")
        final_string = final_string + ('|\n')

    return final_string


if __name__ == '__main__':
    sys('clear')
    e = input('Here: ')
    print(generateTruthTable(e))
    print()


    """NOT ((A and B) or (c and not B))"""




