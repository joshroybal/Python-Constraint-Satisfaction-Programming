# cheque_list.py
from typing import List, Tuple, Dict, Optional
from itertools import product
from csp import CSP, Constraint

def print_table(d: Dict[int, Tuple[str, str, int]]) -> None:
    print(80 * '=')
    print(''.join(f'{s:20s}' for s in ['Amount', 'Payer', 'Sort code', 'Cheque number']))
    print(80 * '=')
    for k in d:
        t = [ u'\xA3' + str(k)] + [ str(v) for v in d[k] ]
        print(''.join(f'{s:20s}' for s in t))
    print(80 * '=')
       
def all_distinct(d: Dict[int, Tuple[str, str, int]]) -> bool:
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

def prune(d: Dict[int, List[Tuple[str, str, int]]]) -> None:
    # 1.
    d[680] = [ v for v in d[680] if '60-02-11' in v and 'Watkins and Co' not in v ]
    # 2.
    d[120] = [ v for v in d[120] if 'John Arnold and Co' not in v and 'Watkins and Co' not in v and 10042 not in v ]
    # 3.
    d[892] = [ v for v in d[892] if 'John Arnold and Co' not in v ]
    d[120] = [ v for v in d[120] if 'Latimer UK' not in v ]
    
    for k in d:
        # 1.
        d[k] = [ v for v in d[k] if eqv('Watkins and Co' in v, 5018 in v) ]
        d[k] = [ v for v in d[k] if imp('Watkins and Co' in v, k < 680) ]
        # 2.
        d[k] = [ v for v in d[k] if imp('48-16-08' in v, 'John Arnold and Co' not in v and 'Watkins and Co' not in v and 10042 not in v) ]
        d[k] = [ v for v in d[k] if imp('John Arnold and Co' in v, v[-1] > 5018) ]
        # 3.
        d[k] = [ v for v in d[k] if eqv(3165 in v, k == 463) ]
        # 4.
        d[k] = [ v for v in d[k] if imp('81-20-16' in v, 3165 not in v)
                 and imp('Galacraft' in v, 10042 not in v) ]
        # 5.
        d[k] = [ v for v in d[k] if eqv('Dentex' in v, '55-10-04' in v) ]
        # 6.
        d[k] = [ v for v in d[k] if eqv(10042 in v, '74-15-30' in v) ]

class LogicPuzzleConstraint(Constraint[int, Tuple[str, str, int]]):
    def __init__(self, variables: List[int]) -> None:
        super().__init__(variables)
        self.variables: List[int] = variables

    def satisfied(self, assignment: Dict[int, Tuple[str, str, int]]) -> bool:
        if not all_distinct(assignment):
            return False       
        return True

if __name__ == '__main__':
    variables: List[int] = [ 120, 315, 463, 680, 892 ]
    payer: List[str] = [ 'Dentex', 'Galacraft', 'John Arnold and Co',
                         'Latimer UK', 'Watkins and Co']
    sort_code: List[str] = [ '48-16-08', '55-10-04', '60-02-11', '74-15-30',
                             '81-20-16']
    cheque_number: List[int] = [ 3165, 5018, 7724, 8561, 10042 ]
    domains: Dict[int, List[Tuple[str, str, int]]] = { variable: list(product(payer, sort_code, cheque_number)) for variable in variables }
    #print([ len(domains[k]) for k in domains ])
    #print('pruning')
    #prune(domains)
    #print([ len(domains[k]) for k in domains ])
    #quit()
    csp: CSP[int, Tuple[str, str, int]] = CSP(variables, domains)
    csp.add_constraint(LogicPuzzleConstraint(variables))
    solution: Optional[Dict[int, Tuple[str, str, int]]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print('Solution found!')
        #print(solution)
        print_table(solution)
