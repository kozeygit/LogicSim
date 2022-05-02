from itertools import permutations
from os import system as sys
from typing import Union, Tuple

def get_tt_outputs(expression: str, dictionary: dict[str, list], num_permutations: int) -> dict[str, list]:
    '''Adds OUT variable and values to incomplete truth table dictionary using by replacing variables in given expression.'''
    truth_dictionary = dictionary
    list_of_outputs = []
    for i in range(num_permutations):
        expression_with_variables = expression
        for variable in truth_dictionary:
            expression_with_variables = expression_with_variables.replace(variable, str(dictionary[variable][i]))
        try:
            output = eval(expression_with_variables)
        except SyntaxError as e:
            print(e, expression_with_variables)
            return "Error"
        list_of_outputs.append(output)
    truth_dictionary['OUT'] = list_of_outputs
    return truth_dictionary


def generate_truth_table(expression: str) -> Union[Tuple[dict[str, list], str], str]:
    '''Returns a truth table in dictionary form'''
    input_expression = expression
    expression = expression.lower()
    expression = expression.replace("not ", "2+~ ")
    expression = expression.replace("not", "2+~ ")
    expression = expression.replace("and", "&")
    expression = expression.replace("xor", "^")
    expression = expression.replace("or", "|")
    
    operators = ["2+~", "&", "^", "|", "(", ")"]
    variables = []

    temp_exp = expression.replace("(", "").replace(")", "")
    for var in temp_exp.split(" "):
        if var not in operators and var not in variables:
            variables.append(var)
    num_variables = len(variables)

    temp = [0 for _ in range(num_variables)] + [1 for _ in range(num_variables)]
    perms = permutations(temp, num_variables)
    variable_permutations = []
    for perm in perms:
        if perm not in variable_permutations:
            variable_permutations.append(perm)

    dictionary = dict()
    for i, key in enumerate(variables):
        dictionary[key] = [perm[i] for perm in variable_permutations]

    final_dictionary = get_tt_outputs(expression, dictionary, len(variable_permutations))

    if final_dictionary == "Error":
        return "Invalid Input"
    else:
        return (final_dictionary, input_expression)


if __name__ == '__main__':
    '''For Testing'''
    sys('clear')
    exp = input('Here: ')
    print(generate_truth_table(exp))
    print()

