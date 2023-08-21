from graphviz import Digraph

def draw_nfa(start_state):
    dot = Digraph()
    states = set()
    to_visit = [start_state]
    
    state_to_id = {}  # To map state objects to small integers
    next_id = 1

    while to_visit:
        state = to_visit.pop()
        if state in states:
            continue
        if state not in state_to_id:
            state_to_id[state] = str(next_id)
            next_id += 1
        states.add(state)
        for char, next_state in state.transitions.items():
            if next_state not in state_to_id:
                state_to_id[next_state] = str(next_id)
                next_id += 1
            dot.edge(state_to_id[state], state_to_id[next_state], label=char)
            to_visit.append(next_state)
        for next_state in state.epsilon_transitions:
            if next_state not in state_to_id:
                state_to_id[next_state] = str(next_id)
                next_id += 1
            dot.edge(state_to_id[state], state_to_id[next_state], label='ε')
            to_visit.append(next_state)

    return dot


def print_nfa(state, visited=None):
    if visited is None:
        visited = set()

    if state in visited:
        return

    visited.add(state)
    
    for char, next_state in state.transitions.items():
        print(f"State {id(state)} -- {char} --> State {id(next_state)}")
        print_nfa(next_state, visited)

    for next_state in state.epsilon_transitions:
        print(f"State {id(state)} -- epsilon --> State {id(next_state)}")
        print_nfa(next_state, visited)