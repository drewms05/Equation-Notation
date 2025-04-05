"""A program that switches a user-inputted equation between
   postfix and infix notation, and then solves it

Drew Schlabach
4/5/25
"""
import re as re

operator_precedence = {'^': 6, '*': 5, '/': 5, '+': 4, '-': 4, '(': 3}

def get_input():
    equation = input('\nPlease input your equation in either format (for postfix, operands must be delimited from each other by a space): ')
    tight_equation = list(equation.replace(' ', ''))
    try:
        tight_equation[-1] = int(tight_equation[-1])
        type = 0
    except:
        if tight_equation[-1] == ')':
            type = 0
        else:
            type = 1
    for i in tight_equation:
        try: 
            i = int(i)
        except:
            if i != '+' and i != '^' and i != '-' and i != '*' and i != '/' and i != '.' and i != '(' and i != ')':
                type = 2
            else:
                continue
    return type, equation


def to_postfix(equation):
    terms = equation.translate(str.maketrans({'+': ' + ', '-': ' - ', '*': ' * ', '/': ' / ', '^': ' ^ ', '(': ' ( ', ')': ' ) '}))
    terms = list(terms.split(' '))
    terms = list(filter(lambda x: x != '', terms))
    stack = []
    result = []
    for t in terms:
        try:
            if '.' in t:
                t = float(t)
            else:
                t = int(t)
            t = str(t)
            t = f'({t})'
            result.append(t)

        except:
            if t == '(':
                stack.append(t)
            elif t == ')':
                for s in reversed(stack):
                    if s != '(':
                        result.append(s)
                        stack.remove(s)
                    else:
                        stack.remove(s)
            else:
                while True:
                    if stack == []:
                        stack.append(t)
                        break
                    elif operator_precedence.get(t) > operator_precedence.get(stack[-1]):
                        stack.append(t)
                        break
                    else:
                        result.append(t)
                        stack.remove(t)
                        continue
    for s in reversed(stack):
        result.append(s) 
    try:
        solution = terms.copy()
        for i in range(len(solution)):
            if solution[i] == '^':
                solution[i] = '**'
        solution = eval(' '.join(str(x) for x in solution))
    except:
        print("\nError evaluating equation. Please check your input.\n")
        main()
    result = ''.join(result)
    return result, solution

def to_infix(equation):
    terms = equation.translate(str.maketrans({'+': ' + ', '-': ' - ', '*': ' * ', '/': ' / ', '^': ' ^ ', '(': ' ( ', ')': ' ) '}))
    terms = list(terms.split(' '))
    terms = list(filter(lambda x: x != '', terms))
    stack = []
    result = []

    for t in terms:
        try:
            if '.' in t:
                t = float(t)
            else:
                t = int(t)
            t = str(t)
            stack.append(t)
        except:
            temp = []
            temp.append(stack[-2])
            temp.append(t)
            temp.append(stack[-1])
            expression = (f'({temp[0]} {temp[1]} {temp[2]})')
            stack.remove(stack[-1])
            stack.remove(stack[-1])
            stack.append(expression)

    result = (stack[0])[1:-1]

    try:
        solution = list(result)
        for i in range(len(solution)):
            if solution[i] == '^':
                solution[i] = '**'
        solution = ''.join(solution)
        solution = eval(solution)
    except:
        print("\nError evaluating equation. Please check your input.\n")
        main()

    return result, solution

def main():
    print("Welcome to the postfix/infix equation swapper and solver!")
    type, equation = get_input()
    if type == 2:
        print("\nError parsing equation. Please check your input.\n")
        main()
    elif type == 0:
        result, solution = to_postfix(equation)
        print(f'\nPostfix: {result}')
        print(f'Solution: {solution}\n')
    else:
        result, solution = to_infix(equation)
        print(f'\nInfix: {result}')
        print(f'Solution: {solution}\n')
    main()

if __name__ == '__main__':
    main()
