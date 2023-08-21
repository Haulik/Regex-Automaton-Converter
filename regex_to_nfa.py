from graphviz import Digraph

def visualize_nfa(nfa):
    dot = Digraph()
    dot.attr(rankdir='LR')  # Set layout to left-to-right

    # Add states
    dot.node(str(nfa.start.state_id), shape='point')
    dot.node(str(nfa.accept.state_id), shape='doublecircle')
    for state in nfa.states:
        dot.node(str(state.state_id))

    # Add transitions
    for state in nfa.states:
        for symbol, next_state in state.transitions:
            dot.edge(str(state.state_id), str(next_state.state_id), label=symbol)

    dot.render("nfa_visualization", format="png", cleanup=True)



class NFAState:
    def __init__(self, state_id):
        self.state_id = state_id
        self.transitions = []  # List of (symbol, next_state) pairs

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept
        self.states = set()  # Store all states in the NFA
        self.transitions = []  # Store all transitions in the NFA

    def add_state(self, state):
        self.states.add(state)

    def add_transition(self, from_state, symbol, to_state):
        self.transitions.append((from_state, symbol, to_state))



def shunting_yard_algorithm(expression):
    output_queue = []
    operator_stack = []
    precedence = {'*': 3, '|': 2, '': 1}

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
    return token in ('*', '|', '')


def is_operand(token):
    return token.isalpha() or token.isdigit()  # You can customize this based on your requirements


def regex_to_nfa(regex):
    postfix_regex = shunting_yard_algorithm(regex)
    nfa_stack = []
    state_counter = 0  # Used to generate unique state IDs

    for token in postfix_regex:
        if is_operand(token):
            # Create a new NFA state for each operand
            start_state = NFAState(state_counter)
            accept_state = NFAState(state_counter + 1)
            state_counter += 2

            # Create a transition from start to accept using the operand
            start_state.transitions.append((token, accept_state))

            # Create an NFA object and store states and transitions
            nfa = NFA(start_state, accept_state)
            nfa.add_state(start_state)
            nfa.add_state(accept_state)
            nfa.add_transition(start_state, token, accept_state)  # Add transition to NFA transitions

            # Push the NFA fragment onto the stack
            nfa_stack.append(nfa)
        elif is_operator(token):
            if token == '*':
                # Apply closure operation and push the result onto the stack
                nfa1 = nfa_stack.pop()
                # Implement Thompson's construction for closure
                new_start = NFAState(state_counter)
                new_accept = NFAState(state_counter + 1)
                state_counter += 2
                # Connect new_start to nfa1.start and nfa1.accept to new_accept
                # Add epsilon transitions for closure
                new_start.transitions.append(('', nfa1.start))
                nfa1.accept.transitions.append(('', new_accept))
                nfa1.accept.transitions.append(('', nfa1.start))
                # Push the result NFA onto the stack
                nfa_stack.append(NFA(new_start, new_accept))
            elif token == '|':
                # Apply union operation and push the result onto the stack
                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()
                # Implement Thompson's construction for union
                new_start = NFAState(state_counter)
                new_accept = NFAState(state_counter + 1)
                state_counter += 2
                # Connect new_start to nfa1.start and nfa2.start
                new_start.transitions.append(('', nfa1.start))
                new_start.transitions.append(('', nfa2.start))
                # Connect nfa1.accept and nfa2.accept to new_accept
                nfa1.accept.transitions.append(('', new_accept))
                nfa2.accept.transitions.append(('', new_accept))
                # Push the result NFA onto the stack
                nfa_stack.append(NFA(new_start, new_accept))
            elif token == '':
                # Apply concatenation operation and push the result onto the stack
                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()
                # Implement Thompson's construction for concatenation
                # Connect nfa1.accept to nfa2.start
                nfa1.accept.transitions.append(('', nfa2.start))
                # Push the result NFA onto the stack
                nfa_stack.append(NFA(nfa1.start, nfa2.accept))

    final_nfa = nfa_stack.pop()
    return final_nfa


regex = "a*b|c"
nfa = regex_to_nfa(regex)
visualize_nfa(nfa)