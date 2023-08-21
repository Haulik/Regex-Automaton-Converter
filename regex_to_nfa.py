from nfa_constructors import literal_nfa, concatenate, union, kleene_star

def parse_regex_to_nfa(regex):
    stack = []
    
    for char in regex:
        if char == 'a' or char == 'b':  # simple literals
            stack.append(literal_nfa(char))
        elif char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concatenate(nfa1, nfa2))
        elif char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(union(nfa1, nfa2))
        elif char == '*':
            nfa = stack.pop()
            stack.append(kleene_star(nfa))
    
    return stack[0]


def infix_to_postfix(regex):
    precedence = {'|': 1, '.': 2, '*': 3}
    output = []
    stack = []

    for char in regex:
        if char == 'a' or char == 'b':
            output.append(char)
        elif char in ['|', '.', '*']:
            while stack and precedence[char] <= precedence.get(stack[-1], 0):
                output.append(stack.pop())
            stack.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return ''.join(output)
