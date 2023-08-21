from visualization import draw_nfa, print_nfa
from regex_to_nfa import infix_to_postfix, parse_regex_to_nfa

# Generate NFA from regex
regex = 'a|b*'
postfix_regex = infix_to_postfix(regex)
nfa = parse_regex_to_nfa(postfix_regex)
print_nfa(nfa.start)

# Draw and save NFA to an image
graph = draw_nfa(nfa.start)
graph.render(filename='nfa', format='png', cleanup=True)