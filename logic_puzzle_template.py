# early_risers.py
from typing import List, Dict, Optional
from itertools import product
from csp import CSP, Constraint

def print_table(d: Dict[str, List[str]]) -> None:
    for k in d:
        print(''.join(['{:20s}'.format(s) for s in [str(k)] + d[k]]))
       
def all_distinct(d: Dict[str, List[str]]) -> bool:
    t = [ e for l in [ d[k] for k in d ] for e in l ]
    if len(t) != len(set(t)):
        return False
    else:
        return True

# logical implication
def imp(p: bool, q: bool) -> bool:
    return not p or q

# logical equivalence
def eqv(p: bool, q:bool) -> bool:
    return implies(p, q) and implies(q, p)
      
class LogicPuzzleConstraint(Constraint[str, List[str]]):
    def __init__(self, variables: List[str]) -> None:
        super().__init__(variables)
        self.variables: List[str] = variables

    def satisfied(self, assignment: Dict[str, List[str]]) -> bool:
        if not all_distinct(assignment):
            return False
        return True

if __name__ == '__main__':
    variables: List[str] = ['', '', '', '', '']
    C2: List[str] = ['', '', '', '', '']
    C3: List[str] = ['', '', '', '', '']
    C4: List[str] = ['', '', '', '', '']
    domains: Dict[str, List[List[str]]] = { variable: [list(t) for t in list(product(C2, C3, C4))] for variable in variables }
    #prune(domains)
    csp: CSP[str, List[str]] = CSP(variables, domains)
    csp.add_constraint(LogicPuzzleConstraint(variables))
    solution: Optional[Dict[str, List[str]]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print('Solution found!')
        print_table(solution)
