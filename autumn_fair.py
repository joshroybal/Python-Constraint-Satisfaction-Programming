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
    return imp(p, q) and imp(q, p)

def prune(d: Dict[str, List[List[str]]]) -> None:
    d['Cancer Research'] = [ v for v in d['Cancer Research'] if '87' not in v ]
    d['Hospice'] = [ v for v in d['Hospice'] if 'cowboys' not in v and '87' not in v ]
    d['Volunteer Centre'] = [ v for v in d['Volunteer Centre'] if '111' in v ]
    for k in d:
        d[k] = [ v for v in d[k] if imp('tombola' in v, 'vampires' in v and '128' not in v) ]
        d[k] = [ v for v in d[k] if imp('hoop-la' in v, '87' in v) ]
        d[k] = [ v for v in d[k] if eqv(k == 'Newstalk', 'vikings' in v) ]
        d[k] = [ v for v in d[k] if imp('balloon race' in v, '128' not in v) ]
        d[k] = [ v for v in d[k] if imp('darts game' in v, '106' not in v) ]
        d[k] = [ v for v in d[k] if eqv('pirates' in v, '94' in v) ]
        d[k] = [ v for v in d[k] if imp(k == 'Hospice', 'cowboys' not in v) ]
        d[k] = [ v for v in d[k] if imp('cowboys' in v, '128' not in v) ]
        d[k] = [ v for v in d[k] if eqv(k == 'Volunteer Centre', '111' in v) ]

class LogicPuzzleConstraint(Constraint[str, List[str]]):
    def __init__(self, variables: List[str]) -> None:
        super().__init__(variables)
        self.variables: List[str] = variables

    def satisfied(self, assignment: Dict[str, List[str]]) -> bool:
        if not all_distinct(assignment):
            return False
        if len(assignment) != 5:
            return True
        cancer_total = int(assignment['Cancer Research'][2])
        newstalk_total = int(assignment['Newstalk'][2])
        hospice_total = int(assignment['Hospice'][2])
        for v in assignment:
            stall, costume, total = assignment[v]
            if stall == 'tombola' and int(total) > cancer_total:
                return False
            if stall == 'balloon race' and int(total) > newstalk_total:
                return False
            if costume == 'cowboys' and int(total) > hospice_total:
                return False
        return True

if __name__ == '__main__':
    variables: List[str] = ['Cancer Research', 'Hospice', 'Newstalk', 'RSPCA', 'Volunteer Centre']
    C2: List[str] = ['balloon race', 'darts game', 'hoop-la', 'lucky dip', 'tombola']
    C3: List[str] = ['clowns', 'cowboys', 'pirates', 'vampires', 'vikings']
    C4: List[str] = ['87', '94', '106', '111', '128']
    domains: Dict[str, List[List[str]]] = { variable: [list(t) for t in list(product(C2, C3, C4))] for variable in variables }
    prune(domains)
    csp: CSP[str, List[str]] = CSP(variables, domains)
    csp.add_constraint(LogicPuzzleConstraint(variables))
    solution: Optional[Dict[str, List[str]]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print('Solution found!')
        print_table(solution)
