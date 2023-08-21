from regex_to_nfa import regex_to_nfa
from visualization import visualize_nfa

def preprocess_regex(regex):
    new_regex = []
    specials = set("()*|")
    prev_char = ""

    for i, char in enumerate(regex):
        new_regex.append(char)

        # Check for possible concatenation scenarios
        if char not in specials and i+1 < len(regex):
            next_char = regex[i+1]

            if next_char not in specials and next_char != '|':
                new_regex.append('concat')
            elif char != '|' and next_char == '(':
                new_regex.append('concat')
            elif char == ')' and next_char not in specials and next_char != '|':
                new_regex.append('concat')

    return ''.join(new_regex)

regex = "a*b|c"
pre_nfa = preprocess_regex(regex)
nfa = regex_to_nfa(pre_nfa)
visualize_nfa(nfa)
