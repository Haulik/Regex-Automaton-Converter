from nfa import State, NFA

def literal_nfa(ch):
    start = State()
    accept = State(True)
    start.transitions[ch] = accept
    return NFA(start, accept)

def concatenate(nfa1, nfa2):
    nfa1.accept.epsilon_transitions.add(nfa2.start)
    nfa1.accept.is_accepting = False
    return NFA(nfa1.start, nfa2.accept)

def union(nfa1, nfa2):
    start = State()
    accept = State(True)
    
    start.epsilon_transitions.add(nfa1.start)
    start.epsilon_transitions.add(nfa2.start)
    
    nfa1.accept.epsilon_transitions.add(accept)
    nfa1.accept.is_accepting = False
    
    nfa2.accept.epsilon_transitions.add(accept)
    nfa2.accept.is_accepting = False
    
    return NFA(start, accept)

def kleene_star(nfa):
    start = State()
    accept = State(True)
    
    start.epsilon_transitions.add(nfa.start)
    start.epsilon_transitions.add(accept)
    
    nfa.accept.epsilon_transitions.add(nfa.start)
    nfa.accept.epsilon_transitions.add(accept)
    nfa.accept.is_accepting = False
    
    return NFA(start, accept)