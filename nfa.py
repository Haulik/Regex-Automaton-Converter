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
