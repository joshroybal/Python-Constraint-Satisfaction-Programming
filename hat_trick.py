# hat_trick.py
from typing import List, Dict, Optional
from itertools import product
from csp import CSP, Constraint

def print_table(d: Dict[str, List[str]]) -> None:
    print(80 * '=')
    print(''.join(f'{s:20s}' for s in ['month', 'flowers', 'other item', 'bride']))
    print(80 * '=')
    for k in d:
        print(''.join(f'{s:20s}' for s in [str(k)] + d[k]))
    print(80 * '=')
       
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

def has31days(s: str) -> bool:
    return s in ['May', 'July', 'August']


def prune(d: Dict[str, List[List[str]]]) -> None:
    # 1.
    d['April'] = [ v for v in d['April'] if 'cousin' not in v  and 'workmate' not
                   in v and 'daisies' not in v and 'velvet bow' not in v and
                   'scarlet ribbon' not in v ]
    d['May'] = [ v for v in d['May'] if 'scarlet ribbon' not in v ]
    d['July'] = [ v for v in d['July'] if 'cherry blossom' in v  and 'niece' not
                  in v ]
    d['August'] = [ v for v in d['August'] if 'roses' not in v and 'sister'
                    not in v and 'poppies' not in v and 'friend' not in v and
                    'velvet bow' not in v and 'niece' not in v ]
    for k in d:
        # 1.
        d[k] = [ v for v in d[k] if not ('cousin' in v and 'roses' in v) ]
        # 2.
        d[k] = [ v for v in d[k] if eqv('cornflowers' in v, 'lace' in v) ]
        d[k] = [ v for v in d[k] if imp('cornflowers' in v and 'lace' in v, has31days(k)) ]
        # 3.
        d[k] = [ v for v in d[k] if eqv('pink net' in v, 'workmate' in v) ]
        # 4.
        d[k] = [ v for v in d[k] if eqv('poppies' in v, 'friend' in v) ]
        d[k] = [ v for v in d[k] if imp('poppies' in v or 'friend' in v,
                                        'green ribbon' not in v) ]

class LogicPuzzleConstraint(Constraint[str, List[str]]):
    def __init__(self, variables: List[str]) -> None:
        super().__init__(variables)
        self.variables: List[str] = variables

    def satisfied(self, assignment: Dict[str, List[str]]) -> bool:
        if not all_distinct(assignment):
            return False
        if len(assignment) < 5:
            return True
        x = assignment.values()

        # 1.
        cousin_month, = (i for i, v in enumerate(x) if any('cousin' in x for x in v))
        roses_month, = (i for i, v in enumerate(x) if any('roses' in x for x in v))
        if cousin_month - roses_month != 1:
            return False
        # 3.
        workmate_month, = (i for i, v in enumerate(x)
                           if any('workmate' in x for x in v))
        sister_month, = (i for i, v in enumerate(x)
                         if any('sister' in x for x in v))
        if workmate_month < sister_month:
            return False

        # 4.
        poppies_month, = (i for i, v in enumerate(x)
                           if any('poppies' in x for x in v))
        daisies_month, = (i for i, v in enumerate(x)
                         if any('daisies' in x for x in v))
        if poppies_month > daisies_month:
            return False        

        # 6.
        niece, = (i for i, v in enumerate(x) if any('niece' in x for x in v))
        velvet_bow, = (i for i, v in enumerate(x) if any('velvet bow' in x for x in v))
        scarlet_ribbon, = (i for i, v in enumerate(x) if any('scarlet ribbon' in x for x in v))
        if not (niece < velvet_bow < scarlet_ribbon):
            return False        

        
        return True

if __name__ == '__main__':
    variables: List[str] = ['April', 'May', 'June', 'July', 'August']
    flowers: List[str] = ['cherry blossom', 'cornflowers', 'daisies', 'poppies', 'roses']
    other_item: List[str] = ['green ribbon', 'lace', 'pink net', 'scarlet ribbon', 'velvet bow']
    bride: List[str] = ['cousin', 'friend', 'niece', 'sister', 'workmate']
    domains: Dict[str, List[List[str]]] = { variable: [list(t) for t in list(product(flowers, other_item, bride))] for variable in variables }
    #print([ len(domains[k]) for k in domains ])
    #print('pruning')
    prune(domains)
    #print([ len(domains[k]) for k in domains ])
    csp: CSP[str, List[str]] = CSP(variables, domains)
    csp.add_constraint(LogicPuzzleConstraint(variables))
    solution: Optional[Dict[str, List[str]]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print('Solution found!')
        #print(solution)
        print_table(solution)
