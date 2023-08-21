from nfa import NFA, NFAState
from shunting_yard import shunting_yard_algorithm, is_operand, is_operator


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
            elif token == 'concat':
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