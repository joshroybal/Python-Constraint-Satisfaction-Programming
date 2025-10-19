# early_risers.py
from typing import List, Dict, Optional
from itertools import product
from csp import CSP, Constraint

#def pretty_print(row: List[Union[str, int]]) -> None:
#    print(''.join(['{:20s}'.format(str(s)) for s in row]))

def pretty_print(d: Dict[str, List[str]]) -> None:
    for k in d:
        print(''.join(['{:20s}'.format(s) for s in [str(k)] + d[k]]))

def all_distinct(d: Dict[str, List[str]]) -> bool:
    checked: List[List[str]] = []
    for key in d:
        for t in checked:
            for item in d[key]:
                if item in t:
                    return False
        checked.append(d[key])
    return True

# Save this - this was by far the empirically best processing ordering!
class LogicPuzzleConstraint(Constraint[str, List[str]]):
    def __init__(self, variables: List[str]) -> None:
        super().__init__(variables)
        self.variables: List[str] = variables

    def satisfied(self, assignment: Dict[str, List[str]]) -> bool:
        if not all_distinct(assignment):
            return False

        # constrain variables

        # constrain domains
        
        # search for constraints
        
        return True

if __name__ == '__main__':
    dates: List[str] = ['18th', '19th', '20th', '21st', '22nd']
    families: List[str] = ['Beach', 'Poole', 'Sandys', 'Sunley', 'Tanner']
    destinations: List[str] = ['Canary Islands', 'Costa del Sol', 'Cyprus', 'Greece', 'Majorca']
    airports: List[str] = ['Birmingham', 'Gatwick', 'Heathrow', 'Luton', 'Stansted']
    domains: Dict[str, List[List[str]]] = { date: [list(t) for t in list(product(families, destinations, airports))] for date in dates }
    csp: CSP[str, List[str]] = CSP(dates, domains)
    csp.add_constraint(LogicPuzzleConstraint(dates))
    solution: Optional[Dict[str, List[str]]] = csp.backtracking_search()

    if solution is None:
        print('No solution found!')
    else:
        print('Solution found!')
        #print(solution)
        pretty_print(solution)
