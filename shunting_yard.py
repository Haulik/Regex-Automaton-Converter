def shunting_yard_algorithm(expression):
    output_queue = []
    operator_stack = []
    precedence = {'*': 3, '|': 2, 'concat': 1}

    for token in expression:
        if is_operand(token):
            output_queue.append(token)
        elif is_operator(token):
            while operator_stack and is_operator(operator_stack[-1]) and precedence[operator_stack[-1]] >= precedence[token]:
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()  # Pop and discard '('

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue


def is_operator(token):
    return token in ('*', '|', 'concat')


def is_operand(token):
    return token.isalnum()