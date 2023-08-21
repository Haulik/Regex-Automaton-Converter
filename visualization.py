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