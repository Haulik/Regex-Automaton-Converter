class State:
    def __init__(self, is_accepting=False):
        self.transitions = {}
        self.is_accepting = is_accepting
        self.epsilon_transitions = set()

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept